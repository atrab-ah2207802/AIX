"use client";
import React from "react";
import { useTranslation } from "react-i18next";

/* ---------- Date Utilities ---------- */

function parseDateString(value) {
  if (!value || typeof value !== "string") return null;
  const monthNameRegex = /\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b/i;
  const isoDateRegex = /^\d{4}-\d{2}-\d{2}/;
  const dayMonthYearRegex = /^\d{1,2}[\s\/.-](?:\w+|\d{1,2})[\s\/.-]\d{2,4}/;

  if (!(monthNameRegex.test(value) || isoDateRegex.test(value) || dayMonthYearRegex.test(value)))
    return null;

  const d = new Date(value);
  if (!Number.isNaN(d.getTime())) return d;

  const dmY = value.match(/^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/);
  if (dmY) {
    let [_, dd, mm, yyyy] = dmY;
    if (yyyy.length === 2) yyyy = "20" + yyyy;
    const candidate = new Date(`${yyyy}-${String(mm).padStart(2, "0")}-${String(dd).padStart(2, "0")}`);
    if (!Number.isNaN(candidate.getTime())) return candidate;
  }

  return null;
}

function formatYYYYMMDD(date) {
  const y = date.getUTCFullYear();
  const m = String(date.getUTCMonth() + 1).padStart(2, "0");
  const d = String(date.getUTCDate()).padStart(2, "0");
  return `${y}${m}${d}`;
}

function addOneDay(date) {
  const copy = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
  copy.setUTCDate(copy.getUTCDate() + 1);
  return copy;
}

function googleCalendarAllDayUrl({ title = "", details = "", startDateObj, parties = [] }) {
  if (!startDateObj) return null;
  const start = formatYYYYMMDD(startDateObj);
  const end = formatYYYYMMDD(addOneDay(startDateObj));

  const partyString = parties.length
    ? `Parties: ${parties.map((p) => (p.role ? `${p.name} (${p.role})` : p.name)).join(" — ")}`
    : "";

  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: `${title} — ${partyString || "Contract Event"}`,
    details: `${details}\n\n${partyString}\n\n(Added by Concice)`,
    dates: `${start}/${end}`,
  });

  return `https://calendar.google.com/calendar/render?${params.toString()}`;
}

/* ---------- Recursive Date Collector ---------- */

function collectDates(obj, path = "") {
  const found = [];
  if (!obj) return found;

  if (Array.isArray(obj)) {
    obj.forEach((item, i) => found.push(...collectDates(item, `${path}[${i}]`)));
    return found;
  }

  if (typeof obj === "object") {
    for (const [k, v] of Object.entries(obj)) {
      const nextPath = path ? `${path}.${k}` : k;

      if (/date/i.test(k) && typeof v === "string") {
        const parsed = parseDateString(v);
        found.push({ label: k, path: nextPath, value: v, parsedDate: parsed });
      } else if (typeof v === "object") {
        found.push(...collectDates(v, nextPath));
      }
    }
  }

  return found;
}

/* ---------- Component ---------- */

export default function Extraction({ data }) {
  const { t } = useTranslation();
  const safeT = (key, fallback) => {
    const res = t(key);
    return !res || res === key ? fallback : res;
  };

  if (!data || typeof data !== "object")
    return <div className="extraction-empty">{safeT("extraction.noData", "No data to display.")}</div>;

  const parties = Array.isArray(data.parties) ? data.parties : [];

  /* ---------- Dates ---------- */
  const detectedDates = collectDates(data);
  const uniqueDates = Array.from(
    new Map(detectedDates.map((d) => [d.value, d])).values()
  );

  const renderDates = () => {
    if (!uniqueDates.length) return null;
    return (
      <section className="extraction-section">
        <h3 className="section-title">{safeT("extraction.keyDates", "Key Dates")}</h3>
        <ul className="date-list">
          {uniqueDates.map((d, idx) => {
            const parsed = d.parsedDate;
            if (!parsed) return null;
            const label = d.label || safeT("extraction.date", "Date");
            const calUrl = googleCalendarAllDayUrl({
              title: label,
              details: `${label}: ${d.value}`,
              startDateObj: parsed,
              parties,
            });
            return (
              <li key={idx} className="date-item">
                <strong>{label}:</strong> {d.value}{" "}
                <a href={calUrl} target="_blank" rel="noopener noreferrer" className="calendar-link">
                  {safeT("extraction.addToGoogleCalendar", "Add to Google Calendar")}
                </a>
              </li>
            );
          })}
        </ul>
      </section>
    );
  };

  /* ---------- Obligations ---------- */
  const renderObligations = () => {
    if (!Array.isArray(data.obligations) || !data.obligations.length) return null;

    const grouped = data.obligations.reduce((acc, o) => {
      const key = o.party || "General";
      acc[key] = acc[key] || [];
      acc[key].push(o.text);
      return acc;
    }, {});

    return (
      <section className="extraction-section">
        <h3 className="section-title">{safeT("extraction.obligations", "Obligations")}</h3>
        {Object.entries(grouped).map(([party, texts], i) => (
          <div key={i} className="obligation-group">
            <h4>{party !== "General" ? party : safeT("extraction.general", "General")}</h4>
            <ul className="obligation-list">
              {texts.map((t, idx) => (
                <li key={idx}>{t}</li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    );
  };

  /* ---------- Financials ---------- */
  const renderFinancials = () => {
    if (!Array.isArray(data.financials) || !data.financials.length) return null;
    return (
      <section className="extraction-section">
        <h3 className="section-title">{safeT("extraction.financials", "Financials")}</h3>
        {data.financials.map((f, i) => (
          <div key={i} className="financial-block">
            <div>
              <strong>{f.label || safeT("extraction.item", "Item")}:</strong>{" "}
              {f.text || `${f.currency || ""} ${f.amount || ""}`}
            </div>
            {f.schedule && (
              <div>
                <strong>{safeT("extraction.schedule", "Schedule")}:</strong> {f.schedule}
              </div>
            )}
            {Array.isArray(f.penalties) && f.penalties.length > 0 && (
              <div className="penalties">
                <strong>{safeT("extraction.penalties", "Penalties")}:</strong>
                <ul>
                  {f.penalties.map((p, idx) => (
                    <li key={idx}>
                      {p.type ? `${p.type}: ` : ""}
                      {p.text || `${p.amount || ""} ${p.rate || ""} (${p.condition || ""})`}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </section>
    );
  };

  /* ---------- Meta ---------- */
  const renderMeta = () => (
    <section className="extraction-section">
      <h3 className="section-title">{safeT("extraction.meta", "Agreement Details")}</h3>
      <div>
        <strong>{safeT("extraction.governingLaw", "Governing Law")}:</strong>{" "}
        {data.governing_law || safeT("extraction.notSpecified", "Not specified")}
      </div>
      <div>
        <strong>{safeT("extraction.autoRenewal", "Auto-Renewal")}:</strong>{" "}
        {data.auto_renewal ? safeT("extraction.yes", "Yes") : safeT("extraction.no", "No")}
      </div>
      <div>
        <strong>{safeT("extraction.signatures", "Signatures Present")}:</strong>{" "}
        {data.signatures_present ? safeT("extraction.yes", "Yes") : safeT("extraction.no", "No")}
      </div>
    </section>
  );

  /* ---------- Parties ---------- */
  const renderParties = () =>
    parties.length ? (
      <section className="extraction-section">
        <h3 className="section-title">{safeT("extraction.parties", "Parties")}</h3>
        <ul className="party-list">
          {parties.map((p, i) => (
            <li key={i}>
              {p.name}
              {p.role && <span className="party-role"> ({p.role})</span>}
            </li>
          ))}
        </ul>
      </section>
    ) : null;

  return (
    <article className="extraction-report">
      <header className="report-header">
        <h1>{safeT("extraction.reportTitle", "Contract Summary")}</h1>
       
      </header>
      {renderParties()}
      {renderDates()}
      {renderObligations()}
      {renderFinancials()}
      {renderMeta()}
       {data.raw_summary && <p className="extraction-section summary-text">{data.raw_summary}</p>}

    </article>
  );
}

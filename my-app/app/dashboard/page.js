"use client";


export default function Dashboard() {
  const data = {
    parties: [
      { name: 'Corelight Technologies, Inc. ("Supplier")', role: null },
      { name: "Blue Fin Consulting W", role: null }
    ],
    effective_date: "2025-01-01", // ISO format
    expiry_date: "2025-12-31",
    governing_law: "State of Qatar",
    obligations: [
      { text: "Supplier shall deliver a responsive website and mobile application by March 30, 2025." },
      { text: "Client shall pay a fixed fee of QAR 45,000 within 30 days of delivery; late payments accrue interest at 1.5% per month." },
      { text: "Limitation of Liability: Liability shall be limited to the total fees paid under this Agreement." },
      { text: "Confidentiality: Both parties shall keep confidential information strictly confidential." }
    ],
    financials: [
      { label: "Payment", text: "QAR 45,000" }
    ],
    signatures_present: true
  };

  // Function to open Google Calendar link for a date
  const addToGoogleCalendar = (date, title) => {
    const start = date.replaceAll("-", "") + "T090000Z";
    const end = date.replaceAll("-", "") + "T100000Z";
    const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(title)}&dates=${start}/${end}&details=${encodeURIComponent(`Contract date: ${date}`)}`;
    window.open(url, "_blank");
  };

  return (
    <div className="dashboard-form-wrapper">
      <div className="dashboard-form">
        <h1 className="form-title">Contract Analysis</h1>

        {/* Effective Date */}
        <div className="form-section">
          <label>Effective Date</label>
          <div className="date-row">
            <span className="form-value">{data.effective_date}</span>
            <button
              className="google-calendar-btn"
              onClick={() => addToGoogleCalendar(data.effective_date, "Contract Effective Date")}
            >
              Add to Google Calendar
            </button>
          </div>
        </div>

        {/* Expiry Date */}
        <div className="form-section">
          <label>Expiry Date</label>
          <div className="date-row">
            <span className="form-value">{data.expiry_date}</span>
            <button
              className="google-calendar-btn"
              onClick={() => addToGoogleCalendar(data.expiry_date, "Contract Expiry Date")}
            >
              Add to Google Calendar
            </button>
          </div>
        </div>

        {/* Parties */}
        <div className="form-section">
          <label>Parties</label>
          <ul className="form-list">
            {data.parties.map((p, i) => (
              <li key={i}>{p.name}</li>
            ))}
          </ul>
        </div>

        {/* Obligations */}
        <div className="form-section">
          <label>Obligations</label>
          <ul className="form-list">
            {data.obligations.map((o, i) => (
              <li key={i}>{o.text}</li>
            ))}
          </ul>
        </div>

        {/* Financials */}
        <div className="form-section">
          <label>Financials</label>
          <ul className="form-list">
            {data.financials.map((f, i) => (
              <li key={i}>
                <strong>{f.label}:</strong> {f.text}
              </li>
            ))}
          </ul>
        </div>

        {/* Governing Law */}
        <div className="form-section">
          <label>Governing Law</label>
          <span className="form-value">{data.governing_law}</span>
        </div>

        {/* Signatures */}
        <div className="form-section">
          <label>Signatures Present</label>
          <span className="form-value">{data.signatures_present ? "Yes" : "No"}</span>
        </div>
      </div>
    </div>
  );
}

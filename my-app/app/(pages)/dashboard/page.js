"use client";
import "../../i18n";
import { useTranslation } from "react-i18next";
import React, { useRef } from "react";
import { useEffect ,useState} from "react";
import Extraction from "../../../components/Extraction";
import RiskAnalysis from "../../../components/RiskAnalysis";
import html2pdf from "html2pdf.js";

export default function Dashboard() {

    const extractionData = localStorage.getItem("extraction");
    const extraction = extractionData ? JSON.parse(extractionData) : null;

    const riskAnalysisData = localStorage.getItem("riskAnalysis");
    const riskAnalysis = riskAnalysisData ? JSON.parse(riskAnalysisData) : null;




  if (!extraction && !riskAnalysis) return <p>Loading data...</p>;



 

  const { t, i18n } = useTranslation();
  const reportRef = useRef(null);
  const isRTL = i18n.language === "ar";

  // PDF Export
  const exportPDF = () => {
    if (!reportRef.current) return;

    const originalColor = reportRef.current.style.color;
    reportRef.current.style.color = "black";

    const opt = {
      margin: 0.5,
      filename: `Contract_Report_${new Date().toISOString().slice(0, 10)}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
    };

    html2pdf()
      .set(opt)
      .from(reportRef.current)
      .save()
      .finally(() => {
        reportRef.current.style.color = originalColor;
      });
  };

  // JSON Export
  const exportJSON = () => {
    const blob = new Blob([JSON.stringify({ data1, data2 }, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Contract_Report_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
  };

  return (
    <div
      className="all-data"
      style={{
        padding: "2rem",
        direction: isRTL ? "rtl" : "ltr",
        background:
          "linear-gradient(120deg, #0a0f29 0%, #2e006c 50%, #091131 100%)",
        color: "#fff",
        minHeight: "100vh",
        fontFamily: "Inter, sans-serif",
      }}
    >
      {/* Top Action Buttons */}
      <div
        className="export-buttons"
        style={{
          display: "flex",
          justifyContent: "flex-end",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        <button
          onClick={exportPDF}
          style={{
            background: "var(--color-primary, #6c63ff)",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            padding: "0.75rem 1.5rem",
            cursor: "pointer",
            fontWeight: 600,
            transition: "background 0.3s",
          }}
          onMouseOver={(e) => (e.target.style.background = "#5548d8")}
          onMouseOut={(e) => (e.target.style.background = "#6c63ff")}
        >
          {t("export_pdf")}
        </button>

        <button
          onClick={exportJSON}
          style={{
            background: "var(--color-secondary, #00b4d8)",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            padding: "0.75rem 1.5rem",
            cursor: "pointer",
            fontWeight: 600,
            transition: "background 0.3s",
          }}
          onMouseOver={(e) => (e.target.style.background = "#0096c7")}
          onMouseOut={(e) => (e.target.style.background = "#00b4d8")}
        >
          {t("export_json")}
        </button>
      </div>

      {/* Report Section */}
      <div ref={reportRef} className="report" style={{ background: "#111633", borderRadius: "12px", padding: "2rem" }}>
        <Extraction data={extraction} />
        <div style={{ margin: "2rem 0", height: "2px", background: "rgba(255,255,255,0.1)" }}></div>
        {/* <RiskAnalysis data={riskAnalysis} /> */}
      </div>

      {/* Footer */}
      <footer
        className="report-footer"
        style={{
          textAlign: "center",
          marginTop: "3rem",
          opacity: 0.7,
          fontSize: "0.9rem",
        }}
      >
        <small>{t("generated_by")}</small>
      </footer>
    </div>
  );
}

"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/navigation";


export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [country, setCountry] = useState("");
  const [loading, setLoading] = useState(false);

  const { t } = useTranslation();
  const router = useRouter();
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";
  const API_BASE2 = process.env.NEXT_PUBLIC_API_BASE2 ?? "http://127.0.0.1:8001";
  const maxSize = 10 * 1024 * 1024;

  const countries = [
    { code: "qatar", label: t("country.qatar", "Qatar") }, // ← FIXED: lowercase
    { code: "uk", label: t("country.uk", "UK") },
    { code: "us", label: t("country.us", "US") },
  ];

  function onChange(e) {
    setError("");
    const f = e.target.files?.[0] ?? null;
    if (!f) return setFile(null);

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    if (!allowedTypes.includes(f.type) && !/\.(pdf|doc|docx)$/i.test(f.name)) {
      setError(t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document."));
      return setFile(null);
    }
    if (f.size > maxSize) {
      setError(t("file_too_large", "File is too large. Maximum allowed size is 10 MB."));
      return setFile(null);
    }
    setFile(f);
  }

  function clear() {
    setFile(null);
    setCountry("");
    setError("");
  }

  async function analyze() {
    if (!file) return alert(t("no_file_selected"));
    if (!country) return alert(t("select_country", "Please select a country for compliance analysis."));

    setLoading(true);
    setError("");

    try {
      console.log("🚀 Starting analysis...");
      
      // 1) Upload
      console.log("📤 Uploading file...");
      const fd = new FormData();
      fd.append("file", file);
      const up = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: fd });
      if (!up.ok) throw new Error(`Upload failed: ${up.status}`);
      const { doc_id } = await up.json();
      console.log("✅ Upload successful, doc_id:", doc_id);

      // 2) Extraction
      console.log("🔍 Extracting contract data...");
      const exRes = await fetch(`${API_BASE}/api/extract`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
      });
      if (!exRes.ok) throw new Error(`Extraction failed: ${exRes.status}`);
      const extraction = await exRes.json();
            localStorage.setItem("extraction", JSON.stringify(extraction));
      console.log("✅ Extraction successful");



      // 3) Risk Analysis - FIXED: Send correct format
      console.log("⚖ Starting risk analysis...");
      const riskRes = await fetch(`${API_BASE2}/api/risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          doc_id, 
          // extraction: extraction,  // ← CRITICAL: Send extraction data
          country: country.toLowerCase() // ← CRITICAL: lowercase
        }),
      });
      if (!riskRes.ok) {
        const errorText = await riskRes.text();
        console.error("❌ Risk analysis failed:", errorText);
        throw new Error(`Risk analysis failed: ${riskRes.status} - ${errorText}`);
      }
      const riskAnalysis = await riskRes.json();
      localStorage.setItem("riskAnalysis", JSON.stringify(riskAnalysis));
      console.log("✅ Risk analysis successful:", riskAnalysis);

      // 4) Redirect to Dashboard with both JSONs
      console.log("📊 Redirecting to dashboard...");
            router.push(
        `/dashboard`
      );
    } catch (e) {
      console.error("❌ Analysis error:", e);
      setError(e.message || "Unexpected error during analysis");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="uploader-container">
      <label className="uploader-label">{t("attach_document")}</label>

      {!file && (
        <input
          type="file"
          accept={`${accept},application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document`}
          onChange={onChange}
          className="file-input"
        />
      )}

      {error && <p className="error-text">{error}</p>}

      {file && (
        <div className="file-card">
          <div className="file-info">
            <p className="file-name">{file.name}</p>
            <p className="file-size">{(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}</p>
          </div>

          <div className="country-selector">
            <label htmlFor="country">{t("select_country", "Compliance Law")}</label>
            <select
              id="country"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="country-dropdown"
            >
              <option value="">{t("select_country_placeholder", "Choose a country")}</option>
              {countries.map((c) => (
                <option key={c.code} value={c.code}>{c.label}</option>
              ))}
            </select>
          </div>

          <div className="file-actions">
            <button type="button" className="remove-btn" onClick={clear}>
              {t("remove")}
            </button>

            <motion.button
              type="button"
              className="attach-btn"
              whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              onClick={analyze}
              disabled={loading}
            >
              <span className="btn-title">
                {loading ? t("analyzing", "Analyzing...") : t("analyze")}
              </span>
            </motion.button>
          </div>
        </div>
      )}
    </div>
  );
}
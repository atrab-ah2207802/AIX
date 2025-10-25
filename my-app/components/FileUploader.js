"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [country, setCountry] = useState(""); // New state for country
  const { t } = useTranslation();

  const maxSize = 10 * 1024 * 1024; // 10 MB

  const countries = [
    { code: "QATAR", label: t("country.qatar", "Qatar") },
    { code: "UK", label: t("country.uk", "UK") },
    { code: "US", label: t("country.us", "US") },
  ];
  

  function onChange(e) {
    setError("");
    const f = e.target.files?.[0];
    if (!f) return setFile(null);

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(f.type) && !f.name.match(/\.(pdf|doc|docx)$/i)) {
      setError(t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document."));
      setFile(null);
      return;
    }

    if (f.size > maxSize) {
      setError(t("file_too_large", "File is too large. Maximum allowed size is 10 MB."));
      setFile(null);
      return;
    }

    setFile(f);
  }

  function clear() {
    setFile(null);
    setError("");
    setCountry("");
  }

  function analyze() {
    if (!file) return alert(t("no_file_selected"));
    if (!country) return alert(t("select_country", "Please select a country for compliance analysis."));

    // Example: send file and country to API
    console.log("Uploading file:", file);
    console.log("Selected country:", country);
  }

  return (
    <div className="uploader-container">
      <label className="uploader-label">{t("attach_document")}</label>

      {!file && (
        <input
          type="file"
          accept={
            accept +
            ",application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          }
          onChange={onChange}
          className="file-input"
        />
      )}

      {error && <p className="error-text">{error}</p>}

      {file && (
        <div className="file-card">
          <div className="file-info">
            <p className="file-name">{file.name}</p>
            <p className="file-size">
              {(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}
            </p>
          </div>

          {/* Country Dropdown */}
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
            >
              <span className="btn-title">{t("analyze")}</span>
            </motion.button>
          </div>
        </div>
      )}

      {!file && <p className="placeholder-text">{t("no_file_selected")}</p>}
    </div>
  );
}

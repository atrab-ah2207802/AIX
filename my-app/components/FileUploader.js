"use client";

import { useState } from "react";
import { motion } from "framer-motion";

export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const maxSize = 10 * 1024 * 1024; // 10 MB

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
      setError("Invalid file type. Please attach a PDF or Word document.");
      setFile(null);
      return;
    }

    if (f.size > maxSize) {
      setError("File is too large. Maximum allowed size is 10 MB.");
      setFile(null);
      return;
    }

    setFile(f);
  }

  function clear() {
    setFile(null);
    setError("");
  }

  return (
    <div className="uploader-container">
      <label className="uploader-label">Attach Document</label>

      {/* Show input only if no file is uploaded */}
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
            <p className="file-name dbt">{file.name}</p>
            <p className="file-size dbt">
              {(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}
            </p>
          </div>
          <div className="file-actions dbt">
            <button type="button" className="remove-btn" onClick={clear}>
              Remove
            </button>

            <motion.button
              type="button"
              className="attach-btn"
              whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
              whileTap={{ scale: 0.95 }}
              transition={{ type: "spring", stiffness: 300 }}
              onClick={() =>
                alert("No backend attached. Implement API to upload the file.")
              }
            >
              <span className="btn-title">Analyze ✨</span>
            </motion.button>
          </div>
        </div>
      )}

      {!file && (
        <p className="placeholder-text">
          No file selected. Supported: .pdf, .doc, .docx. Max 10 MB.
        </p>
      )}
    </div>
  );
}
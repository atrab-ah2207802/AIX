"use client";

import { useState } from "react";

export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const maxSize = 10 * 1024 * 1024; // 10 MB

  function onChange(e) {
    setError("");
    const f = e.target.files && e.target.files[0];
    if (!f) return setFile(null);

    // Basic client-side validation
    const allowed = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowed.includes(f.type) && !f.name.match(/\.(pdf|doc|docx)$/i)) {
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
    <div className="w-full max-w-xl rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <label className="mb-2 block text-sm font-medium text-gray-700">Attach document (PDF / Word)</label>
      <input
        type="file"
        accept={accept + ",application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        onChange={onChange}
        className="mb-3"
      />

      {error && <p className="text-sm text-red-600">{error}</p>}

      {file ? (
        <div className="mt-3 flex items-center justify-between gap-4 rounded-md bg-gray-50 p-3">
          <div>
            <p className="text-sm font-medium">{file.name}</p>
            <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB • {file.type || 'Unknown'}</p>
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={clear}
              className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
            >
              Remove
            </button>
            <button
              type="button"
              onClick={() => alert('No backend attached. Implement API to upload the file.')}
              className="rounded bg-blue-600 px-3 py-1 text-sm text-white hover:bg-blue-700"
            >
              Attach
            </button>
          </div>
        </div>
      ) : (
        <p className="text-sm text-gray-500">No file selected. Supported: .pdf, .doc, .docx. Max 10 MB.</p>
      )}
    </div>
  );
}

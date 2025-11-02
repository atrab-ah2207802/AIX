// "use client";

// import { useState } from "react";
// import { motion } from "framer-motion";
// import { useTranslation } from "react-i18next";
// import { useRouter } from "next/navigation";

// export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
//   const [file, setFile] = useState(null);
//   const [error, setError] = useState("");
//   const [country, setCountry] = useState("");
//   const [loading, setLoading] = useState(false);
//   const { t } = useTranslation();
//   const router = useRouter();

//   const maxSize = 10 * 1024 * 1024; // 10 MB

//   const countries = [
//     { code: "QATAR", label: t("country.qatar", "Qatar") },
//     { code: "UK", label: t("country.uk", "UK") },
//     { code: "US", label: t("country.us", "US") },
//   ];

//   // 🧩 API functions
//   const uploadFile = async (file) => {
//     const formData = new FormData();
//     formData.append("file", file);

//     const res = await fetch("http://localhost:8000/api/upload", {
//       method: "POST",
//       body: formData,
//     });
//     if (!res.ok) throw new Error("Upload failed");
//     return res.json(); // { doc_id, meta }
//   };

//   const extractContract = async (doc_id) => {
//     const res = await fetch("http://localhost:8000/api/extract", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
//     });
//     if (!res.ok) throw new Error("Extraction failed");
//     return res.json();
//   };

//   const analyzeRisk = async (doc_id, extraction) => {
//     const res = await fetch("http://localhost:8000/api/risk", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ doc_id, extraction, country }),
//     });
//     if (!res.ok) throw new Error("Risk analysis failed");
//     return res.json();
//   };

//   function onChange(e) {
//     setError("");
//     const f = e.target.files?.[0];
//     if (!f) return setFile(null);

//     const allowedTypes = [
//       "application/pdf",
//       "application/msword",
//       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
//     ];

//     if (!allowedTypes.includes(f.type) && !f.name.match(/\.(pdf|doc|docx)$/i)) {
//       setError(
//         t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document.")
//       );
//       setFile(null);
//       return;
//     }

//     if (f.size > maxSize) {
//       setError(
//         t("file_too_large", "File is too large. Maximum allowed size is 10 MB.")
//       );
//       setFile(null);
//       return;
//     }

//     setFile(f);
//   }

//   function clear() {
//     setFile(null);
//     setError("");
//     setCountry("");
//   }

//   async function analyze() {
//     if (!file) return alert(t("no_file_selected", "Please select a file first."));
//     if (!country)
//       return alert(t("select_country", "Please select a country for compliance analysis."));

//     try {
//       setLoading(true);

//       // Step 1: Upload
//       const upload = await uploadFile(file);
//       const doc_id = upload.doc_id;

//       // Step 2: Extraction
//       const extraction = await extractContract(doc_id);

//       // Step 3: Risk Analysis
//       const risk = await analyzeRisk(doc_id, extraction);

//       // Step 4: Redirect to dashboard with results
//       router.push(
//         `/dashboard?data1=${encodeURIComponent(
//           JSON.stringify(extraction)
//         )}&data2=${encodeURIComponent(JSON.stringify(risk))}`
//       );
//     } catch (err) {
//       console.error(err);
//       alert(t("analysis_error", `Error: ${err.message}`));
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="uploader-container">
//       <label className="uploader-label">{t("attach_document", "Attach a document")}</label>

//       {!file && (
//         <input
//           type="file"
//           accept={`${accept},application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document`}
//           onChange={onChange}
//           className="file-input"
//         />
//       )}

//       {error && <p className="error-text">{error}</p>}

//       {file && (
//         <div className="file-card">
//           <div className="file-info">
//             <p className="file-name">{file.name}</p>
//             <p className="file-size">
//               {(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}
//             </p>
//           </div>

//           <div className="country-selector">
//             <label htmlFor="country">{t("select_country", "Compliance Region")}</label>
//             <select
//               id="country"
//               value={country}
//               onChange={(e) => setCountry(e.target.value)}
//               className="country-dropdown"
//               disabled={loading}
//             >
//               <option value="">
//                 {t("select_country_placeholder", "Choose a country")}
//               </option>
//               {countries.map((c) => (
//                 <option key={c.code} value={c.code}>
//                   {c.label}
//                 </option>
//               ))}
//             </select>
//           </div>

//           <div className="file-actions">
//             <button
//               type="button"
//               className="remove-btn"
//               onClick={clear}
//               disabled={loading}
//             >
//               {t("remove", "Remove")}
//             </button>

//             <motion.button
//               type="button"
//               className="attach-btn"
//               whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
//               whileTap={{ scale: 0.95 }}
//               transition={{ type: "spring", stiffness: 300 }}
//               onClick={analyze}
//               disabled={loading}
//             >
//               <span className="btn-title">
//                 {loading ? t("processing", "Processing...") : t("analyze", "Analyze")}
//               </span>
//             </motion.button>
//           </div>
//         </div>
//       )}

//       {!file && (
//         <p className="placeholder-text">
//           {t("no_file_selected", "No file selected yet.")}
//         </p>
//       )}
//     </div>
//   );
// }













// "use client";

// import { useState } from "react";
// import { motion } from "framer-motion";
// import { useTranslation } from "react-i18next";
// import { useRouter } from "next/navigation";

// export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
//   const [file, setFile] = useState(null);
//   const [error, setError] = useState("");
//   const [country, setCountry] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [docId, setDocId] = useState("");

//   const { t } = useTranslation();
//   const router = useRouter();
//   const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";
//   const API_BASE2 = process.env.NEXT_PUBLIC_API_BASE2 ?? "http://127.0.0.1:8001";
//   const maxSize = 10 * 1024 * 1024;

//   const countries = [
//     { code: "QATAR", label: t("country.qatar", "Qatar") },
//     { code: "UK", label: t("country.uk", "UK") },
//     { code: "US", label: t("country.us", "US") },
//   ];

//   function onChange(e) {
//     setError("");
//     const f = e.target.files?.[0] ?? null;
//     if (!f) return setFile(null);

//     const allowedTypes = [
//       "application/pdf",
//       "application/msword",
//       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
//     ];
//     if (!allowedTypes.includes(f.type) && !/\.(pdf|doc|docx)$/i.test(f.name)) {
//       setError(t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document."));
//       return setFile(null);
//     }
//     if (f.size > maxSize) {
//       setError(t("file_too_large", "File is too large. Maximum allowed size is 10 MB."));
//       return setFile(null);
//     }
//     setFile(f);
//   }

//   function clear() {
//     setFile(null);
//     setCountry("");
//     setDocId("");
//     setError("");
//   }

//   async function analyze() {
//     if (!file) return alert(t("no_file_selected"));
//     if (!country) return alert(t("select_country", "Please select a country for compliance analysis."));

//     setLoading(true);
//     setError("");

//     try {
//       // 1) Upload
//       const fd = new FormData();
//       fd.append("file", file);
//       const up = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: fd });
//       if (!up.ok) throw new Error(`Upload failed: ${up.status}`);
//       const { doc_id } = await up.json();
//       setDocId(doc_id);

//       // 2) Extraction
//       const exRes = await fetch(`${API_BASE}/api/extract`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
//       });
//       if (!exRes.ok) throw new Error(`Extraction failed: ${exRes.status}`);
//       const extraction = await exRes.json();

//       // 3) Risk Analysis
//       const riskRes = await fetch(`${API_BASE2}/api/risk`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
//       });
//       if (!riskRes.ok) throw new Error(`Risk analysis failed: ${riskRes.status}`);
//       const riskAnalysis = await riskRes.json();
      

//       // 4) Redirect to Dashboard with both JSONs
//       router.push({
//         pathname: "/dashboard",
//         query: {
//           data1: encodeURIComponent(JSON.stringify(extraction)),
//           data2: encodeURIComponent(JSON.stringify(riskAnalysis)),
//         },
//       });
//     } catch (e) {
//       console.error(e);
//       setError(e.message || "Unexpected error");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="uploader-container">
//       <label className="uploader-label">{t("attach_document")}</label>

//       {!file && (
//         <input
//           type="file"
//           accept={`${accept},application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document`}
//           onChange={onChange}
//           className="file-input"
//         />
//       )}

//       {error && <p className="error-text">{error}</p>}

//       {file && (
//         <div className="file-card">
//           <div className="file-info">
//             <p className="file-name">{file.name}</p>
//             <p className="file-size">{(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}</p>
//           </div>

//           <div className="country-selector">
//             <label htmlFor="country">{t("select_country", "Compliance Law")}</label>
//             <select
//               id="country"
//               value={country}
//               onChange={(e) => setCountry(e.target.value)}
//               className="country-dropdown"
//             >
//               <option value="">{t("select_country_placeholder", "Choose a country")}</option>
//               {countries.map((c) => (
//                 <option key={c.code} value={c.code}>{c.label}</option>
//               ))}
//             </select>
//           </div>

//           <div className="file-actions">
//             <button type="button" className="remove-btn" onClick={clear}>
//               {t("remove")}
//             </button>

//             <motion.button
//               type="button"
//               className="attach-btn"
//               whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
//               whileTap={{ scale: 0.95 }}
//               transition={{ type: "spring", stiffness: 300 }}
//               onClick={analyze}
//               disabled={loading}
//             >
//               <span className="btn-title">
//                 {loading ? t("analyzing", "Analyzing...") : t("analyze")}
//               </span>
//             </motion.button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }










// "use client";

// import { useState } from "react";
// import { motion } from "framer-motion";
// import { useTranslation } from "react-i18next";
// import { useRouter } from "next/navigation";

// export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
//   const [file, setFile] = useState(null);
//   const [error, setError] = useState("");
//   const [country, setCountry] = useState("");
//   const [loading, setLoading] = useState(false);

//   const { t } = useTranslation();
//   const router = useRouter();
//   const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";
//   const API_BASE2 = process.env.NEXT_PUBLIC_API_BASE2 ?? "http://127.0.0.1:8001";
//   const maxSize = 10 * 1024 * 1024;

//   const countries = [
//     { code: "QATAR", label: t("country.qatar", "Qatar") },
//     { code: "UK", label: t("country.uk", "UK") },
//     { code: "US", label: t("country.us", "US") },
//   ];

//   function onChange(e) {
//     setError("");
//     const f = e.target.files?.[0] ?? null;
//     if (!f) return setFile(null);

//     const allowedTypes = [
//       "application/pdf",
//       "application/msword",
//       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
//     ];
//     if (!allowedTypes.includes(f.type) && !/\.(pdf|doc|docx)$/i.test(f.name)) {
//       setError(t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document."));
//       return setFile(null);
//     }
//     if (f.size > maxSize) {
//       setError(t("file_too_large", "File is too large. Maximum allowed size is 10 MB."));
//       return setFile(null);
//     }
//     setFile(f);
//   }

//   function clear() {
//     setFile(null);
//     setCountry("");
//     setError("");
//   }

//   async function analyze() {
//     if (!file) return alert(t("no_file_selected"));
//     if (!country) return alert(t("select_country", "Please select a country for compliance analysis."));

//     setLoading(true);
//     setError("");

//     try {
//       // 1) Upload
//       const fd = new FormData();
//       fd.append("file", file);
//       const up = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: fd });
//       if (!up.ok) throw new Error(`Upload failed: ${up.status}`);
//       const { doc_id } = await up.json();

//       // 2) Extraction
//       const exRes = await fetch(`${API_BASE}/api/extract`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
//       });
//       if (!exRes.ok) throw new Error(`Extraction failed: ${exRes.status}`);
//       const extraction = await exRes.json();

//       // 3) Risk Analysis (send country)
//       const riskRes = await fetch(`${API_BASE2}/api/risk`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ doc_id, country, use_llm: true, fallback_rules: true }),
//       });
//       if (!riskRes.ok) throw new Error(`Risk analysis failed: ${riskRes.status}`);
//       const riskAnalysis = await riskRes.json();

//       // 4) Redirect to Dashboard with both JSONs
//       router.push({
//         pathname: "/dashboard",
//         query: {
//           data1: encodeURIComponent(JSON.stringify(extraction)),
//           data2: encodeURIComponent(JSON.stringify(riskAnalysis)),
//         },
//       });
//     } catch (e) {
//       console.error(e);
//       setError(e.message || "Unexpected error");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="uploader-container">
//       <label className="uploader-label">{t("attach_document")}</label>

//       {!file && (
//         <input
//           type="file"
//           accept={`${accept},application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document`}
//           onChange={onChange}
//           className="file-input"
//         />
//       )}

//       {error && <p className="error-text">{error}</p>}

//       {file && (
//         <div className="file-card">
//           <div className="file-info">
//             <p className="file-name">{file.name}</p>
//             <p className="file-size">{(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}</p>
//           </div>

//           <div className="country-selector">
//             <label htmlFor="country">{t("select_country", "Compliance Law")}</label>
//             <select
//               id="country"
//               value={country}
//               onChange={(e) => setCountry(e.target.value)}
//               className="country-dropdown"
//             >
//               <option value="">{t("select_country_placeholder", "Choose a country")}</option>
//               {countries.map((c) => (
//                 <option key={c.code} value={c.code}>{c.label}</option>
//               ))}
//             </select>
//           </div>

//           <div className="file-actions">
//             <button type="button" className="remove-btn" onClick={clear}>
//               {t("remove")}
//             </button>

//             <motion.button
//               type="button"
//               className="attach-btn"
//               whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
//               whileTap={{ scale: 0.95 }}
//               transition={{ type: "spring", stiffness: 300 }}
//               onClick={analyze}
//               disabled={loading}
//             >
//               <span className="btn-title">
//                 {loading ? t("analyzing", "Analyzing...") : t("analyze")}
//               </span>
//             </motion.button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }


























// "use client";

// import { useState } from "react";
// import { motion } from "framer-motion";
// import { useTranslation } from "react-i18next";
// import { useRouter } from "next/navigation";

// export default function FileUploader({ accept = ".pdf,.doc,.docx" }) {
//   const [file, setFile] = useState(null);
//   const [error, setError] = useState("");
//   const [country, setCountry] = useState("");
//   const [loading, setLoading] = useState(false);

//   const { t } = useTranslation();
//   const router = useRouter();
//   const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000";
//   const API_BASE2 = process.env.NEXT_PUBLIC_API_BASE2 ?? "http://127.0.0.1:8001"; // Risk server
//   const maxSize = 10 * 1024 * 1024;

//   const countries = [
//     { code: "qatar", label: t("country.qatar", "Qatar") }, // ← FIXED: lowercase
//     { code: "uk", label: t("country.uk", "UK") },
//     { code: "us", label: t("country.us", "US") },
//   ];

//   function onChange(e) {
//     setError("");
//     const f = e.target.files?.[0] ?? null;
//     if (!f) return setFile(null);

//     const allowedTypes = [
//       "application/pdf",
//       "application/msword",
//       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
//     ];
//     if (!allowedTypes.includes(f.type) && !/\.(pdf|doc|docx)$/i.test(f.name)) {
//       setError(t("invalid_file_type", "Invalid file type. Please attach a PDF or Word document."));
//       return setFile(null);
//     }
//     if (f.size > maxSize) {
//       setError(t("file_too_large", "File is too large. Maximum allowed size is 10 MB."));
//       return setFile(null);
//     }
//     setFile(f);
//   }

//   function clear() {
//     setFile(null);
//     setCountry("");
//     setError("");
//   }

//   async function analyze() {
//     if (!file) return alert(t("no_file_selected"));
//     if (!country) return alert(t("select_country", "Please select a country for compliance analysis."));

//     setLoading(true);
//     setError("");

//     try {
//       // 1) Upload
//       const fd = new FormData();
//       fd.append("file", file);
//       const up = await fetch(`${API_BASE}/api/upload`, { method: "POST", body: fd });
//       if (!up.ok) throw new Error(`Upload failed: ${up.status}`);
//       const { doc_id } = await up.json();

//       // 2) Extraction
//       const exRes = await fetch(`${API_BASE}/api/extract`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ doc_id, use_llm: true, fallback_rules: true }),
//       });
//       if (!exRes.ok) throw new Error(`Extraction failed: ${exRes.status}`);
//       const extraction = await exRes.json();

//       // 3) Risk Analysis - FIXED: Send correct format
//       const riskRes = await fetch(`${API_BASE2}/api/risk`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ 
//           doc_id, 
//           extraction: extraction,  // ← CRITICAL: Send extraction data
//           country: country.toLowerCase() // ← CRITICAL: lowercase
//         }),
//       });
      
//       if (!riskRes.ok) {
//         const errorText = await riskRes.text();
//         throw new Error(`Risk analysis failed: ${riskRes.status} - ${errorText}`);
//       }
      
//       const riskAnalysis = await riskRes.json();

//       console.log("✅ Risk analysis received:", riskAnalysis);

//       // 4) Redirect to Dashboard with both JSONs
//       router.push({
//         pathname: "/dashboard",
//         query: {
//           data1: encodeURIComponent(JSON.stringify(extraction)),
//           data2: encodeURIComponent(JSON.stringify(riskAnalysis)),
//         },
//       });
//     } catch (e) {
//       console.error("Analysis error:", e);
//       setError(e.message || "Unexpected error during analysis");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="uploader-container">
//       <label className="uploader-label">{t("attach_document")}</label>

//       {!file && (
//         <input
//           type="file"
//           accept={`${accept},application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document`}
//           onChange={onChange}
//           className="file-input"
//         />
//       )}

//       {error && <p className="error-text">{error}</p>}

//       {file && (
//         <div className="file-card">
//           <div className="file-info">
//             <p className="file-name">{file.name}</p>
//             <p className="file-size">{(file.size / 1024).toFixed(2)} KB • {file.type || "Unknown"}</p>
//           </div>

//           <div className="country-selector">
//             <label htmlFor="country">{t("select_country", "Compliance Law")}</label>
//             <select
//               id="country"
//               value={country}
//               onChange={(e) => setCountry(e.target.value)}
//               className="country-dropdown"
//             >
//               <option value="">{t("select_country_placeholder", "Choose a country")}</option>
//               {countries.map((c) => (
//                 <option key={c.code} value={c.code}>{c.label}</option>
//               ))}
//             </select>
//           </div>

//           <div className="file-actions">
//             <button type="button" className="remove-btn" onClick={clear}>
//               {t("remove")}
//             </button>

//             <motion.button
//               type="button"
//               className="attach-btn"
//               whileHover={{ scale: 1.05, boxShadow: "0px 5px 15px rgba(63, 43, 100, 0.4)" }}
//               whileTap={{ scale: 0.95 }}
//               transition={{ type: "spring", stiffness: 300 }}
//               onClick={analyze}
//               disabled={loading}
//             >
//               <span className="btn-title">
//                 {loading ? t("analyzing", "Analyzing...") : t("analyze")}
//               </span>
//             </motion.button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }



















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
      console.log("✅ Extraction successful");

      // 3) Risk Analysis - FIXED: Send correct format
      console.log("⚖ Starting risk analysis...");
      const riskRes = await fetch(`${API_BASE2}/api/risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          doc_id, 
          extraction: extraction,  // ← CRITICAL: Send extraction data
          country: country.toLowerCase() // ← CRITICAL: lowercase
        }),
      });
      
      if (!riskRes.ok) {
        const errorText = await riskRes.text();
        console.error("❌ Risk analysis failed:", errorText);
        throw new Error(`Risk analysis failed: ${riskRes.status} - ${errorText}`);
      }
      
      const riskAnalysis = await riskRes.json();
      console.log("✅ Risk analysis successful:", riskAnalysis);

      // 4) Redirect to Dashboard with both JSONs
      console.log("📊 Redirecting to dashboard...");
      router.push({
        pathname: "/dashboard",
        query: {
          data1: encodeURIComponent(JSON.stringify(extraction)),
          data2: encodeURIComponent(JSON.stringify(riskAnalysis)),
        },
      });
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
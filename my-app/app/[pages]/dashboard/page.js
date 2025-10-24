"use client";

import { useEffect, useState } from "react";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/data/analysis.json")
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => console.error(err));
  }, []);

  if (!data) return <p className="loading-text">Loading analysis...</p>;

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Contract Analysis</h1>

      <div className="dashboard-section">
        <h2 className="section-title">Contract Info</h2>
        <p><strong>Title:</strong> {data.contractTitle}</p>
        <p><strong>Client:</strong> {data.clientName}</p>
        <p><strong>Risk Score:</strong> {data.riskScore}%</p>
      </div>

      <div className="dashboard-section">
        <h2 className="section-title">Clauses</h2>
        <ul className="clauses-list">
          {data.clauses.map((clause, index) => (
            <li key={index} className={`clause ${clause.status.toLowerCase()}`}>
              {clause.name}: {clause.status}
            </li>
          ))}
        </ul>
      </div>

      <div className="dashboard-section">
        <h2 className="section-title">Summary</h2>
        <p>{data.summary}</p>
      </div>
    </div>
  );
}

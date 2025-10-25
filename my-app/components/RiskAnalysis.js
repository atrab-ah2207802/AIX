"use client";

import React from "react";

export default function RiskAnalysis({ data }) {
  if (!data) return null;

  const severityClasses = {
    critical: "flag-critical",
    high: "flag-high",
    medium: "flag-medium",
    low: "flag-low",
  };

  const complianceSeverityClasses = {
    non_compliant: "compliance-non-compliant",
    compliant: "compliance-compliant",
    unknown: "compliance-unknown",
  };

  return (
    <div><h1>Risk analysis</h1>
    <div className="risk-analysis-container">
        
    <div className="overall-score">
      Overall Score: <span className="score-value">{data.overall_score}</span>
    </div>
    <div className="risk-summary">{data.summary}</div>

    <div className="flags-list">
      {data.flags?.map((flag, idx) => (
        <div
          key={idx}
          className={`flag-item ${severityClasses[flag.severity] || "flag-medium"}`}
        >
          <div className="flag-title">{flag.title || "No Title"}</div>
          {flag.description && <div className="flag-description">{flag.description}</div>}
          {flag.recommendation && <div className="flag-recommendation"><strong>Recommendation:</strong> {flag.recommendation}</div>}
          {flag.clause_reference && <div className="flag-clause"><strong>Clause:</strong> {flag.clause_reference}</div>}
          {flag.confidence != null && <div className="flag-confidence"><strong>Confidence:</strong> {(flag.confidence*100).toFixed(1)}%</div>}
        </div>
      ))}
    </div>

    {data.recommendations?.length > 0 && (
      <div className="risk-recommendations">
        <h3>Recommendations</h3>
        <ul>
          {data.recommendations.map((rec, idx) => (
            <li key={idx}>{rec}</li>
          ))}
        </ul>
      </div>
    )}

        {/* Term Consistency */}
        {Array.isArray(data.term_consistency) && data.term_consistency.length > 0 && (
  <div className="extraction-section term-consistency">
    <h2>Term Consistency</h2>
    <div className="term-list">
      {data.term_consistency.map((term, idx) => (
        <div key={idx} className="term-card">
          <div className="term-header">
            <span className="term-name">{term.term}</span>
            <span className={`term-badge ${term.is_consistent ? "consistent" : "inconsistent"}`}>
              {term.is_consistent ? "Consistent" : "Inconsistent"}
            </span>
          </div>
          {term.issue_description && (
            <div className="term-issue">{term.issue_description}</div>
          )}
        </div>
      ))}
    </div>
  </div>
)}


      {/* Clause Comparisons */}
      {Array.isArray(data.clause_comparisons) && data.clause_comparisons.length > 0 && (
  <div className="extraction-section clause-comparisons">
    <h2>Clause Comparisons</h2>
    <div className="clause-list">
      {data.clause_comparisons.map((clause, idx) => (
        <div key={idx} className={`clause-card clause-${clause.deviation_severity ?? "medium"}`}>
          <div className="clause-header">
            <span className="clause-type">{clause.clause_type}</span>
            <span className={`clause-badge clause-${clause.deviation_severity ?? "medium"}`}>
              {clause.deviation_severity ?? "Unknown"}
            </span>
          </div>
          <div className="clause-explanation">{clause.explanation}</div>
        </div>
      ))}
    </div>
  </div>
)}


      {/* Legal Advice */}
      {Array.isArray(data.legal_advice) && data.legal_advice.length > 0 && (
  <div className="extraction-section legal-advice">
    <h2>Legal Advice</h2>
    <div className="advice-list">
      {data.legal_advice.map((advice, idx) => (
        <div key={idx} className={`advice-card advice-${advice.risk_level ?? "medium"}`}>
          <div className="advice-header">
            <span className="advice-topic">{advice.topic}</span>
            {advice.risk_level && (
              <span className={`advice-badge advice-${advice.risk_level.toLowerCase()}`}>
                {advice.risk_level}
              </span>
            )}
          </div>
          <div className="advice-text">{advice.advice}</div>
          {Array.isArray(advice.recommendations) && advice.recommendations.length > 0 && (
            <div className="advice-recommendations">
              <strong>Recommendations:</strong>
              <ul>
                {advice.recommendations.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
)}

    </div>
    <div className="legal-compliance-section">
  <h1>Legal Compliance</h1>

  {data.legal_compliance && (
    <div className="extraction-section legal-compliance">

      {/* Overall Compliance Summary */}
      <div className="compliance-summary">
        <div>
          <strong>Overall Compliance Score:</strong>{" "}
          <span className="score-value">
            {data.legal_compliance.compliance_summary.overall_compliance_score}%
          </span>
        </div>
        <div>
          <strong>Status:</strong>{" "}
          <span
            className={`compliance-status ${
              complianceSeverityClasses[
                data.legal_compliance.compliance_summary.status
              ] || "compliance-unknown"
            }`}
          >
            {data.legal_compliance.compliance_summary.status.replace("_", " ")}
          </span>
        </div>
        <div>
          <strong>Total Laws Analyzed:</strong>{" "}
          {data.legal_compliance.compliance_summary.total_laws_analyzed}
        </div>
        <div>
          <strong>Compliant Laws:</strong>{" "}
          {data.legal_compliance.compliance_summary.compliant_laws}
        </div>
        <div>
          <strong>Non-Compliant Laws:</strong>{" "}
          {data.legal_compliance.compliance_summary.non_compliant_laws}
        </div>
        <div>
          <strong>Critical Violations:</strong>{" "}
          {data.legal_compliance.compliance_summary.critical_violations_count}
        </div>
      </div>

      {/* Law Analysis */}
      <div className="law-analysis">
        {data.legal_compliance.law_analysis.map((law, idx) => (
          <div key={idx} className="law-card">
            <h4 className="law-title">{law.law}</h4>
            <div className={`law-status ${complianceSeverityClasses[law.compliance_status]}`}>
              Status: {law.compliance_status.replace("_", " ")}
            </div>
            <div>Compliance Score: {law.compliance_score}%</div>
            {law.recommendations.length > 0 && (
              <div className="law-recommendations">
                <strong>Recommendations:</strong>
                <ul>
                  {law.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
            {law.severity && (
              <div className={`law-severity law-${law.severity}`}>
                Severity: {law.severity}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )}
</div>

    </div>
  );
}

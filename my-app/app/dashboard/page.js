"use client";
import "../i18n";
import { useTranslation } from "react-i18next";
import React, { useRef } from "react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation"; 
import Extraction from "../../components/Extraction";
import RiskAnalysis from "../../components/RiskAnalysis";
import html2pdf from "html2pdf.js";

export default function Dashboard() {
  // const searchParams = useSearchParams();
  // const [extractionData, setExtractionData] = useState(null);
  // const [riskData, setRiskData] = useState(null);

  // useEffect(() => {
  //   const data1 = searchParams.get("data1");
  //   const data2 = searchParams.get("data2");

  //   if (data1) {
  //     try {
  //       setExtractionData(JSON.parse(decodeURIComponent(data1)));
  //     } catch (err) {
  //       console.error("Failed to parse extraction data:", err);
  //     }
  //   }

  //   if (data2) {
  //     try {
  //       setRiskData(JSON.parse(decodeURIComponent(data2)));
  //     } catch (err) {
  //       console.error("Failed to parse risk analysis data:", err);
  //     }
  //   }
  // }, [searchParams]);

  // if (!extractionData && !riskData) return <p>Loading data...</p>;

 const data1={
    "parties": [
      {
        "name": "Corelight Technologies, Inc. (\"Supplier\")",
        "role": null
      },
      {
        "name": "Blue Fin Consulting W",
        "role": null
      }
    ],
    "effective_date": "01 Jan 2025",
    "expiry_date": "31 Dec 2025",
    "renewal_date": null,
    "auto_renewal": true,
    "renewals": null,
    "governing_law": "State of Qatar",
    "jurisdiction": null,
    "obligations": [
      {
        "party": "Supplier",
        "text": "Supplier shall deliver a responsive website and mobile application by March 30, 2025."
      },
      {
        "party": "Client",
        "text": "Client shall pay a fixed fee of QAR 45,000 within 30 days of delivery; late payments accrue interest at 1.5% per month."
      },
      {
        "party": null,
        "text": "Limitation of Liability: Liability shall be limited to the total fees paid under this Agreement."
      },
      {
        "party": null,
        "text": "Confidentiality: Both parties shall keep confidential information strictly confidential."
      }
    ],
    "financials": [
      {
        "label": "Payment",
        "amount": "45,000",
        "currency": "QAR",
        "schedule": "within 30 days",
        "penalties": [
          {
            "type": "late/interest",
            "amount": "45,000",
            "rate": "1.5% per month",
            "condition": "late payment",
            "text": "ier shall deliver a responsive website and mobile application by March 30, 2025. Client shall pay a fixed fee of QAR 45,000 within 30 days of delivery; late payments accrue interest at 1.5% per month. Limitation of Liability: Liability shall be limited to the total fees paid under this Agreement. Confidentiality: Both parties shall ke"
          }
        ],
        "text": "QAR 45,000"
      }
    ],
    "signatures_present": true,
    "raw_summary": "Here's a concise summary of the Software Development Agreement:\n\n*   *Purpose:* Supplier (Corelight Technologies) will develop a responsive website and mobile application for Client (Blue Fin Consulting).\n*   *Deliverables & Key Dates:* Website and mobile application delivery by March 30, 2025. The agreement is effective January 1, 2025, expires December 31, 2025, and auto-renews annually unless canceled with 60 days' notice.\n*   *Payment:* Client pays a fixed fee of QAR 45,000 within 30 days of delivery, with 1.5% monthly interest on late payments.\n*   *Governing Law:* The agreement is governed by the laws of the State of Qatar."
  }
  const data2= {
    "overall_score": 71,
    "risk_level": "low",
    "summary": "Low risk: 4 minor deviations from company standards",
    "flags": [
      {
        "severity": "high",
        "category": "non_standard",
        "title": "Significant Deviation in Limitation of Liability Clause",
        "description": "The contract clause only caps direct damages at total fees paid, omitting the exclusion of indirect, special, incidental, consequential, punitive, or exemplary damages, and loss of profits, revenue, data, goodwill, or use. This significantly broadens potential liability.; The contract clause lacks a specific minimum cap (e.g., $100 in the standard), which could be problematic if total fees paid are very low or zero.; The contract clause fails to explicitly state that the limitations form an essential basis of the bargain and reflect an allocation of risk, which is a common and important contractual element.; The contract clause does not explicitly carve out exceptions for gross negligence, willful misconduct, or breach of confidentiality as per the company standard. It also doesn't explicitly preserve liability for death or personal injury caused by negligence, fraud, or other non-excludable liabilities.",
        "recommendation": "The contract clause must be revised to include the standard exclusion of indirect/consequential damages, establish a minimum cap on liability (e.g., $100 or a more appropriate amount), explicitly state that these limitations are an essential basis of the bargain, and clearly carve out exceptions for gross negligence, willful misconduct, breach of confidentiality, and non-excludable liabilities such as death or personal injury caused by negligence.",
        "clause_reference": "limitation_of_liability Section",
        "confidence": 0.4
      },
      {
        "severity": "medium",
        "category": "non_standard",
        "title": "Non-Standard Payment Terms",
        "description": "",
        "recommendation": "",
        "clause_reference": "payment_terms Section",
        "confidence": 1.0
      },
      {
        "severity": "high",
        "category": "missing_clause",
        "title": "Missing Indemnification Clause",
        "description": "Standard indemnification clause not found (appeared in 2 company contracts)",
        "recommendation": "Add comprehensive indemnification clause matching company standards",
        "clause_reference": "indemnification Section",
        "confidence": 0.4
      },
      {
        "severity": "high",
        "category": "missing_clause",
        "title": "Missing Dispute Resolution Clause",
        "description": "Standard dispute_resolution clause not found (appeared in 3 company contracts)",
        "recommendation": "Add comprehensive dispute_resolution clause matching company standards",
        "clause_reference": "dispute_resolution Section",
        "confidence": 0.6
      }
    ],
    "recommendations": [
      "The contract clause must be revised to include the standard exclusion of indirect/consequential damages, establish a minimum cap on liability (e.g., $100 or a more appropriate amount), explicitly state that these limitations are an essential basis of the bargain, and clearly carve out exceptions for gross negligence, willful misconduct, breach of confidentiality, and non-excludable liabilities such as death or personal injury caused by negligence.",
      "Add comprehensive indemnification clause matching company standards",
      "Add comprehensive dispute_resolution clause matching company standards"
    ],
    "term_consistency": [
      {
        "term": "Confidential",
        "definitions": [
          "References to confidential found in contract"
        ],
        "is_consistent": true,
        "issue_description": null
      },
      {
        "term": "Termination",
        "definitions": [
          "References to termination found in contract"
        ],
        "is_consistent": true,
        "issue_description": null
      },
      {
        "term": "Liability",
        "definitions": [
          "References to liability found in contract"
        ],
        "is_consistent": true,
        "issue_description": null
      },
      {
        "term": "Payment",
        "definitions": [
          "References to payment found in contract"
        ],
        "is_consistent": true,
        "issue_description": null
      },
      {
        "term": "Warrant",
        "definitions": [
          "References to warrant found in contract"
        ],
        "is_consistent": true,
        "issue_description": null
      }
    ],
    "clause_comparisons": [
      {
        "clause_type": "liability",
        "standard_version": "Company standard liability clause",
        "contract_version": "The contract clause only caps direct damages at total fees paid, omitting the exclusion of indirect, special, incidental, consequential, punitive, or exemplary damages, and loss of profits, revenue, d...",
        "deviation_severity": "high",
        "explanation": "The contract clause only caps direct damages at total fees paid, omitting the exclusion of indirect, special, incidental, consequential, punitive, or exemplary damages, and loss of profits, revenue, data, goodwill, or use. This significantly broadens potential liability.; The contract clause lacks a specific minimum cap (e.g., $100 in the standard), which could be problematic if total fees paid are very low or zero.; The contract clause fails to explicitly state that the limitations form an essential basis of the bargain and reflect an allocation of risk, which is a common and important contractual element.; The contract clause does not explicitly carve out exceptions for gross negligence, willful misconduct, or breach of confidentiality as per the company standard. It also doesn't explicitly preserve liability for death or personal injury caused by negligence, fraud, or other non-excludable liabilities."
      },
      {
        "clause_type": "payment",
        "standard_version": "Company standard payment clause",
        "contract_version": "...",
        "deviation_severity": "medium",
        "explanation": ""
      },
      {
        "clause_type": "indemnification",
        "standard_version": "Company standard indemnification clause",
        "contract_version": "Standard indemnification clause not found (appeared in 2 company contracts)...",
        "deviation_severity": "high",
        "explanation": "Standard indemnification clause not found (appeared in 2 company contracts)"
      },
      {
        "clause_type": "dispute_resolution",
        "standard_version": "Company standard dispute_resolution clause",
        "contract_version": "Standard dispute_resolution clause not found (appeared in 3 company contracts)...",
        "deviation_severity": "high",
        "explanation": "Standard dispute_resolution clause not found (appeared in 3 company contracts)"
      }
    ],
    "legal_advice": [
      {
        "topic": "Significant Deviation in Limitation of Liability Clause",
        "advice": "This clause poses significant legal risk that should be addressed. The contract clause only caps direct damages at total fees paid, omitting the exclusion of indirect, special, incidental, consequential, punitive, or exemplary damages, and loss of profits, revenue, data, goodwill, or use. This significantly broadens potential liability.; The contract clause lacks a specific minimum cap (e.g., $100 in the standard), which could be problematic if total fees paid are very low or zero.; The contract clause fails to explicitly state that the limitations form an essential basis of the bargain and reflect an allocation of risk, which is a common and important contractual element.; The contract clause does not explicitly carve out exceptions for gross negligence, willful misconduct, or breach of confidentiality as per the company standard. It also doesn't explicitly preserve liability for death or personal injury caused by negligence, fraud, or other non-excludable liabilities.",
        "risk_level": "high",
        "supporting_law": "General Contract Law Principles",
        "recommendations": [
          "The contract clause must be revised to include the standard exclusion of indirect/consequential damages, establish a minimum cap on liability (e.g., $100 or a more appropriate amount), explicitly state that these limitations are an essential basis of the bargain, and clearly carve out exceptions for gross negligence, willful misconduct, breach of confidentiality, and non-excludable liabilities such as death or personal injury caused by negligence."
        ]
      },
      {
        "topic": "Missing Indemnification Clause",
        "advice": "This clause poses significant legal risk that should be addressed. Standard indemnification clause not found (appeared in 2 company contracts)",
        "risk_level": "high",
        "supporting_law": "General Contract Law Principles",
        "recommendations": [
          "Add comprehensive indemnification clause matching company standards"
        ]
      },
      {
        "topic": "Missing Dispute Resolution Clause",
        "advice": "This clause poses significant legal risk that should be addressed. Standard dispute_resolution clause not found (appeared in 3 company contracts)",
        "risk_level": "high",
        "supporting_law": "General Contract Law Principles",
        "recommendations": [
          "Add comprehensive dispute_resolution clause matching company standards"
        ]
      }
    ],
    "analyzed_at": "2025-10-25T22:32:55.761826",
    "contract_metadata": {
      "contract_name": "analyzed_contract.docx",
      "parties": [
        {
          "name": "QDB",
          "role": "Client"
        },
        {
          "name": "Vendor Inc",
          "role": "Supplier"
        }
      ],
      "effective_date": "2025-01-01",
      "expiry_date": "2025-12-31",
      "total_value": "QAR 500000",
      "extracted_clauses_count": 1
    },
    "legal_compliance": {
      "contract_id": "TEST_001",
      "jurisdiction": "QATAR",
      "analyzed_at": "2025-10-25T22:33:19.130865",
      "compliance_summary": {
        "overall_compliance_score": 50,
        "status": "non_compliant",
        "total_laws_analyzed": 4,
        "compliant_laws": 0,
        "non_compliant_laws": 0,
        "critical_violations_count": 0
      },
      "law_analysis": [
        {
          "law": "Qatar Civil Code - Contracts",
          "compliance_status": "unknown",
          "compliance_score": 50,
          "specific_articles_violated": [],
          "compliance_issues": [],
          "legal_risks": [],
          "recommendations": [
            "Revise Article 4 to limit late payment interest to a maximum of 9% per annum, as mandated by Article 220 of the Qatar Civil Code.",
            "Revise Article 8 to explicitly state that all intellectual property rights for the developed website and mobile application vest with the Client upon full payment, in accordance with the principles of Article 210.",
            "Review Article 5 to ensure that the broad limitation of liability does not attempt to exclude or limit liability in circumstances prohibited by Article 190 (e.g., fraud, gross negligence). Consider adding carve-outs for these specific exceptions."
          ],
          "severity": "medium",
          "missing_required_clauses": []
        },
        {
          "law": "Qatar Commercial Companies Law",
          "compliance_status": "unknown",
          "compliance_score": 50,
          "specific_articles_violated": [],
          "compliance_issues": [],
          "legal_risks": [],
          "recommendations": [],
          "severity": "medium",
          "missing_required_clauses": []
        },
        {
          "law": "Qatar Data Protection Regulations",
          "compliance_status": "unknown",
          "compliance_score": 50,
          "specific_articles_violated": [],
          "compliance_issues": [],
          "legal_risks": [],
          "recommendations": [],
          "severity": "medium",
          "missing_required_clauses": []
        },
        {
          "law": "Specific Regulations",
          "compliance_status": "unknown",
          "compliance_score": 50,
          "specific_articles_violated": [],
          "compliance_issues": [],
          "legal_risks": [],
          "recommendations": [],
          "severity": "medium",
          "missing_required_clauses": []
        }
      ],
      "legal_risks": [],
      "recommendations": [
        "Revise Article 4 to limit late payment interest to a maximum of 9% per annum, as mandated by Article 220 of the Qatar Civil Code.",
        "Revise Article 8 to explicitly state that all intellectual property rights for the developed website and mobile application vest with the Client upon full payment, in accordance with the principles of Article 210.",
        "Review Article 5 to ensure that the broad limitation of liability does not attempt to exclude or limit liability in circumstances prohibited by Article 190 (e.g., fraud, gross negligence). Consider adding carve-outs for these specific exceptions."
      ],
      "critical_violations": [],
      "metadata": {
        "total_laws_available": 4,
        "total_laws_analyzed": 4,
        "analysis_method": "Gemini AI Legal Analysis",
        "legal_database_used": true
      }
    }
  }

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
      <div ref={reportRef} style={{ background: "#111633", borderRadius: "12px", padding: "2rem" }}>
        <Extraction data={data1} />
        <div style={{ margin: "2rem 0", height: "2px", background: "rgba(255,255,255,0.1)" }}></div>
        <RiskAnalysis data={data2} />
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

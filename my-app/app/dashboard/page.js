"use client";

import React, { useRef } from "react";
import Extraction from "@/components/Extraction";
import RiskAnalysis from "@/components/RiskAnalysis";

export default function Dashboard() {

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
    "overall_score": 65,
    "risk_level": "medium",
    "summary": "Moderate risk: 3 deviations from company standards found",
    "flags": [
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
        "severity": "critical",
        "category": "non_standard",
        "title": "Non-Standard Warranties",
        "description": "The contract clause completely disclaims all warranties, whereas the company standard includes detailed express warranties regarding development quality, defect-free software, conformance to specifications, and non-infringement.; The company standard explicitly disclaims implied warranties of merchantability and fitness for a particular purpose, but the contract clause's \"as is\" provision is a much broader and more aggressive disclaimer that negates even basic expectations of software functionality.; The company standard provides specific remedies for breach of warranty (correction, replacement, or refund), which are entirely absent in the contract clause.",
        "recommendation": "The contract clause significantly deviates from company standards by disclaiming all warranties. It is recommended to revise the clause to incorporate the company's standard warranty provisions, including express warranties on quality, non-infringement, and remedies for breach. At a minimum, the 'as is' clause should be removed and replaced with more balanced warranty language.",
        "clause_reference": "warranties Section",
        "confidence": 0.8
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
      "Add comprehensive dispute_resolution clause matching company standards",
      "The contract clause significantly deviates from company standards by disclaiming all warranties. It is recommended to revise the clause to incorporate the company's standard warranty provisions, including express warranties on quality, non-infringement, and remedies for breach. At a minimum, the 'as is' clause should be removed and replaced with more balanced warranty language.",
      "Add comprehensive indemnification clause matching company standards"
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
        "clause_type": "indemnification",
        "standard_version": "Company standard indemnification clause",
        "contract_version": "Standard indemnification clause not found (appeared in 2 company contracts)...",
        "deviation_severity": "high",
        "explanation": "Standard indemnification clause not found (appeared in 2 company contracts)"
      },
      {
        "clause_type": "warranties",
        "standard_version": "Company standard warranties clause",
        "contract_version": "The contract clause completely disclaims all warranties, whereas the company standard includes detailed express warranties regarding development quality, defect-free software, conformance to specifica...",
        "deviation_severity": "critical",
        "explanation": "The contract clause completely disclaims all warranties, whereas the company standard includes detailed express warranties regarding development quality, defect-free software, conformance to specifications, and non-infringement.; The company standard explicitly disclaims implied warranties of merchantability and fitness for a particular purpose, but the contract clause's \"as is\" provision is a much broader and more aggressive disclaimer that negates even basic expectations of software functionality.; The company standard provides specific remedies for breach of warranty (correction, replacement, or refund), which are entirely absent in the contract clause."
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
        "topic": "Missing Indemnification Clause",
        "advice": "This clause poses significant legal risk that should be addressed. Standard indemnification clause not found (appeared in 2 company contracts)",
        "risk_level": "high",
        "supporting_law": "General Contract Law Principles",
        "recommendations": [
          "Add comprehensive indemnification clause matching company standards"
        ]
      },
      {
        "topic": "Non-Standard Warranties",
        "advice": "This clause poses critical legal risk that requires immediate attention. The contract clause completely disclaims all warranties, whereas the company standard includes detailed express warranties regarding development quality, defect-free software, conformance to specifications, and non-infringement.; The company standard explicitly disclaims implied warranties of merchantability and fitness for a particular purpose, but the contract clause's \"as is\" provision is a much broader and more aggressive disclaimer that negates even basic expectations of software functionality.; The company standard provides specific remedies for breach of warranty (correction, replacement, or refund), which are entirely absent in the contract clause.",
        "risk_level": "critical",
        "supporting_law": "General Contract Law Principles",
        "recommendations": [
          "The contract clause significantly deviates from company standards by disclaiming all warranties. It is recommended to revise the clause to incorporate the company's standard warranty provisions, including express warranties on quality, non-infringement, and remedies for breach. At a minimum, the 'as is' clause should be removed and replaced with more balanced warranty language."
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
    "analyzed_at": "2025-10-25T17:21:03.044749",
    "contract_metadata": {
      "contract_name": "analyzed_contract.docx",
      "parties": [
        {
          "name": "QDB",
          "role": "Client"
        },
        {
          "name": "Vendor",
          "role": "Supplier"
        }
      ],
      "effective_date": "2025-01-01",
      "expiry_date": "2025-12-31",
      "total_value": "Value specified in payment terms",
      "extracted_clauses_count": 1
    }
  }
  let data3={}

const reportRef = useRef(null);

  // PDF Export
  const exportPDF = () => {
    if (!reportRef.current) return;
  
    // Force all text to black
    const originalColor = reportRef.current.style.color;
    reportRef.current.style.color = "black";
  
    const opt = {
      margin: 0.5,
      filename: `Contract_Report_${new Date().toISOString().slice(0, 10)}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
    };
  
    html2pdf().set(opt).from(reportRef.current).save().finally(() => {
      // Restore original color
      reportRef.current.style.color = originalColor;
    });
  };

  // JSON Export
  const exportJSON = () => {
    const blob = new Blob([JSON.stringify({ data1, data2 }, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Contract_Report_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
  };



  return (
    
    <div className="all-data" style={{ padding: "2rem" }}>
      <div className="export-buttons">
  <button onClick={exportPDF}>Export PDF</button>
  <button onClick={exportJSON}>Export JSON</button>
</div>

<div className="gap"></div>
  
      <div  ref={reportRef} >
        <Extraction data={data1} />
        <RiskAnalysis data={data2} />
      </div>
      <footer className="report-footer">
        <small>Generated by Contice Extraction</small>
      </footer>
    </div>
  );
}
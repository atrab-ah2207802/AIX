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
    "overall_score": 42,
    "risk_level": "high",
    "summary": "This contract has significant risk with 3 critical and 4 high-priority QDB standard violations. Legal review strongly recommended.",
    "flags": [
      {
        "severity": "critical",
        "category": "non_standard",
        "title": "Unlimited Liability Clause",
        "description": "Contract contains unlimited liability exposing QDB to significant financial risk. QDB standard limits liability to contract value.",
        "recommendation": "Add liability cap at total contract value and exclude indirect damages",
        "clause_reference": "Article 5: Liability",
        "confidence": 0.95
      },
      {
        "severity": "critical",
        "category": "non_standard",
        "title": "Non-Qatar Jurisdiction",
        "description": "Contract specifies UK jurisdiction instead of QDB standard Qatar jurisdiction. This creates legal enforcement risks.",
        "recommendation": "Change governing law to Qatar and specify Qatar courts for disputes",
        "clause_reference": "Article 2: Governing Law",
        "confidence": 0.98
      },
      {
        "severity": "critical",
        "category": "non_standard",
        "title": "Unfavorable IP Ownership",
        "description": "Supplier owns all intellectual property vs QDB standard joint ownership. This risks QDB's investment in developed assets.",
        "recommendation": "Revise to joint IP ownership or QDB ownership of deliverables",
        "clause_reference": "Article 8: Intellectual Property",
        "confidence": 0.92
      },
      {
        "severity": "high",
        "category": "non_standard",
        "title": "Weak Confidentiality Protection",
        "description": "Missing 2-year survival period and proprietary information definition. QDB standard includes comprehensive protection.",
        "recommendation": "Add 2-year confidentiality duration and define protected information",
        "clause_reference": "Article 6: Confidentiality",
        "confidence": 0.88
      },
      {
        "severity": "high",
        "category": "non_standard",
        "title": "Excessive Termination Notice",
        "description": "90-day termination notice vs QDB standard 30-day notice. This restricts business flexibility.",
        "recommendation": "Negotiate for standard 30-day termination notice",
        "clause_reference": "Article 7: Termination",
        "confidence": 0.85
      },
      {
        "severity": "medium",
        "category": "missing_clause",
        "title": "Missing Force Majeure Protection",
        "description": "Contract lacks force majeure clause. QDB standard includes protection for unforeseen events.",
        "recommendation": "Add force majeure clause covering natural disasters and government actions",
        "clause_reference": "Not Found",
        "confidence": 0.78
      },
      {
        "severity": "medium",
        "category": "unfavorable_term",
        "title": "Unclear Payment Terms",
        "description": "Payment terms lack specific due dates and late payment penalties. QDB standard specifies Net 30 with interest.",
        "recommendation": "Specify exact payment schedule and late payment interest rates",
        "clause_reference": "Article 4: Financial Terms",
        "confidence": 0.75
      }
    ],
    "recommendations": [
      "Add liability cap at total contract value",
      "Change governing law to Qatar jurisdiction",
      "Revise IP ownership to joint or QDB ownership",
      "Add comprehensive confidentiality with 2-year duration",
      "Negotiate 30-day termination notice period",
      "Include force majeure protection clause",
      "Specify clear payment terms with penalties"
    ],
    "compliance_checks": [
      {
        "regulation": "Qatar Commercial Law - Article 1",
        "status": "non_compliant",
        "issues": ["No Qatar jurisdiction specified"],
        "recommendations": ["Add 'This contract shall be governed by Qatar law'"]
      },
      {
        "regulation": "Qatar Commercial Law - Article 172",
        "status": "non_compliant", 
        "issues": ["Payment terms not clearly specified"],
        "recommendations": ["Specify exact payment amounts, due dates, and methods"]
      }
    ],
    "term_consistency": [
      {
        "term": "Confidential Information",
        "definitions": ["information that should be kept private", "proprietary business information"],
        "is_consistent": false,
        "issue_description": "Term defined 2 different ways throughout contract"
      },
      {
        "term": "Effective Date",
        "definitions": ["01 Jan 2025"],
        "is_consistent": true,
        "issue_description": null
      }
    ],
    "clause_comparisons": [
      {
        "clause_type": "confidentiality",
        "standard_version": "Both parties shall maintain confidentiality of all proprietary information for 2 years after termination...",
        "contract_version": "Both parties shall keep confidential information strictly confidential...",
        "deviation_severity": "major",
        "explanation": "Missing 2-year duration and proprietary information definition"
      },
      {
        "clause_type": "termination",
        "standard_version": "Either party may terminate with 30 days written notice...",
        "contract_version": "Either party may terminate with 90 days written notice...", 
        "deviation_severity": "major",
        "explanation": "90-day notice vs standard 30-day notice"
      }
    ],
    "legal_advice": [
      {
        "topic": "Liability and Risk Exposure",
        "advice": "The unlimited liability clause creates significant financial exposure for QDB. Under Qatar Commercial Law Article 172, parties should agree on reasonable liability limits. We recommend capping liability at the total contract value and excluding indirect damages to protect QDB's interests.",
        "risk_level": "critical",
        "supporting_law": "Qatar Commercial Law Article 172",
        "recommendations": [
          "Cap liability at total contract value",
          "Exclude indirect and consequential damages", 
          "Add mutual limitation of liability"
        ]
      },
      {
        "topic": "Jurisdiction and Enforcement",
        "advice": "UK jurisdiction creates significant enforcement risks in Qatar. Qatari courts may not recognize foreign judgments easily. Under Qatar Civil Procedure Law, specifying Qatar jurisdiction ensures proper legal recourse and enforcement mechanisms.",
        "risk_level": "critical", 
        "supporting_law": "Qatar Civil Procedure Law Article 12",
        "recommendations": [
          "Specify Qatar as governing law",
          "Designate Qatari courts for disputes",
          "Consider Qatar International Court for international matters"
        ]
      }
    ],
    "analyzed_at": "2024-01-15T14:30:00Z",
    "contract_metadata": {
      "contract_name": "sample_contract.docx",
      "parties": [
        {"name": "Corelight Technologies, Inc.", "role": "Supplier"},
        {"name": "Blue Fin Consulting W.L.L", "role": "Client"}
      ],
      "effective_date": "2025-01-01",
      "expiry_date": "2025-12-31",
      "total_value": "QAR 45,000",
      "extracted_clauses_count": 8
    }
  }



  return (
    <form>
    <Extraction data={data1}></Extraction>
    <RiskAnalysis data={data2}></RiskAnalysis>
    </form>

  );
}

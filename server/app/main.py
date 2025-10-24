# # server/app/main.py
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from .models import UploadResponse, ContractExtraction, RiskSummary, QARequest, QAAnswer
# from . import ocr, extract, risk, rag

# app = FastAPI(title="AIX CLM Backend")

# DOCS = {}     # doc_id -> raw_text
# INDEX = {}    # doc_id -> vector index (FAISS) + chunks

# @app.get("/api/health")
# def health(): return {"ok": True}

# @app.post("/api/upload", response_model=UploadResponse)
# async def upload(file: UploadFile = File(...)):
#     content = await file.read()
#     text = ocr.read_any(file.filename, content)  # pdf/docx/ocr
#     if not text or len(text) < 20:
#         raise HTTPException(status_code=400, detail="Empty or unreadable document.")
#     doc_id = ocr.make_doc_id(file.filename, content)
#     DOCS[doc_id] = text
#     INDEX[doc_id] = rag.build_index(text)
#     return UploadResponse(doc_id=doc_id, meta={"pages": text.count("\f")+1})

# @app.post("/api/extract", response_model=ContractExtraction)
# async def api_extract(body: dict):
#     doc_id = body.get("doc_id")
#     text = DOCS.get(doc_id)
#     if not text: raise HTTPException(404, "doc_id not found")
#     return extract.run(text)

# @app.post("/api/risk", response_model=RiskSummary)
# async def api_risk(body: dict):
#     doc_id = body.get("doc_id")
#     extraction = body.get("extraction")
#     text = DOCS.get(doc_id)
#     if not text: raise HTTPException(404, "doc_id not found")
#     return risk.assess(text, extraction)

# @app.post("/api/qa", response_model=QAAnswer)
# async def api_qa(req: QARequest):
#     idx = INDEX.get(req.doc_id)
#     if not idx: raise HTTPException(404, "doc_id not found")
#     return rag.answer(idx, req.query)


# ──────────────────────────────────────────────────────────────────────────────
# Repo: server/app
# Files in this single canvas:
#   - main.py
#   - models.py
#   - ocr.py
#   - prompts.py
#   - extract.py
#   - requirements.txt (at server/)
#   - run.sh
# Copy each section into its respective file path.
# ──────────────────────────────────────────────────────────────────────────────

# ============================= main.py =======================================
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import time

from .models import UploadResponse, ContractExtraction
from . import ocr, extract

app = FastAPI(title="AIX CLM Backend — Upload/OCR/Extraction")
@app.get("/", include_in_schema=False)
def root():
    return {"ok": True, "service": "AIX CLM Backend", "endpoints": ["/api/health", "/api/upload", "/api/extract"]}

# CORS — adjust origins for your React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory stores for hackathon speed
DOCS: Dict[str, str] = {}       # doc_id -> raw_text
META: Dict[str, dict] = {}      # doc_id -> meta (pages, timings)

class ExtractRequest(BaseModel):
    doc_id: str
    use_llm: bool = True          # toggle LLM extraction
    fallback_rules: bool = True   # enable rule-based fallback
    lang_hint: str | None = None  # 'en' | 'ar' | None

@app.get("/api/health")
def health():
    return {"ok": True, "ts": time.time()}

@app.post("/api/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    started = time.time()
    try:
        content = await file.read()
        text, meta = ocr.read_any(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    if not text or len(text.strip()) < 20:
        raise HTTPException(status_code=422, detail="Document appears empty or unreadable")

    doc_id = ocr.make_doc_id(file.filename, content)
    DOCS[doc_id] = text
    META[doc_id] = {**meta, "bytes": len(content), "elapsed_ms": int((time.time()-started)*1000)}
    return UploadResponse(doc_id=doc_id, meta=META[doc_id])

@app.post("/api/extract", response_model=ContractExtraction)
async def api_extract(req: ExtractRequest):
    text = DOCS.get(req.doc_id)
    if not text:
        raise HTTPException(status_code=404, detail="doc_id not found")
    return extract.run(text, use_llm=req.use_llm, fallback_rules=req.fallback_rules, lang_hint=req.lang_hint)


#------------for risk----------------------
"""
Test risk analysis module - COMPATIBLE VERSION
"""

import asyncio
import sys
import os

# Add the parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.risk import analyze_contract_risk

# Sample contract data with various risks
SAMPLE_TEXT = """
CONTRACT AGREEMENT

This Agreement is made and entered into as of January 1, 2024 ("Effective Date") by and between:

Company A, a corporation organized under the laws of Qatar ("Provider")
and 
Company B, a limited liability company ("Client")

ARTICLE 1: TERM AND TERMINATION
This Agreement shall commence on the Effective Date and continue for a period of one year. The contract will automatically renew every year for successive one-year periods unless either party provides written notice of non-renewal at least 180 days prior to the expiration date.

Either party may terminate this Agreement with 180 days written notice for any reason.

ARTICLE 2: LIABILITY
Company A shall have unlimited liability for any and all damages, losses, or claims arising from this Agreement, including but not limited to direct, indirect, incidental, and consequential damages.

ARTICLE 3: PAYMENT TERMS
Client shall pay Provider the sum of $50,000 upon execution of this Agreement. Payment terms: Net 90 days from invoice date.

ARTICLE 4: CONFIDENTIALITY
The parties agree to maintain the confidentiality of proprietary information disclosed during the term of this Agreement.

ARTICLE 5: GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of New York.

"Product" means the software application described in Exhibit A.
"Product" shall mean the deliverables specified in Section 2.1.
"""

SAMPLE_DATA = {
    "parties": [
        {"name": "Company A", "role": "Provider"},
        {"name": "Company B", "role": "Client"}
    ],
    "dates": {
        "effective_date": "2024-01-01",
        "expiration_date": "2024-12-31"
    },
    "financial": {
        "paymentTerms": "Net 90",
        "amount": 50000
    },
    "jurisdiction": "New York"
}

async def main():
    print("🧪 Running Comprehensive Risk Analysis Test...")
    print("=" * 70)
    
    result = await analyze_contract_risk(SAMPLE_TEXT, SAMPLE_DATA)
    
    # Display Results
    print(f"\n📊 RISK ASSESSMENT SUMMARY")
    print("=" * 70)
    print(f"Overall Risk Score: {result.overall_score}/100")
    print(f"Risk Level: {result.risk_level.upper()}")
    print(f"\n{result.summary}")
    
    # Risk Flags
    print(f"\n🚨 RISK FLAGS FOUND: {len(result.flags)}")
    print("=" * 70)
    for i, flag in enumerate(result.flags, 1):
        severity_icon = {
            "critical": "🔴",
            "high": "🟠", 
            "medium": "🟡",
            "low": "🔵"
        }.get(flag.severity, "⚪")
        
        print(f"\n{severity_icon} {i}. [{flag.severity.upper()}] {flag.title}")
        print(f"   📝 {flag.description}")
        if flag.recommendation:
            print(f"   💡 Recommendation: {flag.recommendation}")
        if flag.legal_opinion:
            print(f"   ⚖️  Legal Opinion: {flag.legal_opinion}")
    
    # Recommendations
    print(f"\n💡 TOP RECOMMENDATIONS")
    print("=" * 70)
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")
    
    # Compliance Checks
    print(f"\n⚖️ COMPLIANCE CHECKS")
    print("=" * 70)
    for check in result.compliance_checks:
        status_icon = "✅" if check.status == "compliant" else "❌" if check.status == "non_compliant" else "⚠️"
        print(f"{status_icon} {check.regulation}: {check.status.upper()}")
        for issue in check.issues:
            print(f"   - {issue}")
    
    # Term Consistency
    print(f"\n🔤 TERM CONSISTENCY")
    print("=" * 70)
    for term_issue in result.term_consistency:
        status_icon = "✅" if term_issue.is_consistent else "❌"
        print(f"{status_icon} {term_issue.term}: {term_issue.issue_description}")
    
    # Clause Comparisons
    print(f"\n📋 CLAUSE COMPARISONS")
    print("=" * 70)
    for comparison in result.clause_comparisons:
        severity_icon = {
            "none": "✅",
            "minor": "🟡",
            "major": "❌"
        }.get(comparison.deviation_severity, "⚪")
        
        print(f"{severity_icon} {comparison.clause_type.title()}: {comparison.deviation_severity.upper()}")
        print(f"   {comparison.explanation}")
    
    # Legal Advice
    print(f"\n🎓 AI LEGAL ADVICE")
    print("=" * 70)
    for advice in result.legal_advice:
        risk_icon = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }.get(advice.risk_level, "⚪")
        
        print(f"{risk_icon} {advice.topic}")
        print(f"   {advice.advice}")
        if advice.supporting_law:
            print(f"   📚 Supporting Law: {advice.supporting_law}")
        print(f"   💡 Recommendations:")
        for rec in advice.recommendations:
            print(f"      - {rec}")
    
    print(f"\n⏰ Analysis completed at: {result.analyzed_at}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

#----------------------------------------
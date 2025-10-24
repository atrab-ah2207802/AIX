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

from .models import UploadResponse, ContractExtraction, RiskSummary, RiskRequest, RiskFlag  # ← ADD RiskFlag
from . import ocr, extract, risk

app = FastAPI(title="AIX CLM Backend — Upload/OCR/Extraction")

@app.get("/", include_in_schema=False)
def root():
    return {"ok": True, "service": "AIX CLM Backend", "endpoints": ["/api/health", "/api/upload", "/api/extract", "/api/risk"]}

# CORS — adjust origins for your React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory stores for hackathon speed
DOCS: Dict[str, str] = {}       # doc_id -> raw_text
META: Dict[str, dict] = {}      # doc_id -> meta (pages, timings)

class ExtractRequest(BaseModel):
    doc_id: str
    use_llm: bool = True
    fallback_rules: bool = True
    lang_hint: str | None = None

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

# KEEP BOTH VERSIONS FOR COMPATIBILITY
@app.post("/api/risk", response_model=RiskSummary)
async def api_risk(body: dict):  # ← KEEP your colleague's parameter style
    """Run comprehensive risk analysis - compatible with both styles"""
    doc_id = body.get("doc_id")
    extraction_data = body.get("extraction")
    
    text = DOCS.get(doc_id)
    if not text:
        raise HTTPException(status_code=404, detail="doc_id not found")
    
    # Convert extraction to the format your risk module expects
    if isinstance(extraction_data, dict):
        # Handle dict format (your colleague's style)
        extracted_data = {
            "parties": extraction_data.get("parties", []),
            "dates": extraction_data.get("dates", {}),
            "financial": extraction_data.get("financial", {}),
            "jurisdiction": extraction_data.get("governing_law", "")
        }
    else:
        # Handle Pydantic model format (your style)
        extracted_data = {
            "parties": [{"name": p.name, "role": p.role} for p in extraction_data.parties],
            "dates": {
                "effective_date": extraction_data.effective_date,
                "expiration_date": extraction_data.expiry_date
            },
            "financial": {
                "paymentTerms": next((f.text for f in extraction_data.financials if "payment" in f.label.lower()), ""),
                "amount": next((f.amount for f in extraction_data.financials if f.amount), None)
            },
            "jurisdiction": extraction_data.governing_law or ""
        }
    
    # Run your risk analysis
    risk_assessment = await risk.analyze_contract_risk(text, extracted_data)
    
    # Convert to the expected RiskSummary format
    return RiskSummary(
        score=risk_assessment.overall_score,
        flags=[
            RiskFlag(
                title=flag.title,
                severity=flag.severity.capitalize(),
                explanation=flag.description,
                suggested_fix_text=flag.recommendation,
                clause_excerpt=flag.clause_reference
            )
            for flag in risk_assessment.flags[:10]  # Limit to top 10 flags
        ]
    )
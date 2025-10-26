# # # server/app/main.py
# # from fastapi import FastAPI, UploadFile, File, HTTPException
# # from .models import UploadResponse, ContractExtraction, RiskSummary, QARequest, QAAnswer
# # from . import ocr, extract, risk, rag

# # app = FastAPI(title="AIX CLM Backend")

# # DOCS = {}     # doc_id -> raw_text
# # INDEX = {}    # doc_id -> vector index (FAISS) + chunks

# # @app.get("/api/health")
# # def health(): return {"ok": True}

# # @app.post("/api/upload", response_model=UploadResponse)
# # async def upload(file: UploadFile = File(...)):
# #     content = await file.read()
# #     text = ocr.read_any(file.filename, content)  # pdf/docx/ocr
# #     if not text or len(text) < 20:
# #         raise HTTPException(status_code=400, detail="Empty or unreadable document.")
# #     doc_id = ocr.make_doc_id(file.filename, content)
# #     DOCS[doc_id] = text
# #     INDEX[doc_id] = rag.build_index(text)
# #     return UploadResponse(doc_id=doc_id, meta={"pages": text.count("\f")+1})

# # @app.post("/api/extract", response_model=ContractExtraction)
# # async def api_extract(body: dict):
# #     doc_id = body.get("doc_id")
# #     text = DOCS.get(doc_id)
# #     if not text: raise HTTPException(404, "doc_id not found")
# #     return extract.run(text)

# # @app.post("/api/risk", response_model=RiskSummary)
# # async def api_risk(body: dict):
# #     doc_id = body.get("doc_id")
# #     extraction = body.get("extraction")
# #     text = DOCS.get(doc_id)
# #     if not text: raise HTTPException(404, "doc_id not found")
# #     return risk.assess(text, extraction)

# # @app.post("/api/qa", response_model=QAAnswer)
# # async def api_qa(req: QARequest):
# #     idx = INDEX.get(req.doc_id)
# #     if not idx: raise HTTPException(404, "doc_id not found")
# #     return rag.answer(idx, req.query)


# # ──────────────────────────────────────────────────────────────────────────────
# # Repo: server/app
# # Files in this single canvas:
# #   - main.py
# #   - models.py
# #   - ocr.py
# #   - prompts.py
# #   - extract.py
# #   - requirements.txt (at server/)
# #   - run.sh
# # Copy each section into its respective file path.
# # ──────────────────────────────────────────────────────────────────────────────

# # ============================= main.py =======================================
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Dict
# import time
# from fastapi import BackgroundTasks

# from .models import UploadResponse, ContractExtraction
# from . import ocr, extract

# from . import rag

# from .gemini_helper import answer_with_gemini
# import os
# from .gemini_helper import build_qa_prompt, answer_with_gemini_prompt
# from .models import QARequest, QAAnswer, QASource, QADebugAnswer
# from . import rag



# app = FastAPI(title="AIX CLM Backend — Upload/OCR/Extraction")

# @app.get("/", include_in_schema=False)
# def root():
#     return {"ok": True, "service": "AIX CLM Backend", "endpoints": ["/api/health", "/api/upload", "/api/extract"]}

# # CORS — adjust origins for your React dev server
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # In‑memory stores for hackathon speed
# DOCS: Dict[str, str] = {}       # doc_id -> raw_text
# META: Dict[str, dict] = {}      # doc_id -> meta (pages, timings)
# INDEX: Dict[str, rag.SimpleIndex] = {}

# class ExtractRequest(BaseModel):
#     doc_id: str
#     use_llm: bool = True
#     fallback_rules: bool = True
#     lang_hint: str | None = None

# @app.get("/api/health")
# def health():
#     return {"ok": True, "ts": time.time()}

# # @app.post("/api/upload", response_model=UploadResponse)
# # async def upload(file: UploadFile = File(...)):
# #     started = time.time()
# #     try:
# #         content = await file.read()
# #         text, meta = ocr.read_any(file.filename, content)
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

# #     if not text or len(text.strip()) < 20:
# #         raise HTTPException(status_code=422, detail="Document appears empty or unreadable")

# #     doc_id = ocr.make_doc_id(file.filename, content)
# #     DOCS[doc_id] = text
# #     META[doc_id] = {**meta, "bytes": len(content), "elapsed_ms": int((time.time()-started)*1000)}
# #     return UploadResponse(doc_id=doc_id, meta=META[doc_id])

# @app.post("/api/upload", response_model=UploadResponse)
# async def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
#     t0 = time.time()
#     content = await file.read()
#     t1 = time.time()
#     text, meta = ocr.read_any(file.filename, content)  # OCR or text extract
#     t2 = time.time()
    

#     doc_id = ocr.make_doc_id(file.filename, content)
#     DOCS[doc_id] = text
#     META[doc_id] = {**meta, "bytes": len(content)}
#     print("done reading")

#     # QA index build (can be slow the first time)
#     def _build():
#         from . import rag
#         try:
#             INDEX[doc_id] = rag.build_index(text, multilingual=True)
#             print(f"[index] built for {doc_id}, chunks={len(INDEX[doc_id].chunks)}")
#         except Exception as e:
#             print("[index] error:", e)

#     if background_tasks is not None:
#         background_tasks.add_task(_build)
#     # else: skip building here; do it lazily on /api/qa

#     return UploadResponse(doc_id=doc_id, meta=META[doc_id])


# @app.post("/api/extract", response_model=ContractExtraction)
# async def api_extract(req: ExtractRequest):
#     text = DOCS.get(req.doc_id)
#     if not text:
#         raise HTTPException(status_code=404, detail="doc_id not found")
#     return extract.run(text, use_llm=req.use_llm, fallback_rules=req.fallback_rules, lang_hint=req.lang_hint)




# from fastapi import HTTPException


# @app.post("/api/qa", response_model=QAAnswer)
# async def api_qa(req: QARequest):
#     text = DOCS.get(req.doc_id)
#     if text is None:
#         raise HTTPException(status_code=404, detail="doc_id not found")

#     idx = INDEX.get(req.doc_id)
#     if idx is None:
#         # build on-demand (fast if TF-IDF; set RAG_EMB=tfidf for hackathon)
#         try:
#             idx = rag.build_index(text, multilingual=True)
#             INDEX[req.doc_id] = idx
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"index build failed: {e}")

#     results = rag.retrieve(req.query, idx, k=max(1, min(req.k, 8)))
#     contexts = [(cid, idx.chunks[cid]) for cid, _ in results]
#     answer = answer_with_gemini(req.query, contexts)

#     sources = [QASource(chunk_id=int(cid), score=float(score), text=idx.chunks[cid]) for cid, score in results]
#     return QAAnswer(answer=answer, sources=sources)


# import os

# @app.on_event("startup")
# def warmup():
#     if os.getenv("RAG_EMB","").lower() != "tfidf":
#         try:
#             rag.preload_sbert(multilingual=True)
#             print("[startup] SBERT preloaded")
#         except Exception as e:
#             print("[startup] preload failed, will fallback:", e)

# # top of main.py
# from .models import QARequest, QAAnswer, QASource, QADebugAnswer
# from .gemini_helper import build_qa_prompt, answer_with_gemini_prompt
# from . import rag

# import os, threading
# from fastapi import HTTPException
# from . import rag

# PENDING_INDEX: set[str] = set()  # track in-flight builds

# def _build_index_bg(doc_id: str, text: str, multilingual=True):
#     try:
#         idx = rag.build_index(text, multilingual=multilingual)
#         INDEX[doc_id] = idx
#     finally:
#         PENDING_INDEX.discard(doc_id)

# @app.post("/api/qa/debug", response_model=QADebugAnswer)
# async def api_qa_debug(req: QARequest):
#     text = DOCS.get(req.doc_id)
#     if text is None:
#         raise HTTPException(404, "doc_id not found")

#     idx = INDEX.get(req.doc_id)
#     if idx is None:
#         if req.doc_id not in PENDING_INDEX:
#             PENDING_INDEX.add(req.doc_id)
#             threading.Thread(target=_build_index_bg, args=(req.doc_id, text, True), daemon=True).start()
#         # Don’t block: tell frontend to retry shortly
#         raise HTTPException(status_code=202, detail="Index is being prepared. Please retry in a moment.")

#     # … proceed with retrieve → prompt → Gemini as before …



#     k = max(1, min(req.k, 8))
#     results = rag.retrieve(req.query, idx, k=k)
#     contexts = [(cid, idx.chunks[cid]) for cid, _ in results]

#     prompt = build_qa_prompt(req.query, contexts, max_total_chars=1600, per_chunk_chars=350)
#     answer = answer_with_gemini_prompt(prompt, model_name=os.getenv("GEMINI_QA_MODEL","gemini-2.0-flash"))

#     sources = [QASource(chunk_id=int(cid), score=float(score), text=idx.chunks[cid]) for cid, score in results]
#     return QADebugAnswer(answer=answer, sources=sources, prompt=prompt, model_name=os.getenv("GEMINI_QA_MODEL","gemini-2.0-flash"))


# # # I MADE A SEPERATE SERVER FOR RISK CZ ERRORS WERE OCCURING
# # @app.post("/api/risk", response_model=RiskSummary)
# # async def api_risk(body: dict):  # ← KEEP your colleague's parameter style
# #     """Run comprehensive risk analysis - compatible with both styles"""
# #     doc_id = body.get("doc_id")
# #     extraction_data = body.get("extraction")
    
# #     text = DOCS.get(doc_id)
# #     if not text:
# #         raise HTTPException(status_code=404, detail="doc_id not found")
    
# #     # Convert extraction to the format your risk module expects
# #     if isinstance(extraction_data, dict):
# #         # Handle dict format (your colleague's style)
# #         extracted_data = {
# #             "parties": extraction_data.get("parties", []),
# #             "dates": extraction_data.get("dates", {}),
# #             "financial": extraction_data.get("financial", {}),
# #             "jurisdiction": extraction_data.get("governing_law", "")
# #         }
# #     else:
# #         # Handle Pydantic model format (your style)
# #         extracted_data = {
# #             "parties": [{"name": p.name, "role": p.role} for p in extraction_data.parties],
# #             "dates": {
# #                 "effective_date": extraction_data.effective_date,
# #                 "expiration_date": extraction_data.expiry_date
# #             },
# #             "financial": {
# #                 "paymentTerms": next((f.text for f in extraction_data.financials if "payment" in f.label.lower()), ""),
# #                 "amount": next((f.amount for f in extraction_data.financials if f.amount), None)
# #             },
# #             "jurisdiction": extraction_data.governing_law or ""
# #         }
    
# #     # Run your risk analysis
# #     risk_assessment = await risk.analyze_contract_risk(text, extracted_data)
    
# #     # Convert to the expected RiskSummary format
# #     return RiskSummary(
# #         score=risk_assessment.overall_score,
# #         flags=[
# #             RiskFlag(
# #                 title=flag.title,
# #                 severity=flag.severity.capitalize(),
# #                 explanation=flag.description,
# #                 suggested_fix_text=flag.recommendation,
# #                 clause_excerpt=flag.clause_reference
# #             )
# #             for flag in risk_assessment.flags[:10]  # Limit to top 10 flags
# #         ]
# #     )


from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import time, os, threading

from .models import (
    UploadResponse,
    ContractExtraction,
    QARequest,
    QAAnswer,
    QASource,
    QADebugAnswer,
)

from . import ocr, extract, rag
from .gemini_helper import (
    answer_with_gemini,
    build_qa_prompt,
    answer_with_gemini_prompt,
)

app = FastAPI(title="AIX CLM Backend — Upload/OCR/Extraction/QA")

@app.get("/", include_in_schema=False)
def root():
    return {"ok": True, "service": "AIX CLM Backend", "endpoints": [
        "/api/health", "/api/upload", "/api/extract", "/api/qa", "/api/qa/debug"
    ]}

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
INDEX: Dict[str, rag.SimpleIndex] = {}
PENDING_INDEX: set[str] = set()  # track in‑flight builds

class ExtractRequest(BaseModel):
    doc_id: str
    use_llm: bool = True
    fallback_rules: bool = True
    lang_hint: str | None = None

@app.get("/api/health")
def health():
    return {"ok": True, "ts": time.time()}

# @app.post("/api/upload", response_model=UploadResponse)
# async def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks | None = None):
#     content = await file.read()
#     text, meta = ocr.read_any(file.filename, content)  # OCR or text extract

#     if not text or len(text.strip()) < 20:
#         raise HTTPException(status_code=422, detail="Document appears empty or unreadable")

#     doc_id = ocr.make_doc_id(file.filename, content)
#     DOCS[doc_id] = text
#     META[doc_id] = {**meta, "bytes": len(content)}

#     def _build():
#         try:
#             INDEX[doc_id] = rag.build_index(text, multilingual=True)
#             print(f"[index] built for {doc_id}, chunks={len(INDEX[doc_id].chunks)}")
#         except Exception as e:
#             print("[index] error:", e)

#     if background_tasks is not None:
#         background_tasks.add_task(_build)

#     return UploadResponse(doc_id=doc_id, meta=META[doc_id])
# server/app/main.py

from fastapi import BackgroundTasks

@app.post("/api/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None  # <-- keep a plain type; no union
):
    content = await file.read()
    text, meta = ocr.read_any(file.filename, content)

    if not text or len(text.strip()) < 20:
        raise HTTPException(status_code=422, detail="Document appears empty or unreadable")

    doc_id = ocr.make_doc_id(file.filename, content)
    DOCS[doc_id] = text
    META[doc_id] = {**meta, "bytes": len(content)}

    def _build():
        try:
            INDEX[doc_id] = rag.build_index(text, multilingual=True)
            print(f"[index] built for {doc_id}, chunks={len(INDEX[doc_id].chunks)}")
        except Exception as e:
            print("[index] error:", e)

    if background_tasks is not None:
        background_tasks.add_task(_build)

    return UploadResponse(doc_id=doc_id, meta=META[doc_id])

@app.post("/api/extract", response_model=ContractExtraction)
async def api_extract(req: ExtractRequest):
    text = DOCS.get(req.doc_id)
    if not text:
        raise HTTPException(status_code=404, detail="doc_id not found")
    return extract.run(text, use_llm=req.use_llm, fallback_rules=req.fallback_rules, lang_hint=req.lang_hint)

# ---- QA routing (auto | full | rag) ----
FULLTEXT_CHAR_LIMIT = int(os.getenv("QA_FULLTEXT_CHAR_LIMIT", "30000"))

@app.post("/api/qa", response_model=QAAnswer)
async def api_qa(req: QARequest):
    text = DOCS.get(req.doc_id)
    if text is None:
        raise HTTPException(status_code=404, detail="doc_id not found")

    strategy = (req.strategy or "auto").lower()
    if strategy == "auto":
        strategy = "full" if len(text) <= FULLTEXT_CHAR_LIMIT else "rag"

    if strategy == "full":
        # Send whole contract (capped) for small docs
        prompt = (
            "Answer the question using ONLY the contract below. "
            "Cite supporting lines using [contract]. If not found, say so.\n\n"
            f"Question: {req.query}\n\n"
            f"Contract [contract]:\n{text[:120000]}"  # hard cap for safety
        )
        answer = answer_with_gemini_prompt(prompt)
        return QAAnswer(
            answer=answer,
            sources=[QASource(chunk_id=0, score=1.0, text=text[:800])]
        )

    # RAG path
    idx = INDEX.get(req.doc_id)
    if idx is None:
        try:
            idx = rag.build_index(text, multilingual=True)
            INDEX[req.doc_id] = idx
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"index build failed: {e}")

    k = max(1, min(req.k, 8))
    results = rag.retrieve(req.query, idx, k=k)
    contexts = [(cid, idx.chunks[cid]) for cid, _ in results]
    answer = answer_with_gemini(req.query, contexts)

    sources = [QASource(chunk_id=int(cid), score=float(score), text=idx.chunks[cid]) for cid, score in results]
    return QAAnswer(answer=answer, sources=sources)

# Optional: async debug variant that won’t block while index builds

def _build_index_bg(doc_id: str, text: str, multilingual=True):
    try:
        idx = rag.build_index(text, multilingual=multilingual)
        INDEX[doc_id] = idx
    finally:
        PENDING_INDEX.discard(doc_id)

@app.post("/api/qa/debug", response_model=QADebugAnswer)
async def api_qa_debug(req: QARequest):
    text = DOCS.get(req.doc_id)
    if text is None:
        raise HTTPException(status_code=404, detail="doc_id not found")

    idx = INDEX.get(req.doc_id)
    if idx is None:
        if req.doc_id not in PENDING_INDEX:
            PENDING_INDEX.add(req.doc_id)
            threading.Thread(target=_build_index_bg, args=(req.doc_id, text, True), daemon=True).start()
        raise HTTPException(status_code=202, detail="Index is being prepared. Please retry in a moment.")

    k = max(1, min(req.k, 8))
    results = rag.retrieve(req.query, idx, k=k)
    contexts = [(cid, idx.chunks[cid]) for cid, _ in results]

    prompt = build_qa_prompt(req.query, contexts, max_total_chars=1600, per_chunk_chars=350)
    answer = answer_with_gemini_prompt(prompt, model_name=os.getenv("GEMINI_QA_MODEL", "gemini-2.0-flash"))

    sources = [QASource(chunk_id=int(cid), score=float(score), text=idx.chunks[cid]) for cid, score in results]
    return QADebugAnswer(answer=answer, sources=sources, prompt=prompt, model_name=os.getenv("GEMINI_QA_MODEL", "gemini-2.0-flash"))

# Warmup SBERT to avoid first‑query latency (if available and not forcing TF‑IDF)
@app.on_event("startup")
def warmup():
    if os.getenv("RAG_EMB", "").lower() != "tfidf":
        try:
            rag.preload_sbert(multilingual=True)
            print("[startup] SBERT preloaded")
        except Exception as e:
            print("[startup] preload failed, will fallback:", e)


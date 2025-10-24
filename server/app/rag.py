# server/app/rag.py
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

MODEL = SentenceTransformer("multi-qa-mpnet-base-dot-v1")

def chunk_text(t: str, size=800, step=700):
    out=[]; i=0
    while i < len(t):
        out.append(t[i:i+size])
        i += step
    return out

def build_index(text: str):
    chunks = chunk_text(text)
    embs = MODEL.encode(chunks, convert_to_numpy=True, show_progress_bar=False)
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embs)
    index.add(embs)
    return {"index": index, "chunks": chunks, "embs": embs}

def answer(idx, query: str):
    q = MODEL.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q)
    D,I = idx["index"].search(q, 3)
    ctx = [idx["chunks"][i] for i in I[0] if i!=-1]
    # Call LLM with ctx + query (omitted here)
    return {"answer": f"(demo) Based on: {ctx[0][:120]}...", "sources": [{"chunk": c[:160], "score": float(s)} for c,s in zip(ctx, D[0])]}

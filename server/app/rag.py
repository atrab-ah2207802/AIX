# # server/app/rag.py
# from __future__ import annotations
# import re, math
# from dataclasses import dataclass
# from typing import List, Tuple
# import numpy as np
# import os
# _FORCE_TFIDF = os.getenv("RAG_EMB", "").lower() == "tfidf"

# # Embeddings: prefer sentence-transformers; fallback to tf-idf
# try:
#     from sentence_transformers import SentenceTransformer
#     _SENT_EMB_OK = True
# except Exception:
#     _SENT_EMB_OK = False

# try:
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     _TFIDF_OK = True
# except Exception:
#     _TFIDF_OK = False

# # ----------------------- chunking -----------------------
# def clean_text(t: str) -> str:
#     return re.sub(r"[ \t]+", " ", t.replace("\r", "")).strip()

# def split_into_chunks(text: str, max_chars: int = 700, overlap: int = 120) -> List[str]:
#     text = clean_text(text)
#     if len(text) <= max_chars:
#         return [text]
#     chunks, i = [], 0
#     while i < len(text):
#         j = i + max_chars
#         if j < len(text):
#             # prefer to cut at sentence boundary
#             k = text.rfind(". ", i, j)
#             if k == -1 or k < i + (max_chars // 2):
#                 k = j
#             else:
#                 k = k + 1
#         else:
#             k = len(text)
#         chunks.append(text[i:k].strip())
#         i = max(0, k - overlap)
#     return [c for c in chunks if c]

# @dataclass
# class SimpleIndex:
#     chunks: List[str]
#     emb_type: str              # "sbert" or "tfidf"
#     emb_matrix: np.ndarray     # shape: (n_chunks, dim)
#     vectorizer: object | None  # TfidfVectorizer if emb_type == "tfidf"
#     model_name: str | None     # sbert model name if used

# # ----------------------- build index -----------------------
# def build_index(text: str, multilingual: bool = True) -> SimpleIndex:
#     chunks = split_into_chunks(text, max_chars=700, overlap=120)

#     if not _FORCE_TFIDF:
#         try:
#             from sentence_transformers import SentenceTransformer
#             model_name = "sentence-transformers/multi-qa-mpnet-base-dot-v1" if multilingual else "sentence-transformers/all-MiniLM-L6-v2"
#             model = _get_sbert(model_name)  # uses cache
#             vecs = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
#             return SimpleIndex(chunks=chunks, emb_type="sbert", emb_matrix=vecs, vectorizer=None, model_name=model_name)
#         except Exception as e:
#             print("[RAG] SBERT unavailable, falling back to TF-IDF:", e)

#     # TF-IDF path
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=50000)
#     vecs = tfidf.fit_transform(chunks).astype(np.float32)
#     return SimpleIndex(chunks=chunks, emb_type="tfidf", emb_matrix=vecs, vectorizer=tfidf, model_name=None)

# # ----------------------- retrieve -----------------------
# def _embed_query(query: str, idx: SimpleIndex) -> np.ndarray:
#     if idx.emb_type == "sbert":
#         model = SentenceTransformer(idx.model_name)  # cached in RAM by HF
#         q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
#         return q
#     if idx.emb_type == "tfidf":
#         v = idx.vectorizer.transform([query]).astype(np.float32)
#         return v
#     # bow
#     v = np.zeros((len(idx.vectorizer),), dtype=np.float32)
#     for tok in re.findall(r"[A-Za-z0-9%]+", query.lower()):
#         j = idx.vectorizer.get(tok)
#         if j is not None:
#             v[j] += 1
#     if v.sum() > 0:
#         v /= np.linalg.norm(v)
#     return v

# def retrieve(query: str, idx: SimpleIndex, k: int = 4) -> List[Tuple[int, float]]:
#     qv = _embed_query(query, idx)
#     if idx.emb_type in ("sbert","bow"):
#         sims = idx.emb_matrix @ qv
#         order = np.argsort(-sims)[:k]
#         return [(int(i), float(sims[i])) for i in order]
#     # tfidf cosine
#     sims = (idx.emb_matrix @ qv.T).toarray().ravel()
#     order = np.argsort(-sims)[:k]
#     return [(int(i), float(sims[i])) for i in order]


# # at top of rag.py (near imports)
# _SBERT_CACHE = {}

# _SBERT_CACHE = {}

# def _get_sbert(model_name: str):
#     from sentence_transformers import SentenceTransformer
#     if model_name not in _SERT_CACHE:
#         _SBERT_CACHE[model_name] = SentenceTransformer(model_name)  # one-time load
#     return _SBERT_CACHE[model_name]

# def preload_sbert(multilingual: bool = True):
#     model_name = "sentence-transformers/multi-qa-mpnet-base-dot-v1" if multilingual else "sentence-transformers/all-MiniLM-L6-v2"
#     _get_sbert(model_name)


# def _embed_query(query: str, idx: SimpleIndex) -> np.ndarray:
#     if idx.emb_type == "sbert":
#         model = _get_sbert(idx.model_name)  # ← cached, no reload
#         return model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
#     if idx.emb_type == "tfidf":
#         return idx.vectorizer.transform([query]).astype(np.float32)
#     # bow fallback...
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import os

_FORCE_TFIDF = os.getenv("RAG_EMB", "").lower() == "tfidf"

# Try to import sentence-transformers; allow fallback
try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    _SENT_EMB_OK = True
except Exception:
    _SENT_EMB_OK = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    _TFIDF_OK = True
except Exception:
    _TFIDF_OK = False

# ----------------------- chunking -----------------------

def clean_text(t: str) -> str:
    return re.sub(r"[ \t]+", " ", t.replace("\r", "")).strip()

def split_into_chunks(text: str, max_chars: int = 700, overlap: int = 120) -> List[str]:
    text = clean_text(text)
    if len(text) <= max_chars:
        return [text]
    chunks, i = [], 0
    while i < len(text):
        j = i + max_chars
        if j < len(text):
            # prefer to cut at sentence boundary
            k = text.rfind(". ", i, j)
            if k == -1 or k < i + (max_chars // 2):
                k = j
            else:
                k = k + 1
        else:
            k = len(text)
        chunks.append(text[i:k].strip())
        i = max(0, k - overlap)
    return [c for c in chunks if c]

# ----------------------- index -----------------------

@dataclass
class SimpleIndex:
    chunks: List[str]
    emb_type: str              # "sbert" or "tfidf"
    emb_matrix: np.ndarray     # shape: (n_chunks, dim) or sparse matrix
    vectorizer: object | None  # TfidfVectorizer if emb_type == "tfidf"
    model_name: str | None     # sbert model name if used

_SBERT_CACHE: dict[str, "SentenceTransformer"] = {}


def _get_sbert(model_name: str):
    """Load/cached SBERT model once per process."""
    if model_name not in _SBERT_CACHE:
        if not _SENT_EMB_OK:
            raise RuntimeError("sentence-transformers not available")
        _SBERT_CACHE[model_name] = SentenceTransformer(model_name)
    return _SBERT_CACHE[model_name]


def preload_sbert(multilingual: bool = True):
    model_name = (
        "sentence-transformers/multi-qa-mpnet-base-dot-v1" if multilingual
        else "sentence-transformers/all-MiniLM-L6-v2"
    )
    try:
        _get_sbert(model_name)
    except Exception:
        pass


def build_index(text: str, multilingual: bool = True) -> SimpleIndex:
    chunks = split_into_chunks(text, max_chars=700, overlap=120)

    if not _FORCE_TFIDF and _SENT_EMB_OK:
        try:
            model_name = (
                "sentence-transformers/multi-qa-mpnet-base-dot-v1" if multilingual
                else "sentence-transformers/all-MiniLM-L6-v2"
            )
            model = _get_sbert(model_name)
            vecs = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
            return SimpleIndex(chunks=chunks, emb_type="sbert", emb_matrix=vecs, vectorizer=None, model_name=model_name)
        except Exception as e:
            print("[RAG] SBERT unavailable, falling back to TF-IDF:", e)

    if not _TFIDF_OK:
        raise RuntimeError("scikit-learn not available for TF-IDF fallback")

    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=50000)
    vecs = tfidf.fit_transform(chunks).astype(np.float32)
    return SimpleIndex(chunks=chunks, emb_type="tfidf", emb_matrix=vecs, vectorizer=tfidf, model_name=None)

# ----------------------- retrieval -----------------------

def _embed_query(query: str, idx: SimpleIndex):
    if idx.emb_type == "sbert":
        model = _get_sbert(idx.model_name or "sentence-transformers/all-MiniLM-L6-v2")
        q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
        return q
    if idx.emb_type == "tfidf":
        assert idx.vectorizer is not None
        return idx.vectorizer.transform([query]).astype(np.float32)
    raise ValueError(f"Unknown emb_type: {idx.emb_type}")


def retrieve(query: str, idx: SimpleIndex, k: int = 4) -> List[Tuple[int, float]]:
    qv = _embed_query(query, idx)
    if idx.emb_type == "sbert":
        sims = idx.emb_matrix @ qv
        order = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i])) for i in order]
    # tfidf cosine
    sims = (idx.emb_matrix @ qv.T).toarray().ravel()
    order = np.argsort(-sims)[:k]
    return [(int(i), float(sims[i])) for i in order]


#!/usr/bin/env bash
# ============================= run.sh ========================================
set -euo pipefail

export PYTHONUNBUFFERED=1

# --- LLM provider: Google Gemini ---
# Expect GEMINI_API_KEY to be set in your shell (recommended):
#   export GEMINI_API_KEY="your_real_key"
# Or uncomment the next line (NOT recommended to commit real keys):
# export GEMINI_API_KEY="your_real_key"

if [ "${GEMINI_API_KEY:-}" = "" ]; then
  echo "[warn] GEMINI_API_KEY is not set. Run: export GEMINI_API_KEY='AIzaSyAuaNa4BbYOmHFBYTuaw_xfiLm2ASMWLqY'"
fi


export GEMINI_QA_MODEL=gemini-2.0-flash-lite
export BUILD_INDEX_ON_UPLOAD=0
export RAG_EMB=tfidf 
# Make sure other providers are off
export USE_BYTEZ=0
unset BYTEZ_API_KEY BYTEZ_MODEL
unset USE_OPENAI_JSON OPENAI_API_KEY OPENAI_MODEL

# FastAPI dev server
uvicorn server.app.main:app --reload --port 8000

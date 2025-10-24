
# ============================= run.sh ========================================
# Simple dev runner (bash)
# ─ Run: bash run.sh
export PYTHONUNBUFFERED=1
export USE_OPENAI_JSON=0   # set 1 when you wire your key + model
# export OPENAI_API_KEY=...  # set when USE_OPENAI_JSON=1
uvicorn server.app.main:app --reload --port 8000

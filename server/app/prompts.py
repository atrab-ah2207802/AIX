# # server/app/prompts.py
# EXTRACT_PROMPT = """You are an expert contract parser...
# Return strictly valid JSON with keys:
# parties[], effective_date, expiry_date, renewals, governing_law,
# obligations[], financials[], signatures_present, raw_summary.
# Contract:
# \"\"\"{chunk}\"\"\""""

# RISK_PROMPT = """You are a contracts risk assessor for Qatar law context (general).
# Input JSON (extraction) and key clauses. Output JSON:
# overall_risk_score (0-100), flags: [{title, severity, explanation, suggested_fix_text, clause_excerpt}].
# Be concise and actionable."""


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


# ============================= prompts.py ====================================
EXTRACT_JSON_PROMPT = """
You are an expert contract parser. Return STRICT JSON with keys:
parties[{name,role}], effective_date, expiry_date, renewals, governing_law,
obligations[{party,text}], financials[{label,amount,currency,text}], signatures_present, raw_summary (bulleted text).
Focus on accuracy; if missing, return null or [].
Text:
\"\"\"{TEXT}\"\"\"
"""


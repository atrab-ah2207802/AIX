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
# EXTRACT_JSON_PROMPT = """
# You are an expert contract parser. Return STRICT JSON with keys:
# parties[{name,role}], effective_date, expiry_date, renewals, governing_law,
# obligations[{party,text}], financials[{label,amount,currency,text}], signatures_present, raw_summary (bulleted text).
# Focus on accuracy; if missing, return null or [].
# Text:
# \"\"\"{TEXT}\"\"\"
# """

# """
# Prompt templates for AI analysis
# """
EXTRACT_JSON_PROMPT = """
You are an expert contract parser. Return ONLY valid JSON with these fields:
{
  "parties": [{"name": "", "role": ""}],
  "effective_date": "",
  "expiry_date": "",
  "renewal_date": "",
  "auto_renewal": true,
  "renewals": "",
  "governing_law": "",
  "jurisdiction": "",
  "obligations": [{"party": "", "text": ""}],
  "financials": [{
    "label": "Payment",
    "amount": "",
    "currency": "",
    "schedule": "",
    "penalties": [{"type": "", "amount": "", "rate": "", "condition": "", "text": ""}],
    "text": ""
  }],
  "signatures_present": true,
  "raw_summary": ""
}

Rules:
- Output JSON only (no markdown or prose).
- If a value is explicitly present in text (e.g., "QAR 45,000", "1.5% per month", "within 30 days"), DO NOT leave it null; copy the exact string.
- Prefer extracting the responsible party for each obligation when it’s clear (“Supplier shall…”, “Client shall…”).
- If a party line contains a role in parentheses, set role accordingly (e.g., "Corelight Technologies, Inc. (Supplier)").
- If renewal is described (notice period, term), set `auto_renewal: true` and compress details in `renewals`.
- Penalties: include any late fees/interest as a penalty with fields filled; at minimum set `text`.
- Dates and amounts: keep the exact formatting from the contract.
- If a field truly does not exist, use null or [].

Examples:

TEXT:
Client shall pay QAR 45,000 within 30 days of delivery; late payments accrue 1.5% per month.

JSON snippet:
{
  "financials": [{
    "label": "Payment",
    "amount": "45,000",
    "currency": "QAR",
    "schedule": "within 30 days",
    "penalties": [{"type": "late/interest", "amount": null, "rate": "1.5% per month", "condition": "late payment", "text": "late payments accrue 1.5% per month"}],
    "text": "Client shall pay QAR 45,000 within 30 days of delivery"
  }]
}

TEXT:
This Agreement auto-renews annually unless terminated with 60 days' prior written notice.

JSON snippet:
{
  "auto_renewal": true,
  "renewals": "notice_period: 60 days; term: annual"
}

Now parse this contract:

\"\"\"{TEXT}\"\"\" 
"""



RISK_ANALYSIS_PROMPT = """
Analyze this contract for legal risks and compliance issues.

EXTRACTED DATA:
{extracted_data}

CONTRACT TEXT (sample):
{contract_text}

Identify risks in these categories:
1. Ambiguous language that could lead to disputes
2. One-sided or unfair terms
3. Missing protections for either party
4. Compliance gaps (GDPR, Qatar law, industry standards)
5. Potential financial exposure

For each risk, provide JSON with:
- severity: critical/high/medium/low
- category: ambiguous/unfavorable_term/compliance/missing_protection
- title: Brief risk title
- description: Clear explanation
- recommendation: Specific action
- clause_reference: Quote relevant text
- confidence: 0-1

Return: {{"risks": [...]}}
"""

LEGAL_ADVICE_PROMPT = """
As a senior legal counsel in Qatar, provide advice on these contract issues:

CATEGORY: {category}

ISSUES IDENTIFIED:
{issues}

CONTRACT EXCERPT:
{contract_excerpt}

Provide legal advice including:
1. Analysis of the legal risk
2. Potential consequences
3. Relevant Qatar Commercial Law or Civil Code articles
4. Specific recommendations to mitigate risk

Return JSON:
{{
  "advice": "Detailed legal advice...",
  "risk_level": "low/medium/high/critical",
  "supporting_law": "Qatar Commercial Law Article X...",
  "recommendations": ["actionable step 1", "actionable step 2"]
}}
"""

CLAUSE_COMPARISON_PROMPT = """
Compare this contract clause to the standard template:

STANDARD TEMPLATE:
{standard_clause}

ACTUAL CONTRACT CLAUSE:
{contract_clause}

Identify:
1. Key differences
2. Missing elements
3. Risk level of deviations
4. Recommendations to align with standard

Return JSON with analysis.
"""

TERM_CONSISTENCY_PROMPT = """
Check if these defined terms are used consistently:

TERMS FOUND:
{terms}

CONTRACT TEXT:
{text}

Identify:
1. Inconsistent capitalization
2. Multiple definitions for same term
3. Undefined terms used
4. Recommendations for consistency

Return JSON with findings.
"""

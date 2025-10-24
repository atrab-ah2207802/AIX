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

"""
Prompt templates for AI analysis
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

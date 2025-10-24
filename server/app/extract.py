# # server/app/extract.py
# from .models import ContractExtraction
# from . import prompts
# # plug your LLM client here

# def llm_json(prompt: str) -> dict:
#     # call your LLM with JSON mode or regex cleanup
#     # return parsed dict
#     return {}

# def run(text: str) -> ContractExtraction:
#     # if long, take top N chunks (e.g., first 3k-4k chars)
#     chunk = text[:8000]
#     data = llm_json(prompts.EXTRACT_PROMPT.format(chunk=chunk))
#     # minimal fallback if LLM fails
#     data.setdefault("parties", [])
#     data.setdefault("obligations", [])
#     data.setdefault("financials", [])
#     return ContractExtraction(**data)


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


# ============================= extract.py ====================================
import json
import os
import re
from typing import Optional
from .models import ContractExtraction, Party, Obligation, MoneyTerm
from .prompts import EXTRACT_JSON_PROMPT

# ---- LLM client adapter (swap in your provider) -----------------------------
USE_OPENAI = os.getenv("USE_OPENAI_JSON", "0") == "1"

if USE_OPENAI:
    # Example OpenAI client with JSON mode (pseudo; wire your real client)
    from openai import OpenAI
    _client = OpenAI()

    def _llm_structured_json(prompt: str) -> dict:
        resp = _client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        txt = resp.choices[0].message.content
        return json.loads(txt)
else:
    def _llm_structured_json(prompt: str) -> dict:
        # Fallback mock (for offline dev). Returns empty dict; rules will fill.
        return {}


# ---- Rule-based fallback extractors -----------------------------------------
DATE_PATTERN = r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})"

PARTY_PATTERNS = [
    r"between\s+(?P<a>[A-Z][\w&.,'\- ]+)\s+and\s+(?P<b>[A-Z][\w&.,'\- ]+)",
    r"this\s+agreement\s+is\s+made\s+by\s+and\s+between\s+(?P<a>.+?)\s+and\s+(?P<b>.+?)\.",
]

LAW_PATTERNS = [
    r"governing\s+law\s*(?:of|:)\s*([A-Za-z ,\-()]+)",
    r"this\s+agreement\s+shall\s+be\s+governed\s+by\s+the\s+laws\s+of\s+([A-Za-z ,\-()]+)",
]

MONEY_PATTERN = r"\b(USD|QAR|AED|SAR|EUR|GBP|\$|QAR)\s?([0-9,.]+)\b"


def _rules_extract(text: str, lang_hint: Optional[str] = None) -> ContractExtraction:
    parties = []
    for pat in PARTY_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            a = m.groupdict().get("a", "").strip(" .,:\n")
            b = m.groupdict().get("b", "").strip(" .,:\n")
            if a: parties.append(Party(name=a))
            if b: parties.append(Party(name=b))
            break

    eff = None
    exp = None
    # Simple date guess from keywords
    m = re.search(r"effective\s+date[:\s]*" + DATE_PATTERN, text, re.I)
    if m: eff = m.group(1)
    m = re.search(r"(expiry|expiration|end)\s+date[:\s]*" + DATE_PATTERN, text, re.I)
    if m: exp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)

    law = None
    for pat in LAW_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            law = m.group(1).strip(" .,\n")
            break

    # Obligations — naive: lines with shall/must
    obligations = []
    for line in text.splitlines():
        if re.search(r"\b(shall|must|will)\b", line, re.I) and len(line) > 30:
            obligations.append(Obligation(text=line.strip()))

    # Financials
    financials = []
    for m in re.finditer(MONEY_PATTERN, text):
        currency, amount = m.group(1), m.group(2)
        financials.append(MoneyTerm(label="Payment", amount=amount, currency=currency, text=m.group(0)))

    return ContractExtraction(
        parties=parties,
        effective_date=eff,
        expiry_date=exp,
        renewals=None,
        governing_law=law,
        obligations=obligations[:10],
        financials=financials[:10],
        signatures_present=("signature" in text.lower() or "signed" in text.lower()),
        raw_summary=None,
    )


# ---- Public entry ------------------------------------------------------------

def run(text: str, use_llm: bool = True, fallback_rules: bool = True, lang_hint: Optional[str] = None) -> ContractExtraction:
    data = {}
    if use_llm:
        try:
            prompt = EXTRACT_JSON_PROMPT.format(TEXT=text[:8000])
            data = _llm_structured_json(prompt) or {}
        except Exception:
            data = {}

    # If LLM failed or fields are thin, enrich with rules
    if fallback_rules:
        rules = _rules_extract(text, lang_hint=lang_hint)
        # Merge: prefer LLM values if present
        def pick(a, b):
            return a if a not in (None, [], "") else b
        merged = ContractExtraction(
            parties=rules.parties if not data.get("parties") else [Party(**p) for p in data["parties"]],
            effective_date=pick(data.get("effective_date"), rules.effective_date),
            expiry_date=pick(data.get("expiry_date"), rules.expiry_date),
            renewals=pick(data.get("renewals"), rules.renewals),
            governing_law=pick(data.get("governing_law"), rules.governing_law),
            obligations=rules.obligations if not data.get("obligations") else [Obligation(**o) for o in data["obligations"]],
            financials=rules.financials if not data.get("financials") else [MoneyTerm(**m) for m in data["financials"]],
            signatures_present=pick(data.get("signatures_present"), rules.signatures_present),
            raw_summary=data.get("raw_summary", None),
        )
        return merged

    # LLM-only path
    return ContractExtraction(**data)


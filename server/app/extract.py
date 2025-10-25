# # # server/app/extract.py
# # from .models import ContractExtraction
# # from . import prompts
# # # plug your LLM client here

# # def llm_json(prompt: str) -> dict:
# #     # call your LLM with JSON mode or regex cleanup
# #     # return parsed dict
# #     return {}

# # def run(text: str) -> ContractExtraction:
# #     # if long, take top N chunks (e.g., first 3k-4k chars)
# #     chunk = text[:8000]
# #     data = llm_json(prompts.EXTRACT_PROMPT.format(chunk=chunk))
# #     # minimal fallback if LLM fails
# #     data.setdefault("parties", [])
# #     data.setdefault("obligations", [])
# #     data.setdefault("financials", [])
# #     return ContractExtraction(**data)


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


# # # ============================= extract.py ====================================
# # import json
# # import os
# # import re
# # from typing import Optional
# # from .models import ContractExtraction, Party, Obligation, MoneyTerm
# # from .prompts import EXTRACT_JSON_PROMPT

# # # ---- LLM client adapter (swap in your provider) -----------------------------
# # USE_OPENAI = os.getenv("USE_OPENAI_JSON", "0") == "1"

# # if USE_OPENAI:
# #     # Example OpenAI client with JSON mode (pseudo; wire your real client)
# #     from openai import OpenAI
# #     _client = OpenAI()

# #     def _llm_structured_json(prompt: str) -> dict:
# #         resp = _client.chat.completions.create(
# #             model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
# #             response_format={"type": "json_object"},
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0.1,
# #         )
# #         txt = resp.choices[0].message.content
# #         return json.loads(txt)
# # else:
# #     def _llm_structured_json(prompt: str) -> dict:
# #         # Fallback mock (for offline dev). Returns empty dict; rules will fill.
# #         return {}


# # # ---- Rule-based fallback extractors -----------------------------------------
# # DATE_PATTERN = r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})"

# # PARTY_PATTERNS = [
# #     r"between\s+(?P<a>[A-Z][\w&.,'\- ]+)\s+and\s+(?P<b>[A-Z][\w&.,'\- ]+)",
# #     r"this\s+agreement\s+is\s+made\s+by\s+and\s+between\s+(?P<a>.+?)\s+and\s+(?P<b>.+?)\.",
# # ]

# # LAW_PATTERNS = [
# #     r"governing\s+law\s*(?:of|:)\s*([A-Za-z ,\-()]+)",
# #     r"this\s+agreement\s+shall\s+be\s+governed\s+by\s+the\s+laws\s+of\s+([A-Za-z ,\-()]+)",
# # ]

# # MONEY_PATTERN = r"\b(USD|QAR|AED|SAR|EUR|GBP|\$|QAR)\s?([0-9,.]+)\b"


# # def _rules_extract(text: str, lang_hint: Optional[str] = None) -> ContractExtraction:
# #     parties = []
# #     for pat in PARTY_PATTERNS:
# #         m = re.search(pat, text, re.I)
# #         if m:
# #             a = m.groupdict().get("a", "").strip(" .,:\n")
# #             b = m.groupdict().get("b", "").strip(" .,:\n")
# #             if a: parties.append(Party(name=a))
# #             if b: parties.append(Party(name=b))
# #             break

# #     eff = None
# #     exp = None
# #     # Simple date guess from keywords
# #     m = re.search(r"effective\s+date[:\s]*" + DATE_PATTERN, text, re.I)
# #     if m: eff = m.group(1)
# #     m = re.search(r"(expiry|expiration|end)\s+date[:\s]*" + DATE_PATTERN, text, re.I)
# #     if m: exp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)

# #     law = None
# #     for pat in LAW_PATTERNS:
# #         m = re.search(pat, text, re.I)
# #         if m:
# #             law = m.group(1).strip(" .,\n")
# #             break

# #     # Obligations — naive: lines with shall/must
# #     obligations = []
# #     for line in text.splitlines():
# #         if re.search(r"\b(shall|must|will)\b", line, re.I) and len(line) > 30:
# #             obligations.append(Obligation(text=line.strip()))

# #     # Financials
# #     financials = []
# #     for m in re.finditer(MONEY_PATTERN, text):
# #         currency, amount = m.group(1), m.group(2)
# #         financials.append(MoneyTerm(label="Payment", amount=amount, currency=currency, text=m.group(0)))

# #     return ContractExtraction(
# #         parties=parties,
# #         effective_date=eff,
# #         expiry_date=exp,
# #         renewals=None,
# #         governing_law=law,
# #         obligations=obligations[:10],
# #         financials=financials[:10],
# #         signatures_present=("signature" in text.lower() or "signed" in text.lower()),
# #         raw_summary=None,
# #     )


# # # ---- Public entry ------------------------------------------------------------

# # def run(text: str, use_llm: bool = True, fallback_rules: bool = True, lang_hint: Optional[str] = None) -> ContractExtraction:
# #     data = {}
# #     if use_llm:
# #         try:
# #             prompt = EXTRACT_JSON_PROMPT.format(TEXT=text[:8000])
# #             data = _llm_structured_json(prompt) or {}
# #         except Exception:
# #             data = {}

# #     # If LLM failed or fields are thin, enrich with rules
# #     if fallback_rules:
# #         rules = _rules_extract(text, lang_hint=lang_hint)
# #         # Merge: prefer LLM values if present
# #         def pick(a, b):
# #             return a if a not in (None, [], "") else b
# #         merged = ContractExtraction(
# #             parties=rules.parties if not data.get("parties") else [Party(**p) for p in data["parties"]],
# #             effective_date=pick(data.get("effective_date"), rules.effective_date),
# #             expiry_date=pick(data.get("expiry_date"), rules.expiry_date),
# #             renewals=pick(data.get("renewals"), rules.renewals),
# #             governing_law=pick(data.get("governing_law"), rules.governing_law),
# #             obligations=rules.obligations if not data.get("obligations") else [Obligation(**o) for o in data["obligations"]],
# #             financials=rules.financials if not data.get("financials") else [MoneyTerm(**m) for m in data["financials"]],
# #             signatures_present=pick(data.get("signatures_present"), rules.signatures_present),
# #             raw_summary=data.get("raw_summary", None),
# #         )
# #         return merged

# #     # LLM-only path
# #     return ContractExtraction(**data)



# # ============================= extract.py ====================================
# import json
# import os
# import re
# from typing import Optional
# from .models import ContractExtraction, Party, Obligation, MoneyTerm
# from .prompts import EXTRACT_JSON_PROMPT

# # ---- LLM client adapter (Bytez: google/gemma-3-1b-it) -----------------------
# USE_BYTEZ = os.getenv("USE_BYTEZ", "1") == "1"
# BYTEZ_MODEL = os.getenv("BYTEZ_MODEL", "google/gemma-3-1b-it")

# _llm_ready = False
# if USE_BYTEZ:
#     try:
#         from bytez import Bytez
#         _bytez = Bytez(os.getenv("BYTEZ_API_KEY", ""))
#         _model = _bytez.model(BYTEZ_MODEL)
#         _llm_ready = True
#     except Exception:
#         _llm_ready = False


# def _coerce_json(text: str) -> dict:
#     """Try to parse JSON; if the model returned extra text, strip to the first JSON object."""
#     if not text:
#         return {}
#     try:
#         return json.loads(text)
#     except Exception:
#         pass
#     # Extract first {...} block
#     m = re.search(r"\{[\s\S]*\}", text)
#     if m:
#         try:
#             return json.loads(m.group(0))
#         except Exception:
#             return {}
#     return {}


# def _llm_structured_json(prompt: str) -> dict:
#     if not (_llm_ready and USE_BYTEZ):
#         return {}
#     # Ask for STRICT JSON only
#     system = {
#         "role": "system",
#         "content": (
#             "You are a contract parser. Output STRICT JSON only, no prose, no markdown. "
#             "Keys: parties[name,role], effective_date, expiry_date, renewals, governing_law, "
#             "obligations[party,text], financials[label,amount,currency,text], signatures_present, raw_summary."
#         ),
#     }
#     user = {"role": "user", "content": prompt}
#     try:
#         output, error = _model.run([system, user])
#         if error:
#             return {}
#         # Bytez may return dict, list, or string; handle all
#         if isinstance(output, dict):
#             return output
#         if isinstance(output, list):
#             for item in output:
#                 if isinstance(item, dict) and "content" in item:
#                     maybe = item["content"]
#                     if isinstance(maybe, (str, bytes)):
#                         return _coerce_json(maybe if isinstance(maybe, str) else maybe.decode())
#             return {}
#         if isinstance(output, (str, bytes)):
#             text = output if isinstance(output, str) else output.decode()
#             return _coerce_json(text)
#         return {}
#     except Exception:
#         return {}


# # ---- Rule-based fallback extractors -----------------------------------------
# DATE_PATTERN = r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})"

# PARTY_PATTERNS = [
#     r"between\s+(?P<a>[A-Z][\w&.,'\- ]+)\s+and\s+(?P<b>[A-Z][\w&.,'\- ]+)",
#     r"this\s+agreement\s+is\s+made\s+by\s+and\s+between\s+(?P<a>.+?)\s+and\s+(?P<b>.+?)\.",
# ]

# LAW_PATTERNS = [
#     r"governing\s+law\s*(?:of|:)\s*([A-Za-z ,\-()]+)",
#     r"this\s+agreement\s+shall\s+be\s+governed\s+by\s+the\s+laws\s+of\s+([A-Za-z ,\-()]+)",
# ]

# MONEY_PATTERN = r"\b(USD|QAR|AED|SAR|EUR|GBP|\$|QAR)\s?([0-9,.]+)\b"


# def _rules_extract(text: str, lang_hint: Optional[str] = None) -> ContractExtraction:
#     parties = []
#     for pat in PARTY_PATTERNS:
#         m = re.search(pat, text, re.I)
#         if m:
#             a = m.groupdict().get("a", "").strip(" .,:\n")
#             b = m.groupdict().get("b", "").strip(" .,:\n")
#             if a: parties.append(Party(name=a))
#             if b: parties.append(Party(name=b))
#             break

#     eff = None
#     exp = None
#     m = re.search(r"effective\s+date[:\s]*" + DATE_PATTERN, text, re.I)
#     if m: eff = m.group(1)
#     m = re.search(r"(expiry|expiration|end)\s+date[:\s]*" + DATE_PATTERN, text, re.I)
#     if m: exp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)

#     law = None
#     for pat in LAW_PATTERNS:
#         m = re.search(pat, text, re.I)
#         if m:
#             law = m.group(1).strip(" .,\n")
#             break

#     obligations = []
#     for line in text.splitlines():
#         if re.search(r"\b(shall|must|will)\b", line, re.I) and len(line) > 30:
#             obligations.append(Obligation(text=line.strip()))

#     financials = []
#     for m in re.finditer(MONEY_PATTERN, text):
#         currency, amount = m.group(1), m.group(2)
#         financials.append(MoneyTerm(label="Payment", amount=amount, currency=currency, text=m.group(0)))

#     return ContractExtraction(
#         parties=parties,
#         effective_date=eff,
#         expiry_date=exp,
#         renewals=None,
#         governing_law=law,
#         obligations=obligations[:10],
#         financials=financials[:10],
#         signatures_present=("signature" in text.lower() or "signed" in text.lower()),
#         raw_summary=None,
#     )


# # ---- Public entry ------------------------------------------------------------

# def run(text: str, use_llm: bool = True, fallback_rules: bool = True, lang_hint: Optional[str] = None) -> ContractExtraction:
#     data = {}
#     if use_llm:
#         try:
#             prompt = EXTRACT_JSON_PROMPT.format(TEXT=text[:8000])
#             data = _llm_structured_json(prompt) or {}
#         except Exception:
#             data = {}

#     if fallback_rules:
#         rules = _rules_extract(text, lang_hint=lang_hint)
#         def pick(a, b):
#             return a if a not in (None, [], "") else b
#         merged = ContractExtraction(
#             parties=rules.parties if not data.get("parties") else [Party(**p) for p in data["parties"]],
#             effective_date=pick(data.get("effective_date"), rules.effective_date),
#             expiry_date=pick(data.get("expiry_date"), rules.expiry_date),
#             renewals=pick(data.get("renewals"), rules.renewals),
#             governing_law=pick(data.get("governing_law"), rules.governing_law),
#             obligations=rules.obligations if not data.get("obligations") else [Obligation(**o) for o in data["obligations"]],
#             financials=rules.financials if not data.get("financials") else [MoneyTerm(**m) for m in data["financials"]],
#             signatures_present=pick(data.get("signatures_present"), rules.signatures_present),
#             raw_summary=data.get("raw_summary", None),
#         )
#         return merged

#     return ContractExtraction(**data)


import json
import os
import re
from .summary_helper import generate_summary
# from .gemini_helper import call_gemini_json, EXTRACTION_SCHEMA
from .gemini_helper import call_gemini_extract


from typing import Optional, List, Tuple
from .models import ContractExtraction, Party, Obligation, MoneyTerm, Penalty
from .prompts import EXTRACT_JSON_PROMPT


def _llm_structured_json(prompt: str) -> dict:
    # Our prompt already inserts TEXT; here prompt == EXTRACT_JSON_PROMPT.format(TEXT=...)
    # We just feed the raw contract text to the strict caller, not the whole instruction.
    # Pull the text back out of the prompt to avoid nested instructions.
    # Simpler: change caller to pass raw text directly:
    return {}




# ------------------- Regex helpers & patterns --------------------------------
DATE_PATTERN = r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})"
CURRENCY = r"USD|QAR|AED|SAR|EUR|GBP|\$|€|£"
AMOUNT = r"[0-9][0-9,]*(?:\.[0-9]{2})?"
MONEY_PATTERN = rf"\b({CURRENCY})\s?({AMOUNT})\b"
NET_PATTERN = r"\bnet\s*(\d{1,3})\b"
WITHIN_DAYS_PATTERN = r"within\s*(\d{1,3})\s*days"
MONTHLY_PATTERN = r"\bmonthly\b|\beach\s+month\b"
PENALTY_RATE_PATTERN = r"(\d+(?:\.\d+)?)%\s*(?:per\s*(?:month|annum|year))"
LATE_KEYWORDS = r"late|delay|overdue|penalt|interest"

PARTY_PATTERNS = [
    r"between\s+(?P<a>[A-Z][\w&.,'\- ]+)\s+and\s+(?P<b>[A-Z][\w&.,'\- ]+)",
    r"this\s+agreement\s+is\s+made\s+by\s+and\s+between\s+(?P<a>.+?)\s+and\s+(?P<b>.+?)\.",
]

LAW_PATTERNS = [
    r"governing\s+law\s*(?:of|:)\s*([A-Za-z ,\-()]+)",
    r"this\s+agreement\s+shall\s+be\s+governed\s+by\s+the\s+laws\s+of\s+([A-Za-z ,\-()]+)",
]

JURIS_PATTERNS = [
    r"exclusive\s+jurisdiction\s+of\s+([A-Za-z ,\-()]+)",
    r"courts?\s+of\s+([A-Za-z ,\-()]+)",
    r"venue\s+in\s+([A-Za-z ,\-()]+)",
]

RENEW_PATTERNS = [
    r"renew(al|s)?\s+for\s+(\d+\s*(?:month|months|year|years))",
    r"auto(?:matic(?:ally)?)?\s*renew[s]?\s*(?:for\s*)?(\d+\s*(?:month|months|year|years))",
    r"renewal\s+date[:\s]*" + DATE_PATTERN,
]

# ------------------- Rule-based extractors -----------------------------------
def _extract_parties(text: str) -> List[Party]:
    parties: List[Party] = []
    for pat in PARTY_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            a = m.groupdict().get("a", "").strip(" .,:\n")
            b = m.groupdict().get("b", "").strip(" .,:\n")
            if a: parties.append(Party(name=a))
            if b: parties.append(Party(name=b))
            break
    return parties

def _extract_dates(text: str):
    eff = exp = renewal_date = renewals = None
    auto = None
    m = re.search(r"effective\s+date[:\s]*" + DATE_PATTERN, text, re.I)
    if m: eff = m.group(1)
    m = re.search(r"(expiry|expiration|end)\s+date[:\s]*" + DATE_PATTERN, text, re.I)
    if m: exp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
    for pat in RENEW_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            renewals = m.group(0).strip()
            if re.search(DATE_PATTERN, renewals):
                renewal_date = re.search(DATE_PATTERN, renewals).group(0)
            break
    if re.search(r"auto(?:matic(?:ally)?)?\s*renew", text, re.I): auto = True
    elif re.search(r"shall\s+not\s+auto\s*renew|no\s+auto\s*renew", text, re.I): auto = False
    return eff, exp, renewal_date, auto, renewals

def _extract_law_and_jurisdiction(text: str):
    law = None
    for pat in LAW_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            law = m.group(1).strip(" .,\n")
            break
    juris = None
    for pat in JURIS_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            juris = m.group(1).strip(" .,\n")
            break
    return law, juris

def _extract_obligations(text: str, parties: List[Party]) -> List[Obligation]:
    party_names = [p.name for p in parties]
    aliases = ["supplier", "client", "company", "customer", "vendor", "msp", "provider", "licensee", "licensor"]
    obligations: List[Obligation] = []
    for line in text.splitlines():
        if re.search(r"\b(shall|must|will)\b", line, re.I) and len(line) > 30:
            who = None
            low = line.lower()
            # map to explicit party if mentioned
            for n in party_names:
                first = n.split()[0].lower() if n else None
                if first and first in low:
                    who = n; break
            # fall back to alias
            if not who:
                for a in aliases:
                    if re.search(rf"\b{a}\b", low):
                        who = a.title(); break
            obligations.append(Obligation(party=who, text=line.strip()))
    return obligations[:15]

def _extract_financials(text: str) -> List[MoneyTerm]:
    fins: List[MoneyTerm] = []
    for m in re.finditer(MONEY_PATTERN, text):
        currency, amount = m.group(1), m.group(2)
        # sentence window
        start = text.rfind(".", 0, m.start()) + 1
        end = text.find(".", m.end())
        end = end if end != -1 else m.end() + 100
        sent = text[start:end]

        schedule = None
        if re.search(NET_PATTERN, sent, re.I):
            d = re.search(NET_PATTERN, sent, re.I).group(1)
            schedule = f"net {d}"
        elif re.search(WITHIN_DAYS_PATTERN, sent, re.I):
            d = re.search(WITHIN_DAYS_PATTERN, sent, re.I).group(1)
            schedule = f"within {d} days"
        elif re.search(MONTHLY_PATTERN, sent, re.I):
            schedule = "monthly"

        penalties: List[Penalty] = []
        window = text[max(0, start-80):min(len(text), end+150)]
        if re.search(LATE_KEYWORDS, window, re.I):
            rate_m = re.search(PENALTY_RATE_PATTERN, window, re.I)
            amt_m = re.search(MONEY_PATTERN, window)
            penalties.append(Penalty(
                type="late/interest",
                amount=amt_m.group(2) if amt_m else None,
                rate=rate_m.group(0) if rate_m else None,
                condition="late payment" if re.search(r"late|overdue", window, re.I) else None,
                text=re.sub(r"\s+", " ", window).strip()
            ))

        fins.append(MoneyTerm(
            label="Payment",
            amount=amount,
            currency=currency,
            schedule=schedule,
            penalties=penalties,
            text=m.group(0)
        ))
    return fins[:10]

def _rules_extract(text: str, lang_hint: Optional[str] = None) -> ContractExtraction:
    parties = _extract_parties(text)
    eff, exp, renewal_date, auto, renewals = _extract_dates(text)
    law, juris = _extract_law_and_jurisdiction(text)
    obligations = _extract_obligations(text, parties)
    financials = _extract_financials(text)

    return ContractExtraction(
        parties=parties,
        effective_date=eff,
        expiry_date=exp,
        renewal_date=renewal_date,
        auto_renewal=auto,
        renewals=renewals,
        governing_law=law,
        jurisdiction=juris,
        obligations=obligations,
        financials=financials,
        signatures_present=("signature" in text.lower() or "signed" in text.lower()),
        raw_summary=None,
    )


def _normalize_extraction_payload(d: dict) -> dict:
    """
    Coerce a loose LLM JSON into the strict ContractExtraction schema.
    - parties: list[str] -> [{"name": str, "role": None}]
    - obligations: list[str] -> [{"party": None, "text": str}]
    - financials: map variant keys to {label, text, amount, currency, schedule, penalties[]}
    - renewals: list[dict] -> compact string
    - ensure all required keys exist
    """
    if not isinstance(d, dict):
        d = {}

    def ensure_keys(obj: dict, defaults: dict) -> dict:
        out = {**defaults}
        if isinstance(obj, dict):
            for k in defaults.keys():
                if k in obj:
                    out[k] = obj[k]
        return out

    base = {
        "parties": [],
        "effective_date": None,
        "expiry_date": None,
        "renewal_date": None,
        "auto_renewal": None,
        "renewals": None,
        "governing_law": None,
        "jurisdiction": None,
        "obligations": [],
        "financials": [],
        "signatures_present": None,
        "raw_summary": None,
    }
    d = ensure_keys(d, base)

    # parties
    parties = d.get("parties") or []
    norm_parties = []
    if isinstance(parties, list):
        for p in parties:
            if isinstance(p, str):
                norm_parties.append({"name": p, "role": None})
            elif isinstance(p, dict):
                name = p.get("name") or p.get("party") or p.get("entity") or ""
                role = p.get("role") or p.get("type") or None
                if name:
                    norm_parties.append({"name": name, "role": role})
    d["parties"] = norm_parties

    # obligations
    obligations = d.get("obligations") or []
    norm_obl = []
    if isinstance(obligations, list):
        for o in obligations:
            if isinstance(o, str):
                norm_obl.append({"party": None, "text": o})
            elif isinstance(o, dict):
                party = o.get("party") or o.get("owner") or o.get("responsible") or None
                text = (
                    o.get("text")
                    or o.get("obligation")
                    or o.get("deliverable")
                    or o.get("clause")
                    or None
                )
                if isinstance(text, str) and text.strip():
                    norm_obl.append({"party": party, "text": text.strip()})
    d["obligations"] = norm_obl

    # renewals (some models return list/dict)
    renewals = d.get("renewals")
    if isinstance(renewals, list):
        # turn into a compact sentence
        parts = []
        for item in renewals:
            if isinstance(item, dict):
                frag = []
                for k, v in item.items():
                    if v is not None and v != "":
                        frag.append(f"{k}: {v}")
                if frag:
                    parts.append("; ".join(frag))
            elif isinstance(item, str):
                parts.append(item)
        d["renewals"] = "; ".join(parts) if parts else None
    elif isinstance(renewals, dict):
        d["renewals"] = "; ".join([f"{k}: {v}" for k, v in renewals.items() if v]) or None
    elif renewals is not None and not isinstance(renewals, str):
        d["renewals"] = str(renewals)

    # financials
    def to_penalty_list(p):
        # normalize penalties into [{"type","amount","rate","condition","text"}]
        out = []
        if isinstance(p, list):
            items = p
        else:
            items = [p] if p else []
        for it in items:
            if isinstance(it, dict):
                text = it.get("text") or it.get("clause") or it.get("description")
                entry = {
                    "type": it.get("type"),
                    "amount": it.get("amount"),
                    "rate": it.get("rate"),
                    "condition": it.get("condition"),
                    "text": text or "",
                }
                # require at least text to satisfy model
                if not entry["text"]:
                    # synthesize if needed
                    fields = [f"{k}={v}" for k, v in it.items() if v and k != "text"]
                    entry["text"] = "; ".join(fields) if fields else "Penalty"
                out.append(entry)
            elif isinstance(it, str):
                out.append({"type": None, "amount": None, "rate": None, "condition": None, "text": it})
        return out

    fin = d.get("financials") or []
    norm_fin = []
    if isinstance(fin, list):
        for f in fin:
            if isinstance(f, dict):
                # Map common variants
                label = f.get("label") or f.get("type") or f.get("category") \
                        or ("Payment" if ("payment" in " ".join(f.keys()).lower()) else "Financial")
                text = f.get("text") or f.get("payment_terms") or f.get("terms") \
                       or f.get("clause") or ""
                amount = f.get("amount") or f.get("value") or f.get("fee") or None
                currency = f.get("currency") or f.get("curr") or None
                schedule = f.get("schedule") or f.get("due") or f.get("timeline") or None
                penalties = to_penalty_list(f.get("penalties"))
                norm_fin.append({
                    "label": label,
                    "amount": amount,
                    "currency": currency,
                    "schedule": schedule,
                    "penalties": penalties,
                    "text": text or (f"{currency or ''} {amount}" if amount else "N/A")
                })
            elif isinstance(f, str):
                norm_fin.append({
                    "label": "Financial",
                    "amount": None,
                    "currency": None,
                    "schedule": None,
                    "penalties": [],
                    "text": f
                })
    d["financials"] = norm_fin

    # signatures_present should be bool or null
    sig = d.get("signatures_present")
    if isinstance(sig, str):
        low = sig.lower()
        if low in ("true", "yes", "present", "signed"):
            d["signatures_present"] = True
        elif low in ("false", "no", "absent", "unsigned"):
            d["signatures_present"] = False
        else:
            d["signatures_present"] = None

    # raw_summary: keep as-is if string; else drop
    if not isinstance(d.get("raw_summary"), str):
        d["raw_summary"] = None

    # governing_law / jurisdiction: coerce non-strings
    for k in ("governing_law", "jurisdiction", "effective_date", "expiry_date", "renewal_date"):
        if d.get(k) is not None and not isinstance(d[k], str):
            d[k] = str(d[k])

    return d


def run(text: str, use_llm: bool = True, fallback_rules: bool = True, lang_hint: Optional[str] = None) -> ContractExtraction:
    data = {}
    if use_llm:
        try:
            data = call_gemini_extract(text) or {}
            data = _normalize_extraction_payload(data)  
            data = enrich_extraction_with_rules(data, text)   
        except Exception:
            data = {}

    if fallback_rules:
        rules = _rules_extract(text, lang_hint=lang_hint)
        def pick(a, b): return a if a not in (None, [], "") else b
        merged = ContractExtraction(
            parties=rules.parties if not data.get("parties") else [Party(**p) for p in data["parties"]],
            effective_date=pick(data.get("effective_date"), rules.effective_date),
            expiry_date=pick(data.get("expiry_date"), rules.expiry_date),
            renewal_date=pick(data.get("renewal_date"), rules.renewal_date),
            auto_renewal=pick(data.get("auto_renewal"), rules.auto_renewal),
            renewals=pick(data.get("renewals"), rules.renewals),
            governing_law=pick(data.get("governing_law"), rules.governing_law),
            jurisdiction=pick(data.get("jurisdiction"), rules.jurisdiction),
            obligations=rules.obligations if not data.get("obligations") else [Obligation(**o) for o in data["obligations"]],
            financials=rules.financials if not data.get("financials") else [MoneyTerm(**m) for m in data["financials"]],
            signatures_present=pick(data.get("signatures_present"), rules.signatures_present),
            raw_summary=data.get("raw_summary", None),
        )
        if not merged.raw_summary:
            merged.raw_summary = generate_summary(text, merged)
        return merged

    only_llm = ContractExtraction(**data)
    if not only_llm.raw_summary:
        only_llm.raw_summary = generate_summary(text, only_llm)
    return only_llm

import re

_MONEY = re.compile(r"\b([A-Z]{3})\s?([\d,]+(?:\.\d+)?)\b")               # e.g., QAR 45,000
_INTEREST = re.compile(r"\b(\d+(?:\.\d+)?)%\s*(?:per\s*)?(month|annum|year)\b", re.I)
_SCHEDULE = re.compile(r"\bwithin\s+\d+\s+(?:days|weeks|months)\b", re.I)
_LATE = re.compile(r"\blate\s+payment[s]?\b", re.I)
_ROLE_FROM_NAME = re.compile(r"\((Supplier|Client|Vendor|Customer|Licensor|Licensee)\)", re.I)

def enrich_extraction_with_rules(data: dict, text: str) -> dict:
    # Parties: infer role from parentheses in name if missing
    for p in data.get("parties", []):
        if p.get("role") in (None, "") and isinstance(p.get("name"), str):
            m = _ROLE_FROM_NAME.search(p["name"])
            if m: p["role"] = m.group(1).capitalize()

    # Financials: ensure amount/currency/schedule/penalties where obvious in text
    if not data.get("financials"):
        data["financials"] = [{"label":"Payment","amount":None,"currency":None,"schedule":None,"penalties":[],"text":""}]

    f0 = data["financials"][0]
    if not f0.get("text"):
        # If we have an obligation about payment, harvest that line as text
        pay_line = next((o["text"] for o in data.get("obligations", []) if "pay" in o.get("text","").lower()), "")
        f0["text"] = pay_line

    if not f0.get("currency") or not f0.get("amount"):
        m = _MONEY.search(text)
        if m:
            f0["currency"] = f0.get("currency") or m.group(1)
            f0["amount"] = f0.get("amount") or m.group(2)

    if not f0.get("schedule"):
        m = _SCHEDULE.search(text)
        if m:
            f0["schedule"] = m.group(0)

    # Penalties: interest/late payments
    if not f0.get("penalties"):
        rate = None
        m = _INTEREST.search(text)
        if m:
            rate = f"{m.group(1)}% per {m.group(2)}"
        if rate or _LATE.search(text):
            f0["penalties"] = [{
                "type": "late/interest",
                "amount": None,
                "rate": rate,
                "condition": "late payment",
                "text": "late payment interest" if not rate else f"late payments accrue {rate}"
            }]

    return data


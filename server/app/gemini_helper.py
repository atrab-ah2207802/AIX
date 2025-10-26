# # # server/app/gemini_helper.py
# # import os, re, json, asyncio
# # import google.genai as genai

# # api_key = os.getenv("GEMINI_API_KEY", "")
# # client = genai.Client(api_key=api_key)

# # # Your extraction schema (same as earlier)
# # EXTRACTION_SCHEMA = {
# #     "type": "object",
# #     "properties": {
# #         "parties": {"type":"array","items":{"type":"object","properties":{
# #             "name":{"type":"string"},"role":{"type":["string","null"]}
# #         },"required":["name"],"additionalProperties":False}},
# #         "effective_date":{"type":["string","null"]},
# #         "expiry_date":{"type":["string","null"]},
# #         "renewal_date":{"type":["string","null"]},
# #         "auto_renewal":{"type":["boolean","null"]},
# #         "renewals":{"type":["string","null"]},
# #         "governing_law":{"type":["string","null"]},
# #         "jurisdiction":{"type":["string","null"]},
# #         "obligations":{"type":"array","items":{"type":"object","properties":{
# #             "party":{"type":["string","null"]},"text":{"type":"string"}
# #         },"required":["text"],"additionalProperties":False}},
# #         "financials":{"type":"array","items":{"type":"object","properties":{
# #             "label":{"type":"string"},"amount":{"type":["string","null"]},
# #             "currency":{"type":["string","null"]},"schedule":{"type":["string","null"]},
# #             "penalties":{"type":"array","items":{"type":"object","properties":{
# #                 "type":{"type":["string","null"]},"amount":{"type":["string","null"]},
# #                 "rate":{"type":["string","null"]},"condition":{"type":["string","null"]},
# #                 "text":{"type":"string"}
# #             },"required":["text"],"additionalProperties":False}},
# #             "text":{"type":"string"}
# #         },"required":["label","text"],"additionalProperties":False}},
# #         "signatures_present":{"type":["boolean","null"]},
# #         "raw_summary":{"type":["string","null"]}
# #     },
# #     "required":["parties","effective_date","expiry_date","renewal_date","auto_renewal",
# #                 "renewals","governing_law","jurisdiction","obligations","financials",
# #                 "signatures_present","raw_summary"],
# #     "additionalProperties": False
# # }

# # def _fallback_minimal_payload() -> dict:
# #     return {
# #         "parties": [], "effective_date": None, "expiry_date": None,
# #         "renewal_date": None, "auto_renewal": None, "renewals": None,
# #         "governing_law": None, "jurisdiction": None,
# #         "obligations": [], "financials": [],
# #         "signatures_present": None, "raw_summary": None
# #     }

# # def _repair_json_string(s: str) -> str:
# #     if not s: return "{}"
# #     # strip code fences
# #     s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.I)
# #     # grab first {...} block if extra text exists
# #     m = re.search(r"\{[\s\S]*\}", s)
# #     if m: s = m.group(0)
# #     # remove trailing commas before } or ]
# #     s = re.sub(r",\s*(\}|\])", r"\1", s)
# #     # ensure quotes are double quotes for keys
# #     # (light heuristic; better to rely on model, but this helps)
# #     return s

# # def _strict_prompt(contract_text: str) -> str:
# #     return (
# #         "CRITICAL: Return ONLY valid JSON parsable by json.loads().\n"
# #         "RULES:\n"
# #         "1) Double quotes for all keys/strings\n"
# #         "2) Escape inner quotes with \\\" \n"
# #         "3) No trailing commas\n"
# #         "4) No markdown / code fences\n"
# #         "5) Properly matched brackets { } and [ ]\n"
# #         "6) If a field is missing, use null or []\n\n"
# #         "Expected top-level keys: parties, effective_date, expiry_date, renewal_date, auto_renewal, "
# #         "renewals, governing_law, jurisdiction, obligations, financials, signatures_present, raw_summary.\n\n"
# #         "Contract text:\n" + contract_text[:12000]
# #     )

# # def call_gemini_text(prompt: str, model_name: str = "gemini-2.0-flash") -> str | None:
# #     """Return plain text from Gemini (used for summaries)."""
# #     try:
# #         resp = client.models.generate_content(model=model_name, contents=prompt)
# #         return (resp.text or "").strip()
# #     except Exception as e:
# #         print("[Gemini Text] Error:", e)
# #         return None


# # def call_gemini_json_strict(contract_text: str, model_name: str = "gemini-2.0-flash") -> dict:
# #     """
# #     Robust JSON caller for Python 3.10:
# #     - Calls Gemini for JSON
# #     - Repairs common formatting issues
# #     - Validates with json.loads
# #     - Returns minimal fallback on error
# #     """
# #     prompt = _strict_prompt(contract_text)

# #     try:
# #         # Run the blocking call in a thread and apply a timeout using asyncio.wait_for
# #         async def _run():
# #             loop = asyncio.get_running_loop()
# #             resp = await asyncio.to_thread(
# #                 client.models.generate_content,
# #                 model=model_name,
# #                 contents=prompt,
# #                 generation_config={
# #                     # Prefer JSON mime if your key supports it; if not, this is ignored gracefully
# #                     "response_mime_type": "application/json"
# #                 }
# #             )
# #             return resp

# #         # Create a short-lived event loop if we're in a sync context
# #         try:
# #             loop = asyncio.get_event_loop()
# #         except RuntimeError:
# #             loop = asyncio.new_event_loop()
# #             asyncio.set_event_loop(loop)

# #         resp = loop.run_until_complete(asyncio.wait_for(_run(), timeout=30))
# #         text = (resp.text or "").strip()

# #         repaired = _repair_json_string(text)
# #         try:
# #             parsed = json.loads(repaired)
# #             # Ensure required keys exist (fill if missing)
# #             payload = _fallback_minimal_payload()
# #             if isinstance(parsed, dict):
# #                 payload.update({k: parsed.get(k, payload[k]) for k in payload.keys()})
# #             return payload
# #         except json.JSONDecodeError:
# #             return _fallback_minimal_payload()

# #     except Exception as e:
# #         print("[Gemini strict JSON] error:", e)
# #         return _fallback_minimal_payload()

# import os, json, re
# import google.genai as genai

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

# REQUIRED_KEYS = [
#     "parties","effective_date","expiry_date","renewal_date","auto_renewal","renewals",
#     "governing_law","jurisdiction","obligations","financials","signatures_present","raw_summary"
# ]

# def _empty_payload():
#     return {
#         "parties": [], "effective_date": None, "expiry_date": None,
#         "renewal_date": None, "auto_renewal": None, "renewals": None,
#         "governing_law": None, "jurisdiction": None,
#         "obligations": [], "financials": [],
#         "signatures_present": None, "raw_summary": None
#     }

# def _ensure_keys(d: dict) -> dict:
#     base = _empty_payload()
#     if isinstance(d, dict):
#         for k in base.keys():
#             base[k] = d.get(k, base[k])
#     return base

# def _repair_json(s: str) -> dict:
#     if not s:
#         return {}
#     # strip code fences
#     s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.I)
#     # keep first {...}
#     m = re.search(r"\{[\s\S]*\}", s)
#     if m: s = m.group(0)
#     # remove trailing commas
#     s = re.sub(r",\s*(\}|\])", r"\1", s)
#     try:
#         return json.loads(s)
#     except Exception:
#         return {}

# def _strict_prompt(text: str) -> str:
#     return (
#         "CRITICAL: Return ONLY valid JSON parsable by json.loads().\n"
#         "Rules: double quotes for keys/strings; escape inner quotes with \\\"; "
#         "no trailing commas; no markdown; proper brackets; use null/[] when missing.\n\n"
#         "Top-level keys: parties, effective_date, expiry_date, renewal_date, auto_renewal, renewals, "
#         "governing_law, jurisdiction, obligations, financials, signatures_present, raw_summary.\n\n"
#         "Contract text:\n" + text[:12000]
#     )

# _client = None
# def _get_client() -> genai.Client:
#     global _client
#     api_key = os.getenv("GEMINI_API_KEY", "")
#     if not api_key:
#         raise RuntimeError("GEMINI_API_KEY is not set in the environment.")
#     if _client is None:
#         _client = genai.Client(api_key=api_key)
#     return _client


# def call_gemini_text(prompt: str, model_name="gemini-2.0-flash") -> str | None:
#     """Plain text (used by summary helper)."""
#     try:
#         resp = client.models.generate_content(model=model_name, contents=prompt)
#         return (resp.text or "").strip()
#     except Exception as e:
#         print("[Gemini Text] Error:", e)
#         return None

# def call_gemini_extract(text: str, model_name="gemini-2.0-flash") -> dict:
#     """
#     Synchronous, strict JSON path with logging + repair.
#     No generation_config, no asyncio → avoids event loop issues.
#     """
#     prompt = _strict_prompt(text)
#     try:
#         print("\n[Gemini] Strict JSON extract: sending prompt...")
#         resp = client.models.generate_content(model=model_name, contents=prompt)
#         raw = (resp.text or "").strip()
#         print("[Gemini] Raw response (first 800 chars):\n", raw[:800], "\n--- END RAW ---\n")
#         repaired = _repair_json(raw)
#         if repaired:
#             print("[Gemini] JSON parsed after repair.")
#         else:
#             print("[Gemini] Failed to parse JSON after repair; returning empty payload.")
#         return _ensure_keys(repaired)
#     except Exception as e:
#         print("[Gemini] Error during extract:", e)
#         return _empty_payload()


# def answer_with_gemini(question: str, contexts: list[tuple[int, str]], model_name="gemini-2.0-flash") -> str:
#     try:
#         client = _get_client()

#         # Keep the total context small (≈ 1–2k chars)
#         MAX_TOTAL = 1600
#         snips = []
#         total = 0
#         for cid, txt in contexts:
#             # take only the most relevant ~350 chars per chunk
#             snippet = txt[:350]
#             if total + len(snippet) + 10 > MAX_TOTAL:
#                 break
#             snips.append((cid, snippet))
#             total += len(snippet) + 10

#         numbered = "\n\n".join([f"[{cid}] {txt}" for cid, txt in snips])
#         prompt = (
#             "Answer the question using ONLY the provided context. "
#             "Cite sources like [#]. If not found, say so.\n\n"
#             f"Question: {question}\n\n"
#             f"Context:\n{numbered}"
#         )

#         # Use smaller, faster model if you have it:
#         # model_name = "gemini-2.0-flash-lite"
#         resp = client.models.generate_content(model=model_name, contents=prompt)
#         return (resp.text or "").strip()
#     except Exception as e:
#         print("[Gemini QA] Error:", e)
#         return "Sorry — I couldn’t answer that from the contract context."
    
# def build_qa_prompt(question: str, contexts: list[tuple[int, str]], *,
#                     max_total_chars: int = 1600, per_chunk_chars: int = 350) -> str:
#     """Create a short, citation-friendly prompt for Gemini."""
#     snips, total = [], 0
#     for cid, txt in contexts:
#         snip = txt[:per_chunk_chars]
#         if total + len(snip) + 10 > max_total_chars:
#             break
#         snips.append((cid, snip))
#         total += len(snip) + 10

#     numbered = "\n\n".join([f"[{cid}] {txt}" for cid, txt in snips])
#     prompt = (
#         "Answer the question using ONLY the provided context. "
#         "Cite supporting snippets using bracket numbers like [12]. "
#         "If the answer is not in context, say you don't find it.\n\n"
#         f"Question: {question}\n\n"
#         f"Context:\n{numbered}"
#     )
#     return prompt

# def answer_with_gemini_prompt(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
#     """Send a prebuilt prompt; return plain text answer."""
#     try:
#         client = _get_client()
#         resp = client.models.generate_content(model=model_name, contents=prompt)
#         return (resp.text or "").strip()
#     except Exception as e:
#         print("[Gemini QA] Error:", e)
#         return "Sorry — I couldn’t answer that from the contract context."

# import asyncio

# async def answer_with_timeout(prompt: str, model_name="gemini-2.0-flash", timeout_s=6):
#     client = _get_client()
#     loop = asyncio.get_running_loop()
#     def _call():
#         resp = client.models.generate_content(model=model_name, contents=prompt)
#         return (resp.text or "").strip()

#     try:
#         return await asyncio.wait_for(loop.run_in_executor(None, _call), timeout=timeout_s)
#     except Exception as e:
#         print("[Gemini QA] timeout/fail -> fallback:", e)
#         return None  # signal to fallback
## server/app/gemini_helper.py
# server/app/gemini_helper.py
import os, json, re
from typing import Optional
import google.genai as genai

_client: Optional[genai.Client] = None

def _get_client() -> genai.Client:
    global _client
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment.")
    if _client is None:
        _client = genai.Client(api_key=api_key)
    return _client

def call_gemini_text(prompt: str, model_name: str = "gemini-2.0-flash") -> str | None:
    try:
        client = _get_client()
        resp = client.models.generate_content(model=model_name, contents=prompt)
        return (resp.text or "").strip()
    except Exception as e:
        print("[Gemini Text] Error:", e)
        return None

# ---- Strict JSON extractor kept for backward compatibility ----

def _empty_payload():
    return {
        "parties": [], "effective_date": None, "expiry_date": None,
        "renewal_date": None, "auto_renewal": None, "renewals": None,
        "governing_law": None, "jurisdiction": None,
        "obligations": [], "financials": [],
        "signatures_present": None, "raw_summary": None
    }

def _repair_json(s: str) -> dict:
    if not s:
        return {}
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.I)
    m = re.search(r"\{[\s\S]*\}", s)
    if m:
        s = m.group(0)
    s = re.sub(r",\s*(\}|\])", r"\1", s)
    try:
        return json.loads(s)
    except Exception:
        return {}

def call_gemini_extract(contract_text: str, model_name: str = "gemini-2.0-flash-lite") -> dict:
    """
    Return a strict JSON payload for extraction (compatible with older import sites).
    """
    try:
        client = _get_client()
        prompt = (
            "CRITICAL: Return ONLY valid JSON parsable by json.loads().\n"
            "Rules: double quotes for keys/strings; escape inner quotes with \\\"; "
            "no trailing commas; no markdown; proper brackets; use null/[] when missing.\n\n"
            "Top-level keys: parties, effective_date, expiry_date, renewal_date, auto_renewal, renewals, "
            "governing_law, jurisdiction, obligations, financials, signatures_present, raw_summary.\n\n"
            "Contract text:\n" + contract_text[:12000]
        )
        resp = client.models.generate_content(model=model_name, contents=prompt)
        raw = (resp.text or "").strip()
        repaired = _repair_json(raw)
        print(f"[Gemini Extract] Using model: {model_name}")
        if not isinstance(repaired, dict):
            return _empty_payload()
        payload = _empty_payload()
        for k in payload.keys():
            payload[k] = repaired.get(k, payload[k])
        return payload
    except Exception as e:
        print("[Gemini Extract] Error:", e)
        return _empty_payload()

def answer_with_gemini(question: str, contexts: list[tuple[int, str]], model_name: str = "gemini-2.0-flash") -> str:
    try:
        client = _get_client()
        MAX_TOTAL = 1600
        snips: list[tuple[int, str]] = []
        total = 0
        for cid, txt in contexts:
            snippet = txt[:350]
            if total + len(snippet) + 10 > MAX_TOTAL:
                break
            snips.append((cid, snippet))
            total += len(snippet) + 10

        numbered = "\n\n".join([f"[{cid}] {txt}" for cid, txt in snips])
        prompt = (
            "Answer the question using ONLY the provided context. "
            "Cite sources like [#]. If not found, say so.\n\n"
            f"Question: {question}\n\n"
            f"Context:\n{numbered}"
        )
        resp = client.models.generate_content(model=model_name, contents=prompt)
        return (resp.text or "").strip()
    except Exception as e:
        print("[Gemini QA] Error:", e)
        return "Sorry — I couldn’t answer that from the contract context."

def build_qa_prompt(question: str, contexts: list[tuple[int, str]], *,
                    max_total_chars: int = 1600, per_chunk_chars: int = 350) -> str:
    snips: list[tuple[int, str]] = []
    total = 0
    for cid, txt in contexts:
        snip = txt[:per_chunk_chars]
        if total + len(snip) + 10 > max_total_chars:
            break
        snips.append((cid, snip))
        total += len(snip) + 10

    numbered = "\n\n".join([f"[{cid}] {txt}" for cid, txt in snips])
    prompt = (
        "Answer the question using ONLY the provided context. "
        "Cite supporting snippets using bracket numbers like [12]. "
        "If the answer is not in context, say you don't find it.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{numbered}"
    )
    return prompt

def answer_with_gemini_prompt(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    try:
        client = _get_client()
        resp = client.models.generate_content(model=model_name, contents=prompt)
        return (resp.text or "").strip()
    except Exception as e:
        print("[Gemini QA] Error:", e)
        return "Sorry — I couldn’t answer that from the contract context."

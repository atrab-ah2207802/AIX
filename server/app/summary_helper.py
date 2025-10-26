# # server/app/summary_helper.py
# import os, re
# from .models import ContractExtraction
# from .gemini_helper import call_gemini_text


# def generate_summary(text: str, ex: ContractExtraction) -> str | None:
#     """
#     Generates a concise bullet-point summary using Gemini.
#     Fallbacks to heuristic summary if API fails.
#     """
#     prompt = (
#         "Summarize this contract in 3–5 concise bullet points focusing on its "
#         "purpose, deliverables, key dates, governing law, and payment terms.\n\n"
#         f"{text[:6000]}"
#     )

#     try:
#         result = call_gemini_text(prompt)
#         if result:
#             return result.strip()
#     except Exception:
#         pass

#     # --- Fallback if Gemini fails ---
#     bullets = []
#     if ex.obligations:
#         bullets.append(f"Purpose: {ex.obligations[0].text[:120]}")
#     if ex.parties:
#         bullets.append("Parties: " + " vs. ".join(p.name for p in ex.parties[:2]))
#     if ex.effective_date or ex.expiry_date:
#         bullets.append(f"Dates: {ex.effective_date} → {ex.expiry_date}")
#     if ex.governing_law:
#         bullets.append(f"Governing law: {ex.governing_law}")
#     if ex.financials:
#         f = ex.financials[0]
#         bullets.append(f"Payment: {f.currency} {f.amount}")
#     return "- " + "\n- ".join(bullets[:5]) if bullets else None

from .models import ContractExtraction
from .gemini_helper import call_gemini_text


def generate_summary(text: str, ex: ContractExtraction) -> str | None:
    """
    Generates a concise bullet-point summary using Gemini.
    Fallbacks to heuristic summary if API fails.
    """
    prompt = (
        "Summarize this contract in 3–5 concise bullet points focusing on its "
        "purpose, deliverables, key dates, governing law, and payment terms.\n\n"
        f"{text[:6000]}"
    )

    try:
        result = call_gemini_text(prompt)
        if result:
            return result.strip()
    except Exception:
        pass

    # --- Fallback if Gemini fails ---
    bullets = []
    if ex.obligations:
        bullets.append(f"Purpose: {ex.obligations[0].text[:120]}")
    if ex.parties:
        bullets.append("Parties: " + " vs. ".join(p.name for p in ex.parties[:2]))
    if ex.effective_date or ex.expiry_date:
        bullets.append(f"Dates: {ex.effective_date} → {ex.expiry_date}")
    if ex.governing_law:
        bullets.append(f"Governing law: {ex.governing_law}")
    if ex.financials:
        f = ex.financials[0]
        bullets.append(f"Payment: {f.currency} {f.amount}")
    return "- " + "\n- ".join(bullets[:5]) if bullets else None

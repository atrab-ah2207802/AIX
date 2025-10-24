# server/app/risk.py
from .models import RiskSummary, RiskFlag
from . import prompts

# simple rules + LLM blended
RULES = [
    ("Unlimited liability", "High", lambda t: "unlimited liab" in t.lower() or "unlimited liability" in t.lower()),
    ("Missing termination notice", "Medium", lambda t: "termination" not in t.lower()),
]

def assess(text: str, extraction: dict) -> RiskSummary:
    score = 100
    flags = []
    for title, sev, fn in RULES:
        if fn(text):
            flags.append(RiskFlag(title=title, severity=sev, explanation="Detected by rule"))
            score -= 15 if sev=="High" else 8
    score = max(min(score,100),0)
    return RiskSummary(score=score, flags=flags)

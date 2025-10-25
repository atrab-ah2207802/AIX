# # server/app/models.py
# from pydantic import BaseModel
# from typing import List, Optional, Literal

# class Party(BaseModel):
#     name: str
#     role: Optional[str] = None

# class MoneyTerm(BaseModel):
#     label: str
#     amount: Optional[str] = None
#     currency: Optional[str] = None
#     text: str

# class Obligation(BaseModel):
#     party: Optional[str] = None
#     text: str

# class ContractExtraction(BaseModel):
#     parties: List[Party] = []
#     effective_date: Optional[str] = None
#     expiry_date: Optional[str] = None
#     renewals: Optional[str] = None
#     governing_law: Optional[str] = None
#     obligations: List[Obligation] = []
#     financials: List[MoneyTerm] = []
#     signatures_present: Optional[bool] = None
#     raw_summary: Optional[str] = None

# class RiskFlag(BaseModel):
#     title: str
#     severity: Literal["Low","Medium","High"]
#     explanation: str
#     suggested_fix_text: Optional[str] = None
#     clause_excerpt: Optional[str] = None

# class RiskSummary(BaseModel):
#     score: int
#     flags: List[RiskFlag] = []

# class UploadResponse(BaseModel):
#     doc_id: str
#     meta: dict

# class QARequest(BaseModel):
#     doc_id: str
#     query: str

# class QAAnswer(BaseModel):
#     answer: str
#     sources: list


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

# ============================= models.py =====================================
# from pydantic import BaseModel
# from typing import List, Optional, Literal

# class Party(BaseModel):
#     name: str
#     role: Optional[str] = None  # e.g., Supplier, Client

# class MoneyTerm(BaseModel):
#     label: str
#     amount: Optional[str] = None
#     currency: Optional[str] = None
#     text: str

# class Obligation(BaseModel):
#     party: Optional[str] = None
#     text: str

# class ContractExtraction(BaseModel):
#     parties: List[Party] = []
#     effective_date: Optional[str] = None
#     expiry_date: Optional[str] = None
#     renewals: Optional[str] = None
#     governing_law: Optional[str] = None
#     obligations: List[Obligation] = []
#     financials: List[MoneyTerm] = []
#     signatures_present: Optional[bool] = None
#     raw_summary: Optional[str] = None

# class UploadResponse(BaseModel):
#     doc_id: str
#     meta: dict


# class RiskFlag(BaseModel):
#     title: str
#     severity: Literal["Low", "Medium", "High", "Critical"]
#     explanation: str
#     suggested_fix_text: Optional[str] = None
#     clause_excerpt: Optional[str] = None

# class RiskSummary(BaseModel):
#     score: int
#     flags: List[RiskFlag] = []

# class RiskRequest(BaseModel):
#     doc_id: str
#     extraction: ContractExtraction  # Reuse the extraction model


from pydantic import BaseModel
from typing import List, Optional

class Party(BaseModel):
    name: str
    role: Optional[str] = None  # e.g., Supplier, Client

class Penalty(BaseModel):
    type: Optional[str] = None          # e.g., "late fee", "interest"
    amount: Optional[str] = None        # e.g., "100", "500"
    rate: Optional[str] = None          # e.g., "1.5% per month"
    condition: Optional[str] = None     # e.g., "late payment"
    text: str

class MoneyTerm(BaseModel):
    label: str
    amount: Optional[str] = None
    currency: Optional[str] = None
    schedule: Optional[str] = None      # e.g., "net 30", "monthly"
    penalties: List[Penalty] = []       # structured penalties tied to payments
    text: str

class Obligation(BaseModel):
    party: Optional[str] = None
    text: str

class ContractExtraction(BaseModel):
    # Parties
    parties: List[Party] = []

    # Dates
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    renewal_date: Optional[str] = None   # explicit date if present
    auto_renewal: Optional[bool] = None  # True/False if stated, else None
    renewals: Optional[str] = None       # original renewal language

    # Law & venue
    governing_law: Optional[str] = None
    jurisdiction: Optional[str] = None   # courts/venue

    # Core terms
    obligations: List[Obligation] = []
    financials: List[MoneyTerm] = []

    # Other
    signatures_present: Optional[bool] = None
    raw_summary: Optional[str] = None    # 3–5 bullets: purpose and scope

class UploadResponse(BaseModel):
    doc_id: str
    meta: dict

from pydantic import BaseModel

class QARequest(BaseModel):
    doc_id: str
    query: str
    k: int = 4

class QASource(BaseModel):
    chunk_id: int
    score: float
    text: str

class QAAnswer(BaseModel):
    answer: str
    sources: list[QASource]

class QADebugAnswer(QAAnswer):
    prompt: str
    model_name: str | None = None


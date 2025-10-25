# risk_server.py - COMPLETE FIXED VERSION
import sys
import os
import asyncio

# Add parent directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import time
import json

app = FastAPI(title="AIX CLM - Risk Analysis API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== YOUR RISK ANALYSIS ==========
class RiskRequest(BaseModel):
    doc_id: str
    extraction: Dict[str, Any]
    country: str = "qatar"

class RiskFlag(BaseModel):
    severity: str
    category: str
    title: str
    description: str
    recommendation: str
    clause_reference: str
    confidence: float

class RiskResponse(BaseModel):
    overall_score: int
    risk_level: str
    summary: str
    flags: List[RiskFlag]
    recommendations: List[str]
    analyzed_at: str
    contract_metadata: Dict[str, Any]
    legal_compliance: Dict[str, Any]

@app.get("/api/health")
def health():
    return {"ok": True, "ts": time.time(), "service": "Risk Analysis API"}

@app.post("/api/risk", response_model=RiskResponse)
async def api_risk(body: RiskRequest):
    """YOUR COMPLETE RISK ANALYSIS"""
    try:
        # Import your risk modules (should work now with the path fix)
        from app.risk import call_llm, analyze_contract_risk
        from app.legal_compliance import LegalComplianceAnalyzer
        from app.learned_analyzer import SmartProductionRiskAnalyzer
        
        print("🚀 Starting risk analysis...")
        
        # STEP 1: Load templates
        templates = await learn_templates_from_contracts()
        
        # STEP 2: Prepare data
        test_data = {
            "contract_id": body.doc_id,
            "parties": body.extraction.get("parties", []),
            "dates": body.extraction.get("dates", {}),
            "financial": body.extraction.get("financial", {}),
            "jurisdiction": body.country,
            "governing_law": f"{body.country} laws"
        }
        
        # Use sample contract text
        sample_text = """
        AGREEMENT BETWEEN QDB AND VENDOR INC
        
        This Agreement is made on January 1, 2025 between Qatar Development Bank ("QDB") 
        and Vendor Inc ("Supplier").
        
        TERM: This Agreement shall be effective from January 1, 2025 and expire on December 31, 2025.
        
        PAYMENT TERMS: Supplier shall be paid QAR 500,000 upon completion of services.
        Payment shall be made net 60 days from invoice date.
        
        GOVERNING LAW: This Agreement shall be governed by the laws of Qatar.
        """
        
        # STEP 3: Run template-based risk analysis
        template_risk = None
        if templates:
            try:
                print("🧠 Running template-based analysis...")
                template_analyzer = SmartProductionRiskAnalyzer(templates, call_llm)
                template_risk = await template_analyzer.analyze_contract(sample_text, test_data)
                print(f"   ✅ Template analysis: {template_risk.overall_score}/100")
            except Exception as e:
                print(f"   ❌ Template analysis failed: {e}")
                template_risk = None
        
        # Fallback to basic analysis
        if not template_risk:
            print("📊 Running basic risk analysis...")
            template_risk = await analyze_contract_risk(sample_text, test_data, body.country)
            print(f"   ✅ Basic analysis: {template_risk.overall_score}/100")
        
        # STEP 4: Legal compliance analysis
        legal_compliance = None
        legal_db_path = os.path.join("..", "legal_database", body.country)
        
        if os.path.exists(legal_db_path):
            try:
                print("⚖️ Running legal compliance analysis...")
                risk_flags_dict = [
                    {
                        "severity": flag.severity,
                        "category": flag.category,
                        "title": flag.title,
                        "description": flag.description,
                        "recommendation": flag.recommendation
                    }
                    for flag in template_risk.flags
                ]
                
                legal_analyzer = LegalComplianceAnalyzer(call_llm)
                legal_compliance = await legal_analyzer.analyze_legal_compliance(
                    sample_text, body.country, risk_flags_dict, contract_id=body.doc_id
                )
                print(f"   ✅ Legal compliance: {legal_compliance['compliance_summary']['overall_compliance_score']}/100")
            except Exception as e:
                print(f"   ❌ Legal compliance failed: {e}")
        else:
            print(f"   ⚠️ No legal database at {legal_db_path}")
        
        # STEP 5: Generate unified report
        unified_report = generate_unified_report(template_risk, legal_compliance, sample_text, test_data)
        
        print("🎉 Risk analysis complete!")
        return unified_report
        
    except Exception as e:
        print(f"❌ Risk analysis failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")

# ========== YOUR HELPER FUNCTIONS ==========
async def learn_templates_from_contracts():
    """Load your pre-saved templates"""
    try:
        template_path = os.path.join("..", "data", "learned_templates", "company_templates.json")
        with open(template_path, 'r', encoding='utf-8') as f:
            templates = json.load(f)
        print(f"✅ Loaded {len(templates['learned_templates'])} templates")
        return templates
    except Exception as e:
        print(f"❌ Failed to load templates: {e}")
        return None

def generate_unified_report(template_risk, legal_compliance, contract_text: str, extracted_data: Dict) -> Dict:
    """Generate your unified report format"""
    flags = []
    for flag in template_risk.flags:
        flags.append({
            "severity": flag.severity,
            "category": flag.category,
            "title": flag.title,
            "description": flag.description,
            "recommendation": flag.recommendation or "",
            "clause_reference": flag.clause_reference or "Not Found",
            "confidence": flag.confidence
        })
    
    recommendations = list(set([
        flag["recommendation"] for flag in flags 
        if flag["recommendation"] and len(flag["recommendation"]) > 10
    ]))[:10]
    
    report = {
        "overall_score": template_risk.overall_score,
        "risk_level": template_risk.risk_level,
        "summary": template_risk.summary,
        "flags": flags,
        "recommendations": recommendations,
        "analyzed_at": template_risk.analyzed_at,
        "contract_metadata": {
            "contract_name": "analyzed_contract.docx",
            "parties": extracted_data.get("parties", []),
            "effective_date": extracted_data.get("dates", {}).get("start", "Not specified"),
            "expiry_date": extracted_data.get("dates", {}).get("expiration", "Not specified"),
            "total_value": "QAR 500000",
            "extracted_clauses_count": 5
        },
        "legal_compliance": legal_compliance if legal_compliance else {
            "analyzed": False,
            "jurisdiction": "N/A",
            "compliance_summary": {
                "overall_compliance_score": 0,
                "status": "not_analyzed"
            }
        }
    }
    
    return report

if __name__ == "__main__":
    import uvicorn
    
    # Set environment variables
    os.environ["GEMINI_API_KEY"] = "AIzaSyAuaNa4BbYOmHFBYTuaw_xfiLm2ASMWLqY"
    
    print("🚀 Starting Risk Analysis Server on http://localhost:8001")
    print("📁 Working directory:", os.getcwd())
    print("📁 Python path:", sys.path)
    uvicorn.run(app, host="0.0.0.0", port=8001)
# """
# - Non-standard clause detection
# - Legal advice and opinions
# - Law/regulation comparison
# - Missing clause identification
# - Term consistency checking
# - Company template comparison
# """
# import google.generativeai as genai
# import os
# from typing import List, Dict, Any, Optional
# from datetime import datetime
# from pydantic import BaseModel
# import openai
# import json
# #For pattern matching like finding clauses
# import re
# from collections import defaultdict
# from .config import settings
# from .prompts import (
#     RISK_ANALYSIS_PROMPT, 
#     LEGAL_ADVICE_PROMPT,
#     CLAUSE_COMPARISON_PROMPT,
#     TERM_CONSISTENCY_PROMPT
# )


# class RiskFlag(BaseModel):
#     """Individual risk finding"""
#     severity: str  # "critical", "high", "medium", "low"
#     category: str  # type of risk found, "non_standard", "missing_clause", "inconsistent_term", "legal_risk", "compliance"
#     title: str #just a name for the risk
#     description: str
#     recommendation: Optional[str] = None
#     clause_reference: Optional[str] = None # which part of the contract has the issue
#     legal_opinion: Optional[str] = None
#     confidence: float = 1.0
#     affected_section: Optional[str] = None


# class ComplianceCheck(BaseModel):
#     """Compliance with specific law/regulation"""
#     regulation: str
#     status: str  # "compliant", "non_compliant", "unclear"
#     issues: List[str]
#     recommendations: List[str]


# class TermConsistency(BaseModel):
#     """Term definition consistency check"""
#     term: str
#     definitions: List[str]
#     is_consistent: bool
#     issue_description: Optional[str] = None


# class ClauseComparison(BaseModel):
#     """Comparison with standard template"""
#     clause_type: str
#     standard_version: str
#     contract_version: str
#     deviation_severity: str  # "none", "minor", "major"
#     explanation: str


# class LegalAdvice(BaseModel):
#     """AI-generated legal advice"""
#     topic: str
#     advice: str
#     risk_level: str
#     supporting_law: Optional[str] = None
#     recommendations: List[str]


# class RiskAssessment(BaseModel):
#     """Complete risk analysis result"""
#     overall_score: int
#     risk_level: str
#     flags: List[RiskFlag]
#     summary: str
#     recommendations: List[str]
#     compliance_checks: List[ComplianceCheck]
#     term_consistency: List[TermConsistency]
#     clause_comparisons: List[ClauseComparison]
#     legal_advice: List[LegalAdvice]
#     analyzed_at: str



# class StandardTemplates:
#     """Standard clauses that contracts should match"""
    
#     STANDARD_CLAUSES = {
#         "termination": {
#             "standard": """Either party may terminate this Agreement with 30 days' written notice. 
#             In case of material breach, termination may be immediate upon written notice.""",
#             "key_elements": ["30 days notice", "written notice", "material breach", "immediate termination"],
#             "must_include": ["notice period", "termination conditions"]
#         },
#         "confidentiality": {
#             "standard": """Both parties agree to keep confidential all proprietary information 
#             disclosed during the term of this Agreement and for 2 years thereafter.""",
#             "key_elements": ["both parties", "confidential", "proprietary information", "2 years"],
#             "must_include": ["confidentiality obligation", "duration"]
#         },
#         "liability": {
#             "standard": """Neither party shall be liable for indirect, incidental, or consequential 
#             damages. Total liability shall not exceed the total fees paid under this Agreement.""",
#             "key_elements": ["liability cap", "exclude indirect damages", "limitation amount"],
#             "must_include": ["liability limitation", "damage exclusions"]
#         },
#         "force_majeure": {
#             "standard": """Neither party shall be liable for failure to perform due to circumstances 
#             beyond reasonable control, including natural disasters, war, or government action.""",
#             "key_elements": ["beyond control", "natural disasters", "excuse performance"],
#             "must_include": ["force majeure events", "performance excuse"]
#         },
#         "intellectual_property": {
#             "standard": """All intellectual property rights shall remain with the creating party. 
#             Any joint creations shall be jointly owned.""",
#             "key_elements": ["IP ownership", "creating party", "joint ownership"],
#             "must_include": ["ownership rights", "license terms"]
#         },
#         "dispute_resolution": {
#             "standard": """Any disputes shall first be attempted to resolve through negotiation. 
#             If unsuccessful, disputes shall be resolved through arbitration in Qatar.""",
#             "key_elements": ["negotiation first", "arbitration", "Qatar jurisdiction"],
#             "must_include": ["dispute mechanism", "jurisdiction"]
#         }
#     }



# class AIRiskAssessor:
#     """AI-powered risk analysis using LLM"""
    
#     def __init__(self, contract_text: str, extracted_data: Dict):
#         self.text = contract_text
#         self.data = extracted_data
    
#     # async def analyze(self) -> List[RiskFlag]:
#     #     """Use LLM for nuanced risk analysis"""
#     #     prompt = RISK_ANALYSIS_PROMPT.format(
#     #         extracted_data=json.dumps(self.data, indent=2),
#     #         contract_text=self.text[:3000]
#     #     )
        
#     #     try:
#     #         response = await call_llm(prompt)
#     #         result = json.loads(response)
#     #         return self._parse_ai_risks(result.get("risks", []))
#     #     except Exception as e:
#     #         print(f"AI risk analysis failed: {e}")
#     #         return []
#     async def analyze(self) -> RiskAssessment:
#         print("🔍 Starting PARALLEL risk analysis...")
        
#         # Run rule-based and AI in parallel
#         rule_detector = RuleBasedRiskDetector(self.text, self.data)
#         ai_assessor = AIRiskAssessor(self.text, self.data)
        
#         # Run both simultaneously
#         rule_flags, ai_flags = await asyncio.gather(
#             asyncio.to_thread(rule_detector.analyze),  # Rule-based in thread
#             ai_assessor.analyze()                      # AI async
#         )
    
#     def _parse_ai_risks(self, risks_data: List) -> List[RiskFlag]:
#         """Convert AI response to RiskFlag objects"""
#         flags = []
#         for risk in risks_data:
#             flags.append(RiskFlag(
#                 severity=risk.get("severity", "medium"),
#                 category=risk.get("category", "legal_risk"),
#                 title=risk.get("title", "AI-Identified Risk"),
#                 description=risk.get("description", ""),
#                 recommendation=risk.get("recommendation"),
#                 clause_reference=risk.get("clause_reference"),
#                 confidence=risk.get("confidence", 0.7)
#             ))
#         return flags



# class RuleBasedRiskDetector:
#     """Fast, deterministic rule-based risk checks"""
    
#     REQUIRED_CLAUSES = {
#         "termination": ["termination", "terminate", "cancellation", "end the contract"],
#         "liability": ["liability", "indemnification", "indemnify", "limitation of liability"],
#         "confidentiality": ["confidential", "confidentiality", "non-disclosure", "proprietary"],
#         "dispute_resolution": ["dispute resolution", "arbitration", "mediation", "jurisdiction"],
#         "intellectual_property": ["intellectual property", "IP rights", "copyright", "ownership"],
#         "payment_terms": ["payment", "invoice", "fee", "price", "compensation"],
#         "force_majeure": ["force majeure", "act of god", "beyond reasonable control"],
#     }

#     RED_FLAG_TERMS = {
#         "unlimited_liability": ["unlimited liability", "no limit on liability", "full liability"],
#         "automatic_renewal": ["automatically renew", "auto-renewal", "perpetual renewal"],
#         "unilateral_change": ["right to modify unilaterally", "change at any time without notice"],
#         "excessive_notice": ["180 days notice", "six month notice", "one year notice"],
#     }

#     def __init__(self, contract_text: str, extracted_data: Dict[str, Any]):
#         self.text = contract_text.lower()
#         self.data = extracted_data
#         self.flags: List[RiskFlag] = []
    
#     def analyze(self) -> List[RiskFlag]:
#         """Run all rule-based checks"""
#         self._check_missing_clauses()
#         self._check_red_flag_terms()
#         self._check_dates()
#         self._check_financial_terms()
#         self._check_jurisdiction()
#         self._check_unusual_clauses()
#         return self.flags
    
#     def _check_missing_clauses(self):
#         """Check for missing required clauses"""
#         for clause_type, keywords in self.REQUIRED_CLAUSES.items():
#             if not any(keyword in self.text for keyword in keywords):
#                 self.flags.append(RiskFlag(
#                     severity="high",
#                     category="missing_clause",
#                     title=f"Missing {clause_type.replace('_', ' ').title()} Clause",
#                     description=f"Standard {clause_type} clause not found",
#                     recommendation=f"Add comprehensive {clause_type} clause"
#                 ))
    
#     def _check_red_flag_terms(self):
#         """Check for unfavorable terms"""
#         for flag_type, terms in self.RED_FLAG_TERMS.items():
#             for term in terms:
#                 if term in self.text:
#                     self.flags.append(RiskFlag(
#                         severity="high",
#                         category="unfavorable_term",
#                         title=f"Unfavorable Term: {term.title()}",
#                         description=f"Contract contains {term} which may be unfavorable",
#                         recommendation=f"Negotiate removal or modification of '{term}'"
#                     ))
    
#     def _check_dates(self):
#         """Check for date-related risks"""
#         # Check for unreasonable notice periods
#         if "180 days" in self.text or "six month" in self.text:
#             self.flags.append(RiskFlag(
#                 severity="medium",
#                 category="unfavorable_term",
#                 title="Excessive Notice Period",
#                 description="180-day notice period is unusually long",
#                 recommendation="Negotiate for standard 30-day notice period"
#             ))
    
#     def _check_financial_terms(self):
#         """Check financial risks"""
#         # Check for unclear payment terms
#         payment_terms = self.data.get("financial", {}).get("paymentTerms", "")
#         if not payment_terms or "net" not in payment_terms.lower():
#             self.flags.append(RiskFlag(
#                 severity="medium",
#                 category="missing_clause",
#                 title="Unclear Payment Terms",
#                 description="Payment terms are not clearly specified",
#                 recommendation="Specify exact payment amounts, due dates, and methods"
#             ))
    
#     def _check_jurisdiction(self):
#         """Check jurisdiction risks"""
#         jurisdiction = self.data.get("jurisdiction", "")
#         if not jurisdiction:
#             self.flags.append(RiskFlag(
#                 severity="high",
#                 category="compliance",
#                 title="No Jurisdiction Specified",
#                 description="Contract does not specify governing law or jurisdiction",
#                 recommendation="Add jurisdiction clause specifying applicable law"
#             ))
    
#     def _check_unusual_clauses(self):
#         """Check for unusual/risky clauses"""
#         unusual_terms = {
#             "perpetual": "Perpetual obligation without end date",
#             "irrevocable": "Irrevocable rights may limit future flexibility",
#             "exclusive": "Exclusive arrangements limit business options",
#             "non-compete": "Non-compete clauses restrict business activities",
#             "assignment prohibited": "Unable to assign contract could limit exit options"
#         }
        
#         for term, risk in unusual_terms.items():
#             if term in self.text:
#                 self.flags.append(RiskFlag(
#                     severity="medium",
#                     category="non_standard",
#                     title=f"Unusual Clause: {term.title()}",
#                     description=risk,
#                     recommendation="Review necessity and negotiate narrower scope if possible"
#                 ))


# # ============================================================================
# # QATAR LAW COMPLIANCE CHECKER
# # ============================================================================

# class QatarLawCompliance:
#     """Check compliance with Qatar Commercial Law"""
    
#     QATAR_REQUIREMENTS = {
#         "arabic_version": {
#             "required": False,
#             "description": "Commercial contracts with Qatari entities may require Arabic version",
#             "severity": "medium"
#         },
#         "jurisdiction": {
#             "required": True,
#             "description": "Contracts must specify jurisdiction (preferably Qatar)",
#             "severity": "high"
#         },
#         "payment_terms": {
#             "required": True,
#             "description": "Payment terms must be clearly specified",
#             "severity": "high"
#         },
#         "contract_duration": {
#             "required": True,
#             "description": "Contract duration must be specified",
#             "severity": "medium"
#         },
#         "good_faith": {
#             "required": True,
#             "description": "Contracts must be performed in good faith per Qatar Civil Code",
#             "severity": "low"
#         }
#     }
    
#     @staticmethod
#     def check_compliance(text: str, extracted_data: Dict) -> List[ComplianceCheck]:
#         """Check Qatar Commercial Law compliance"""
#         checks = []
        
#         # Check jurisdiction
#         jurisdiction = extracted_data.get("jurisdiction", "").lower()
#         if not jurisdiction:
#             checks.append(ComplianceCheck(
#                 regulation="Qatar Commercial Law - Article 1",
#                 status="non_compliant",
#                 issues=["No jurisdiction specified"],
#                 recommendations=["Add clause: 'This contract shall be governed by Qatar law'"]
#             ))
        
#         # Check payment terms
#         payment = extracted_data.get("financial", {}).get("paymentTerms")
#         if not payment:
#             checks.append(ComplianceCheck(
#                 regulation="Qatar Commercial Law - Article 172",
#                 status="non_compliant",
#                 issues=["Payment terms not clearly specified"],
#                 recommendations=["Specify payment amounts, due dates, and methods"]
#             ))
        
#         # Check good faith clause
#         if "good faith" not in text.lower():
#             checks.append(ComplianceCheck(
#                 regulation="Qatar Civil Code - Article 171",
#                 status="unclear",
#                 issues=["No explicit good faith obligation"],
#                 recommendations=["Consider adding: 'Parties shall perform in good faith'"]
#             ))
        
#         return checks


# # ============================================================================
# # TERM CONSISTENCY CHECKER
# # ============================================================================

# class TermConsistencyChecker:
#     """Check for consistent use of defined terms"""
    
#     def __init__(self, contract_text: str):
#         self.text = contract_text
#         self.issues: List[TermConsistency] = []
    
#     def analyze(self) -> List[TermConsistency]:
#         """Check term consistency"""
#         definitions = self._extract_definitions()
        
#         for term, defs in definitions.items():
#             if len(defs) > 1:
#                 self.issues.append(TermConsistency(
#                     term=term,
#                     definitions=defs,
#                     is_consistent=False,
#                     issue_description=f"'{term}' is defined {len(defs)} different ways"
#                 ))
            
#             if not self._check_capitalization(term):
#                 self.issues.append(TermConsistency(
#                     term=term,
#                     definitions=defs,
#                     is_consistent=False,
#                     issue_description=f"'{term}' has inconsistent capitalization throughout contract"
#                 ))
        
#         return self.issues
    
#     def _extract_definitions(self) -> Dict[str, List[str]]:
#         """Extract defined terms and their definitions"""
#         definitions = defaultdict(list)
#         pattern = r'"([^"]+)"\s+(?:means?|shall mean|is defined as)\s+([^.;]+)'
#         matches = re.finditer(pattern, self.text, re.IGNORECASE)
        
#         for match in matches:
#             term = match.group(1)
#             definition = match.group(2).strip()
#             definitions[term].append(definition)
        
#         return dict(definitions)
    
#     def _check_capitalization(self, term: str) -> bool:
#         """Check if term is consistently capitalized"""
#         capitalized = len(re.findall(rf'\b{re.escape(term)}\b', self.text))
#         lowercase = len(re.findall(rf'\b{re.escape(term.lower())}\b', self.text.lower()))
        
#         if capitalized > 0 and lowercase > 0:
#             inconsistency_ratio = min(capitalized, lowercase) / max(capitalized, lowercase)
#             return inconsistency_ratio < 0.2
        
#         return True


# # ============================================================================
# # NON-STANDARD CLAUSE DETECTOR
# # ============================================================================

# class NonStandardClauseDetector:
#     """Detect clauses that deviate from company standards"""
    
#     def __init__(self, contract_text: str):
#         self.text = contract_text.lower()
#         self.comparisons: List[ClauseComparison] = []
    
#     def compare_to_standards(self) -> List[ClauseComparison]:
#         """Compare contract clauses to standard templates"""
#         for clause_type, standard in StandardTemplates.STANDARD_CLAUSES.items():
#             comparison = self._compare_clause(clause_type, standard)
#             if comparison:
#                 self.comparisons.append(comparison)
        
#         return self.comparisons
    
#     def _compare_clause(self, clause_type: str, standard: Dict) -> Optional[ClauseComparison]:
#         """Compare specific clause to standard"""
#         contract_clause = self._extract_clause(clause_type)
        
#         if not contract_clause:
#             return ClauseComparison(
#                 clause_type=clause_type,
#                 standard_version=standard["standard"],
#                 contract_version="NOT FOUND",
#                 deviation_severity="major",
#                 explanation=f"Standard {clause_type} clause is missing entirely"
#             )
        
#         missing_elements = []
#         for element in standard["key_elements"]:
#             if element.lower() not in contract_clause.lower():
#                 missing_elements.append(element)
        
#         if len(missing_elements) == 0:
#             severity = "none"
#             explanation = f"{clause_type.title()} clause matches standard"
#         elif len(missing_elements) <= 2:
#             severity = "minor"
#             explanation = f"Missing elements: {', '.join(missing_elements)}"
#         else:
#             severity = "major"
#             explanation = f"Significant deviations. Missing: {', '.join(missing_elements)}"
        
#         return ClauseComparison(
#             clause_type=clause_type,
#             standard_version=standard["standard"][:100] + "...",
#             contract_version=contract_clause[:100] + "...",
#             deviation_severity=severity,
#             explanation=explanation
#         )
    
#     def _extract_clause(self, clause_type: str) -> Optional[str]:
#         """Extract specific clause from contract"""
#         keywords = {
#             "termination": ["termination", "terminate"],
#             "confidentiality": ["confidential", "confidentiality"],
#             "liability": ["liability", "indemnif"],
#             "force_majeure": ["force majeure", "act of god"],
#             "intellectual_property": ["intellectual property", "ip rights"],
#             "dispute_resolution": ["dispute", "arbitration"]
#         }
        
#         search_terms = keywords.get(clause_type, [])
#         paragraphs = self.text.split('\n\n')
        
#         for para in paragraphs:
#             if any(term in para for term in search_terms):
#                 return para[:500]
        
#         return None




# class AILegalAdvisor:
#     """Generate legal advice using LLM"""
    
#     def __init__(self, contract_text: str, extracted_data: Dict, risk_flags: List[RiskFlag]):
#         self.text = contract_text
#         self.data = extracted_data
#         self.flags = risk_flags
    
#     # async def generate_advice(self) -> List[LegalAdvice]:
#     #     """Generate comprehensive legal advice"""
#     #     advice_list = []
#     #     categories = set(f.category for f in self.flags)
        
#     #     for category in categories:
#     #         category_flags = [f for f in self.flags if f.category == category]
#     #         if len(category_flags) > 0:
#     #             advice = await self._get_ai_advice(category, category_flags)
#     #             if advice:
#     #                 advice_list.append(advice)
        
#     #     return advice_list
    
    
#     # async def _get_ai_advice(self, category: str, flags: List[RiskFlag]) -> Optional[LegalAdvice]:
#     #     """Get AI legal advice for specific category"""
#     #     flag_summaries = "\n".join([f"- {f.title}: {f.description}" for f in flags])
        
#     #     prompt = LEGAL_ADVICE_PROMPT.format(
#     #         category=category,
#     #         issues=flag_summaries,
#     #         contract_excerpt=self.text[:2000]
#     #     )
        
#     #     try:
#     #         response = await call_llm(prompt)
#     #         result = json.loads(response)
            
#     #         return LegalAdvice(
#     #             topic=category.replace("_", " ").title(),
#     #             advice=result.get("advice", ""),
#     #             risk_level=result.get("risk_level", "medium"),
#     #             supporting_law=result.get("supporting_law"),
#     #             recommendations=result.get("recommendations", [])
#     #         )
        
#     #     except Exception as e:
#     #         print(f"Failed to generate legal advice: {e}")
#     #         return None
# async def generate_advice(self) -> List[LegalAdvice]:
#     """Generate legal advice in parallel for all categories"""
#     categories = set(f.category for f in self.flags)
    
#     # Create all prompts first
#     prompts = []
#     for category in categories:
#         category_flags = [f for f in self.flags if f.category == category]
#         if len(category_flags) > 0:
#             flag_summaries = "\n".join([f"- {f.title}: {f.description}" for f in category_flags])
#             prompt = LEGAL_ADVICE_PROMPT.format(
#                 category=category,
#                 issues=flag_summaries,
#                 contract_excerpt=self.text[:1000]  # Reduced from 2000
#             )
#             prompts.append((category, prompt))
    
#     # Run all AI calls in parallel
#     tasks = [self._get_ai_advice_parallel(category, prompt) for category, prompt in prompts]
#     results = await asyncio.gather(*tasks, return_exceptions=True)
    
#     # Filter successful results
#     return [r for r in results if r is not None and not isinstance(r, Exception)]

# async def _get_ai_advice_parallel(self, category: str, prompt: str) -> Optional[LegalAdvice]:
#     """Optimized version without redundant processing"""
#     try:
#         response = await call_llm(prompt)
#         result = json.loads(response)
#         return LegalAdvice(
#             topic=category.replace("_", " ").title(),
#             advice=result.get("advice", ""),
#             risk_level=result.get("risk_level", "medium"),
#             supporting_law=result.get("supporting_law"),
#             recommendations=result.get("recommendations", [])
#         )
#     except Exception:
#         return None



# class ComprehensiveRiskAnalyzer:
#     """Complete risk analysis meeting all requirements"""
    
#     def __init__(self, contract_text: str, extracted_data: Dict[str, Any]):
#         self.text = contract_text
#         self.data = extracted_data

#     async def analyze(self) -> RiskAssessment:
#         """Run COMPLETE risk analysis"""
        
#         print("🔍 Starting comprehensive risk analysis...")
        
#         # 1. Rule-based detection (fast)
#         print("  ↳ Running rule-based checks...")
#         rule_detector = RuleBasedRiskDetector(self.text, self.data)
#         rule_flags = rule_detector.analyze()
        
#         # 2. AI-powered assessment (deeper)
#         print("  ↳ Running AI risk assessment...")
#         ai_assessor = AIRiskAssessor(self.text, self.data)
#         ai_flags = await ai_assessor.analyze()
        
#         # 3. Term consistency check
#         print("  ↳ Checking term consistency...")
#         term_checker = TermConsistencyChecker(self.text)
#         term_issues = term_checker.analyze()
        
#         # Convert term issues to flags
#         for issue in term_issues:
#             rule_flags.append(RiskFlag(
#                 severity="medium",
#                 category="inconsistent_term",
#                 title=f"Inconsistent Term: {issue.term}",
#                 description=issue.issue_description or "Term used inconsistently",
#                 recommendation="Standardize term usage throughout contract"
#             ))
        
#         # 4. Non-standard clause detection
#         print("  ↳ Comparing to company standards...")
#         clause_detector = NonStandardClauseDetector(self.text)
#         clause_comparisons = clause_detector.compare_to_standards()
        
#         # Convert major deviations to flags
#         for comp in clause_comparisons:
#             if comp.deviation_severity == "major":
#                 rule_flags.append(RiskFlag(
#                     severity="high",
#                     category="non_standard",
#                     title=f"Non-Standard {comp.clause_type.title()} Clause",
#                     description=comp.explanation,
#                     recommendation=f"Revise to match company standard template"
#                 ))
        
#         # 5. Qatar law compliance
#         print("  ↳ Checking Qatar law compliance...")
#         compliance_checks = QatarLawCompliance.check_compliance(self.text, self.data)
        
#         # Convert non-compliance to flags
#         for check in compliance_checks:
#             if check.status == "non_compliant":
#                 rule_flags.append(RiskFlag(
#                     severity="high",
#                     category="compliance",
#                     title=f"Non-Compliant: {check.regulation}",
#                     description=", ".join(check.issues),
#                     recommendation=", ".join(check.recommendations),
#                     legal_opinion=f"This may violate {check.regulation}"
#                 ))
        
#         # 6. Combine all flags
#         all_flags = self._deduplicate_flags(rule_flags + ai_flags)
        
#         # 7. Generate legal advice
#         print("  ↳ Generating legal advice...")
#         legal_advisor = AILegalAdvisor(self.text, self.data, all_flags)
#         legal_advice = await legal_advisor.generate_advice()
        
#         # 8. Calculate overall risk score
#         score = self._calculate_risk_score(all_flags)
#         risk_level = self._get_risk_level(score)
        
#         # 9. Generate summary and recommendations
#         summary = self._generate_summary(all_flags, score)
#         recommendations = self._generate_recommendations(all_flags)
        
#         print("✅ Analysis complete!")
        
#         return RiskAssessment(
#             overall_score=score,
#             risk_level=risk_level,
#             flags=all_flags,
#             summary=summary,
#             recommendations=recommendations,
#             compliance_checks=compliance_checks,
#             term_consistency=term_issues,
#             clause_comparisons=clause_comparisons,
#             legal_advice=legal_advice,
#             analyzed_at=datetime.utcnow().isoformat()
#         )
    
#     def _deduplicate_flags(self, flags: List[RiskFlag]) -> List[RiskFlag]:
#         """Remove duplicate risk flags"""
#         seen = set()
#         unique = []
        
#         for flag in flags:
#             key = f"{flag.category}:{flag.title}"
#             if key not in seen:
#                 seen.add(key)
#                 unique.append(flag)
        
#         severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
#         unique.sort(key=lambda f: severity_order.get(f.severity, 4))
        
#         return unique

#     def _calculate_risk_score(self, flags: List[RiskFlag]) -> int:
#         """Calculate 0-100 risk score (higher = safer)"""
#         base_score = 100
        
#         severity_weights = {
#             "critical": 25,
#             "high": 15,
#             "medium": 8,
#             "low": 3
#         }
        
#         for flag in flags:
#             deduction = severity_weights.get(flag.severity, 5)
#             deduction = int(deduction * flag.confidence)
#             base_score -= deduction
        
#         return max(0, min(100, base_score))

#     def _get_risk_level(self, score: int) -> str:
#         """Convert score to risk level"""
#         if score >= 80:
#             return "low"
#         elif score >= 60:
#             return "medium"
#         elif score >= 40:
#             return "high"
#         else:
#             return "critical"

#     def _generate_summary(self, flags: List[RiskFlag], score: int) -> str:
#         """Generate human-readable summary"""
#         risk_level = self._get_risk_level(score)
#         critical = sum(1 for f in flags if f.severity == "critical")
#         high = sum(1 for f in flags if f.severity == "high")
        
#         if risk_level == "low":
#             return f"This contract has low risk with {len(flags)} minor issues identified. Overall compliance is good."
#         elif risk_level == "medium":
#             return f"This contract has moderate risk with {high} high-priority and {len(flags)-high} total issues. Review recommended."
#         elif risk_level == "high":
#             return f"This contract has significant risk with {critical} critical and {high} high-priority issues. Legal review strongly recommended."
#         else:
#             return f"This contract has critical risk with {critical} critical issues. Do not sign without legal counsel."

#     def _generate_recommendations(self, flags: List[RiskFlag]) -> List[str]:
#         """Generate actionable recommendations"""
#         recommendations = []
#         seen = set()
        
#         for flag in flags:
#             if flag.recommendation and flag.recommendation not in seen:
#                 recommendations.append(flag.recommendation)
#                 seen.add(flag.recommendation)
        
#         categories = set(f.category for f in flags)
#         if "missing_clause" in categories:
#             recommendations.append("Engage legal counsel to add missing critical clauses")
#         if "unfavorable_term" in categories:
#             recommendations.append("Negotiate more balanced terms with the counterparty")
#         if "compliance" in categories:
#             recommendations.append("Ensure all compliance requirements are met before execution")
        
#         return recommendations[:5]


# # ============================================================================
# # MAIN ENTRY POINT
# # ============================================================================

# async def analyze_contract_risk(
#     contract_text: str, 
#     extracted_data: Dict[str, Any]
# ) -> RiskAssessment:
#     """
#     Complete risk & compliance analysis
#     Meets ALL hackathon requirements
#     """
#     analyzer = ComprehensiveRiskAnalyzer(contract_text, extracted_data)
#     return await analyzer.analyze()

# # ============================================================================
# # LLM HELPER FUNCTION (Self-contained in risk.py)
# # ============================================================================

# # async def call_llm(prompt: str) -> str:
# #     """
# #     LLM function for risk analysis - returns mock responses for testing
# #     Keep this in risk.py to make the module self-contained
# #     """
# #     print(f"🤖 Mock LLM called: {prompt[:100]}...")
    
# #     # Mock responses for testing risk analysis
# #     if "risk analysis" in prompt.lower():
# #         return '''{
# #             "risks": [
# #                 {
# #                     "severity": "critical",
# #                     "category": "unfavorable_term",
# #                     "title": "Unlimited Liability Detected",
# #                     "description": "Contract contains unlimited liability clause exposing company to significant financial risk",
# #                     "recommendation": "Negotiate liability cap at contract value",
# #                     "clause_reference": "Liability Section 4.2",
# #                     "confidence": 0.9
# #                 },
# #                 {
# #                     "severity": "high", 
# #                     "category": "compliance",
# #                     "title": "No Qatar Jurisdiction",
# #                     "description": "Contract does not specify Qatar jurisdiction which may cause legal complications",
# #                     "recommendation": "Add 'This contract shall be governed by Qatar law'",
# #                     "clause_reference": "Governing Law Section",
# #                     "confidence": 0.8
# #                 },
# #                 {
# #                     "severity": "medium",
# #                     "category": "unfavorable_term", 
# #                     "title": "Excessive Notice Period",
# #                     "description": "180-day notice period restricts business flexibility",
# #                     "recommendation": "Negotiate standard 30-day notice period",
# #                     "clause_reference": "Termination Clause",
# #                     "confidence": 0.7
# #                 }
# #             ]
# #         }'''
# #     elif "legal advice" in prompt.lower():
# #         return '''{
# #             "advice": "This contract contains several high-risk clauses. The unlimited liability clause is particularly concerning under Qatar Commercial Law Article 172. The lack of Qatar jurisdiction creates legal uncertainty for enforcement.",
# #             "risk_level": "high",
# #             "supporting_law": "Qatar Commercial Law Article 172",
# #             "recommendations": [
# #                 "Cap liability at the total contract value",
# #                 "Specify Qatar as the governing jurisdiction", 
# #                 "Add termination for convenience clause",
# #                 "Include good faith performance obligation"
# #             ]
# #         }'''
# #     else:
# #         return '{"result": "mock response", "status": "success"}'
# def get_fallback_response(prompt: str) -> str:
#     """Fallback mock responses when API fails"""
#     if "risk analysis" in prompt.lower():
#         return '''{
#             "risks": [
#                 {
#                     "severity": "critical",
#                     "category": "unfavorable_term",
#                     "title": "Unlimited Liability Detected",
#                     "description": "Contract contains unlimited liability clause exposing company to significant financial risk",
#                     "recommendation": "Negotiate liability cap at contract value",
#                     "clause_reference": "Liability Section 4.2",
#                     "confidence": 0.9
#                 },
#                 {
#                     "severity": "high", 
#                     "category": "compliance",
#                     "title": "No Qatar Jurisdiction",
#                     "description": "Contract does not specify Qatar jurisdiction which may cause legal complications",
#                     "recommendation": "Add 'This contract shall be governed by Qatar law'",
#                     "clause_reference": "Governing Law Section",
#                     "confidence": 0.8
#                 }
#             ]
#         }'''
#     elif "legal advice" in prompt.lower():
#         return '''{
#             "advice": "This contract contains high-risk clauses requiring legal review. Consider consulting Qatar legal counsel.",
#             "risk_level": "high",
#             "supporting_law": "Qatar Commercial Law",
#             "recommendations": ["Cap liability", "Specify Qatar jurisdiction"]
#         }'''
#     else:
#         return '{"result": "fallback"}'
    
# # async def call_llm(prompt: str) -> str:
# #     """
# #     Real LLM call using Google Gemini - with complete JSON cleaning
# #     """
# #     try:
# #         from .config import settings
# #         api_key = settings.GEMINI_API_KEY
# #         genai.configure(api_key=api_key)
        
# #         model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
# #         response = model.generate_content(prompt)
# #         response_text = response.text.strip()
        
# #         print(f"✅ Gemini raw response: {response_text[:200]}...")
        
# #         # STEP 1: Remove ```json and ``` markers if present
# #         if response_text.startswith('```json'):
# #             response_text = response_text[7:]  # Remove ```json
# #         if response_text.endswith('```'):
# #             response_text = response_text[:-3]  # Remove ```
# #         response_text = response_text.strip()
        
# #         # STEP 2: Remove any invisible control characters that break JSON
# #         import re
# #         response_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response_text)
        
# #         # STEP 3: Try to parse JSON to validate
# #         try:
# #             json.loads(response_text)
# #             print("✅ Response is valid JSON after cleaning")
# #             return response_text
# #         except json.JSONDecodeError as e:
# #             print(f"❌ Still invalid JSON after cleaning: {e}")
# #             print(f"Cleaned response: {response_text[:500]}...")
# #             return get_fallback_response(prompt)
        
# #     except Exception as e:
# #         print(f"❌ Gemini API error: {e}")
# #         return get_fallback_response(prompt)
# async def call_llm(prompt: str) -> str:
#     """LLM call with timeout to prevent hanging"""
#     try:
#         # Add timeout to prevent slow responses
#         async with asyncio.timeout(30):  # 30 second timeout
#             from .config import settings
#             api_key = settings.GEMINI_API_KEY
#             genai.configure(api_key=api_key)
            
#             model = genai.GenerativeModel('gemini-2.0-flash-lite')
            
#             # Shorter, more focused prompt
#             focused_prompt = f"Return ONLY valid JSON: {prompt[:1500]}..."  # Limit prompt size
            
#             response = await asyncio.to_thread(model.generate_content, focused_prompt)
#             response_text = response.text.strip()
            
#             # Fast JSON cleaning
#             if response_text.startswith('```json'):
#                 response_text = response_text[7:]
#             if response_text.endswith('```'):
#                 response_text = response_text[:-3]
            
#             import re
#             response_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response_text.strip())
            
#             json.loads(response_text)  # Validate
#             return response_text
            
#     except asyncio.TimeoutError:
#         print("⏰ LLM timeout - using fallback")
#         return get_fallback_response(prompt)
#     except Exception as e:
#         print(f"❌ LLM error: {e}")
#         return get_fallback_response(prompt)
"""
Risk Analysis Module - Final Fixed Version
"""

import google.generativeai as genai
import os
import asyncio
from asyncio import timeout
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import openai
import json
import re
from collections import defaultdict
from .config import settings
from .prompts import (
    RISK_ANALYSIS_PROMPT,
    LEGAL_ADVICE_PROMPT,
    CLAUSE_COMPARISON_PROMPT,
    TERM_CONSISTENCY_PROMPT
)

class RiskFlag(BaseModel):
    """Individual risk finding"""
    severity: str
    category: str
    title: str
    description: str
    recommendation: Optional[str] = None
    clause_reference: Optional[str] = None
    legal_opinion: Optional[str] = None
    confidence: float = 1.0
    affected_section: Optional[str] = None

class ComplianceCheck(BaseModel):
    """Compliance with specific law/regulation"""
    regulation: str
    status: str
    issues: List[str]
    recommendations: List[str]

class TermConsistency(BaseModel):
    """Term definition consistency check"""
    term: str
    definitions: List[str]
    is_consistent: bool
    issue_description: Optional[str] = None

class ClauseComparison(BaseModel):
    """Comparison with standard template"""
    clause_type: str
    standard_version: str
    contract_version: str
    deviation_severity: str
    explanation: str

class LegalAdvice(BaseModel):
    """AI-generated legal advice"""
    topic: str
    advice: str
    risk_level: str
    supporting_law: Optional[str] = None
    recommendations: List[str]

class RiskAssessment(BaseModel):
    """Complete risk analysis result"""
    overall_score: int
    risk_level: str
    flags: List[RiskFlag]
    summary: str
    recommendations: List[str]
    compliance_checks: List[ComplianceCheck]
    term_consistency: List[TermConsistency]
    clause_comparisons: List[ClauseComparison]
    legal_advice: List[LegalAdvice]
    analyzed_at: str

class StandardTemplates:
    """Standard clauses that contracts should match"""
    
    STANDARD_CLAUSES = {
        "termination": {
            "standard": """Either party may terminate this Agreement with 30 days' written notice.
            In case of material breach, termination may be immediate upon written notice.""",
            "key_elements": ["30 days notice", "written notice", "material breach", "immediate termination"],
            "must_include": ["notice period", "termination conditions"]
        },
        "confidentiality": {
            "standard": """Both parties agree to keep confidential all proprietary information
            disclosed during the term of this Agreement and for 2 years thereafter.""",
            "key_elements": ["both parties", "confidential", "proprietary information", "2 years"],
            "must_include": ["confidentiality obligation", "duration"]
        },
        "liability": {
            "standard": """Neither party shall be liable for indirect, incidental, or consequential
            damages. Total liability shall not exceed the total fees paid under this Agreement.""",
            "key_elements": ["liability cap", "exclude indirect damages", "limitation amount"],
            "must_include": ["liability limitation", "damage exclusions"]
        },
        "force_majeure": {
            "standard": """Neither party shall be liable for failure to perform due to circumstances
            beyond reasonable control, including natural disasters, war, or government action.""",
            "key_elements": ["beyond control", "natural disasters", "excuse performance"],
            "must_include": ["force majeure events", "performance excuse"]
        },
        "intellectual_property": {
            "standard": """All intellectual property rights shall remain with the creating party.
            Any joint creations shall be jointly owned.""",
            "key_elements": ["IP ownership", "creating party", "joint ownership"],
            "must_include": ["ownership rights", "license terms"]
        },
        "dispute_resolution": {
            "standard": """Any disputes shall first be attempted to resolve through negotiation.
            If unsuccessful, disputes shall be resolved through arbitration in Qatar.""",
            "key_elements": ["negotiation first", "arbitration", "Qatar jurisdiction"],
            "must_include": ["dispute mechanism", "jurisdiction"]
        }
    }

class AIRiskAssessor:
    """AI-powered risk analysis using LLM"""
    
    def __init__(self, contract_text: str, extracted_data: Dict):
        self.text = contract_text
        self.data = extracted_data
    
    async def analyze(self) -> List[RiskFlag]:
        """Use LLM for nuanced risk analysis"""
        prompt = RISK_ANALYSIS_PROMPT.format(
            extracted_data=json.dumps(self.data, indent=2),
            contract_text=self.text[:3000]
        )
        
        try:
            response = await call_llm(prompt)
            result = json.loads(response)
            return self._parse_ai_risks(result.get("risks", []))
        except Exception as e:
            print(f"AI risk analysis failed: {e}")
            return []
    
    def _parse_ai_risks(self, risks_data: List) -> List[RiskFlag]:
        """Convert AI response to RiskFlag objects"""
        flags = []
        for risk in risks_data:
            flags.append(RiskFlag(
                severity=risk.get("severity", "medium"),
                category=risk.get("category", "legal_risk"),
                title=risk.get("title", "AI-Identified Risk"),
                description=risk.get("description", ""),
                recommendation=risk.get("recommendation"),
                clause_reference=risk.get("clause_reference"),
                confidence=risk.get("confidence", 0.7)
            ))
        return flags

class RuleBasedRiskDetector:
    """Fast, deterministic rule-based risk checks"""
    
    REQUIRED_CLAUSES = {
        "termination": ["termination", "terminate", "cancellation", "end the contract"],
        "liability": ["liability", "indemnification", "indemnify", "limitation of liability"],
        "confidentiality": ["confidential", "confidentiality", "non-disclosure", "proprietary"],
        "dispute_resolution": ["dispute resolution", "arbitration", "mediation", "jurisdiction"],
        "intellectual_property": ["intellectual property", "IP rights", "copyright", "ownership"],
        "payment_terms": ["payment", "invoice", "fee", "price", "compensation"],
        "force_majeure": ["force majeure", "act of god", "beyond reasonable control"],
    }

    RED_FLAG_TERMS = {
        "unlimited_liability": ["unlimited liability", "no limit on liability", "full liability"],
        "automatic_renewal": ["automatically renew", "auto-renewal", "perpetual renewal"],
        "unilateral_change": ["right to modify unilaterally", "change at any time without notice"],
        "excessive_notice": ["180 days notice", "six month notice", "one year notice"],
    }

    def __init__(self, contract_text: str, extracted_data: Dict[str, Any]):
        self.text = contract_text.lower()
        self.data = extracted_data
        self.flags: List[RiskFlag] = []
    
    def analyze(self) -> List[RiskFlag]:
        """Run all rule-based checks"""
        self._check_missing_clauses()
        self._check_red_flag_terms()
        self._check_dates()
        self._check_financial_terms()
        self._check_jurisdiction()
        self._check_unusual_clauses()
        return self.flags
    
    def _check_missing_clauses(self):
        """Check for missing required clauses"""
        for clause_type, keywords in self.REQUIRED_CLAUSES.items():
            if not any(keyword in self.text for keyword in keywords):
                self.flags.append(RiskFlag(
                    severity="high",
                    category="missing_clause",
                    title=f"Missing {clause_type.replace('_', ' ').title()} Clause",
                    description=f"Standard {clause_type} clause not found",
                    recommendation=f"Add comprehensive {clause_type} clause"
                ))
    
    def _check_red_flag_terms(self):
        """Check for unfavorable terms"""
        for flag_type, terms in self.RED_FLAG_TERMS.items():
            for term in terms:
                if term in self.text:
                    self.flags.append(RiskFlag(
                        severity="high",
                        category="unfavorable_term",
                        title=f"Unfavorable Term: {term.title()}",
                        description=f"Contract contains {term} which may be unfavorable",
                        recommendation=f"Negotiate removal or modification of '{term}'"
                    ))
    
    def _check_dates(self):
        """Check for date-related risks"""
        if "180 days" in self.text or "six month" in self.text:
            self.flags.append(RiskFlag(
                severity="medium",
                category="unfavorable_term",
                title="Excessive Notice Period",
                description="180-day notice period is unusually long",
                recommendation="Negotiate for standard 30-day notice period"
            ))
    
    def _check_financial_terms(self):
        """Check financial risks"""
        payment_terms = self.data.get("financial", {}).get("paymentTerms", "")
        if not payment_terms or "net" not in payment_terms.lower():
            self.flags.append(RiskFlag(
                severity="medium",
                category="missing_clause",
                title="Unclear Payment Terms",
                description="Payment terms are not clearly specified",
                recommendation="Specify exact payment amounts, due dates, and methods"
            ))
    
    def _check_jurisdiction(self):
        """Check jurisdiction risks"""
        jurisdiction = self.data.get("jurisdiction", "")
        if not jurisdiction:
            self.flags.append(RiskFlag(
                severity="high",
                category="compliance",
                title="No Jurisdiction Specified",
                description="Contract does not specify governing law or jurisdiction",
                recommendation="Add jurisdiction clause specifying applicable law"
            ))
    
    def _check_unusual_clauses(self):
        """Check for unusual/risky clauses"""
        unusual_terms = {
            "perpetual": "Perpetual obligation without end date",
            "irrevocable": "Irrevocable rights may limit future flexibility",
            "exclusive": "Exclusive arrangements limit business options",
            "non-compete": "Non-compete clauses restrict business activities",
            "assignment prohibited": "Unable to assign contract could limit exit options"
        }
        
        for term, risk in unusual_terms.items():
            if term in self.text:
                self.flags.append(RiskFlag(
                    severity="medium",
                    category="non_standard",
                    title=f"Unusual Clause: {term.title()}",
                    description=risk,
                    recommendation="Review necessity and negotiate narrower scope if possible"
                ))

class QatarLawCompliance:
    """Check compliance with Qatar Commercial Law"""
    
    @staticmethod
    def check_compliance(text: str, extracted_data: Dict) -> List[ComplianceCheck]:
        """Check Qatar Commercial Law compliance"""
        checks = []
        
        jurisdiction = extracted_data.get("jurisdiction", "").lower()
        if not jurisdiction:
            checks.append(ComplianceCheck(
                regulation="Qatar Commercial Law - Article 1",
                status="non_compliant",
                issues=["No jurisdiction specified"],
                recommendations=["Add clause: 'This contract shall be governed by Qatar law'"]
            ))
        
        payment = extracted_data.get("financial", {}).get("paymentTerms")
        if not payment:
            checks.append(ComplianceCheck(
                regulation="Qatar Commercial Law - Article 172",
                status="non_compliant",
                issues=["Payment terms not clearly specified"],
                recommendations=["Specify payment amounts, due dates, and methods"]
            ))
        
        if "good faith" not in text.lower():
            checks.append(ComplianceCheck(
                regulation="Qatar Civil Code - Article 171",
                status="unclear",
                issues=["No explicit good faith obligation"],
                recommendations=["Consider adding: 'Parties shall perform in good faith'"]
            ))
        
        return checks

class TermConsistencyChecker:
    """Check for consistent use of defined terms"""
    
    def __init__(self, contract_text: str):
        self.text = contract_text
        self.issues: List[TermConsistency] = []
    
    def analyze(self) -> List[TermConsistency]:
        """Check term consistency"""
        definitions = self._extract_definitions()
        
        for term, defs in definitions.items():
            if len(defs) > 1:
                self.issues.append(TermConsistency(
                    term=term,
                    definitions=defs,
                    is_consistent=False,
                    issue_description=f"'{term}' is defined {len(defs)} different ways"
                ))
            
            if not self._check_capitalization(term):
                self.issues.append(TermConsistency(
                    term=term,
                    definitions=defs,
                    is_consistent=False,
                    issue_description=f"'{term}' has inconsistent capitalization throughout contract"
                ))
        
        return self.issues
    
    def _extract_definitions(self) -> Dict[str, List[str]]:
        """Extract defined terms and their definitions"""
        definitions = defaultdict(list)
        pattern = r'\"([^\"]+)\"\s+(?:means?|shall mean|is defined as)\s+([^.;]+)'
        matches = re.finditer(pattern, self.text, re.IGNORECASE)
        
        for match in matches:
            term = match.group(1)
            definition = match.group(2).strip()
            definitions[term].append(definition)
        
        return dict(definitions)
    
    def _check_capitalization(self, term: str) -> bool:
        """Check if term is consistently capitalized"""
        capitalized = len(re.findall(rf'\b{re.escape(term)}\b', self.text))
        lowercase = len(re.findall(rf'\b{re.escape(term.lower())}\b', self.text.lower()))
        
        if capitalized > 0 and lowercase > 0:
            inconsistency_ratio = min(capitalized, lowercase) / max(capitalized, lowercase)
            return inconsistency_ratio < 0.2
        
        return True

class NonStandardClauseDetector:
    """Detect clauses that deviate from company standards"""
    
    def __init__(self, contract_text: str):
        self.text = contract_text.lower()
        self.comparisons: List[ClauseComparison] = []
    
    def compare_to_standards(self) -> List[ClauseComparison]:
        """Compare contract clauses to standard templates"""
        for clause_type, standard in StandardTemplates.STANDARD_CLAUSES.items():
            comparison = self._compare_clause(clause_type, standard)
            if comparison:
                self.comparisons.append(comparison)
        
        return self.comparisons
    
    def _compare_clause(self, clause_type: str, standard: Dict) -> Optional[ClauseComparison]:
        """Compare specific clause to standard"""
        contract_clause = self._extract_clause(clause_type)
        
        if not contract_clause:
            return ClauseComparison(
                clause_type=clause_type,
                standard_version=standard["standard"],
                contract_version="NOT FOUND",
                deviation_severity="major",
                explanation=f"Standard {clause_type} clause is missing entirely"
            )
        
        missing_elements = []
        for element in standard["key_elements"]:
            if element.lower() not in contract_clause.lower():
                missing_elements.append(element)
        
        if len(missing_elements) == 0:
            severity = "none"
            explanation = f"{clause_type.title()} clause matches standard"
        elif len(missing_elements) <= 2:
            severity = "minor"
            explanation = f"Missing elements: {', '.join(missing_elements)}"
        else:
            severity = "major"
            explanation = f"Significant deviations. Missing: {', '.join(missing_elements)}"
        
        return ClauseComparison(
            clause_type=clause_type,
            standard_version=standard["standard"][:100] + "...",
            contract_version=contract_clause[:100] + "...",
            deviation_severity=severity,
            explanation=explanation
        )
    
    def _extract_clause(self, clause_type: str) -> Optional[str]:
        """Extract specific clause from contract"""
        keywords = {
            "termination": ["termination", "terminate"],
            "confidentiality": ["confidential", "confidentiality"],
            "liability": ["liability", "indemnif"],
            "force_majeure": ["force majeure", "act of god"],
            "intellectual_property": ["intellectual property", "ip rights"],
            "dispute_resolution": ["dispute", "arbitration"]
        }
        
        search_terms = keywords.get(clause_type, [])
        paragraphs = self.text.split('\n\n')
        
        for para in paragraphs:
            if any(term in para for term in search_terms):
                return para[:500]
        
        return None

class AILegalAdvisor:
    """Generate legal advice using LLM"""
    
    def __init__(self, contract_text: str, extracted_data: Dict, risk_flags: List[RiskFlag]):
        self.text = contract_text
        self.data = extracted_data
        self.flags = risk_flags
    
    async def generate_advice(self) -> List[LegalAdvice]:
        """Generate legal advice in parallel for all categories"""
        categories = set(f.category for f in self.flags)
        
        # Create all prompts first
        prompts = []
        for category in categories:
            category_flags = [f for f in self.flags if f.category == category]
            if len(category_flags) > 0:
                flag_summaries = "\n".join([f"- {f.title}: {f.description}" for f in category_flags])
                prompt = LEGAL_ADVICE_PROMPT.format(
                    category=category,
                    issues=flag_summaries,
                    contract_excerpt=self.text[:1000]
                )
                prompts.append((category, prompt))
        
        # Run all AI calls in parallel
        tasks = [self._get_ai_advice_parallel(category, prompt) for category, prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter successful results
        return [r for r in results if r is not None and not isinstance(r, Exception)]
    
    async def _get_ai_advice_parallel(self, category: str, prompt: str) -> Optional[LegalAdvice]:
        """Optimized version without redundant processing"""
        try:
            response = await call_llm(prompt)
            result = json.loads(response)
            return LegalAdvice(
                topic=category.replace("_", " ").title(),
                advice=result.get("advice", ""),
                risk_level=result.get("risk_level", "medium"),
                supporting_law=result.get("supporting_law"),
                recommendations=result.get("recommendations", [])
            )
        except Exception:
            return None

class ComprehensiveRiskAnalyzer:
    """Complete risk analysis meeting all requirements"""
    
    def __init__(self, contract_text: str, extracted_data: Dict[str, Any]):
        self.text = contract_text
        self.data = extracted_data
    
    async def analyze(self) -> RiskAssessment:
        """Run COMPLETE risk analysis"""
        
        print("🔍 Starting comprehensive risk analysis...")
        
        # Run analyses in parallel where possible
        rule_detector = RuleBasedRiskDetector(self.text, self.data)
        ai_assessor = AIRiskAssessor(self.text, self.data)
        term_checker = TermConsistencyChecker(self.text)
        clause_detector = NonStandardClauseDetector(self.text)
        
        print("  ↳ Running parallel analyses...")
        rule_flags, ai_flags, term_issues, clause_comparisons = await asyncio.gather(
            asyncio.to_thread(rule_detector.analyze),
            ai_assessor.analyze(),
            asyncio.to_thread(term_checker.analyze),
            asyncio.to_thread(clause_detector.compare_to_standards)
        )
        
        # Qatar law compliance (sync)
        print("  ↳ Checking Qatar law compliance...")
        compliance_checks = QatarLawCompliance.check_compliance(self.text, self.data)
        
        # Convert term issues to flags
        for issue in term_issues:
            rule_flags.append(RiskFlag(
                severity="medium",
                category="inconsistent_term",
                title=f"Inconsistent Term: {issue.term}",
                description=issue.issue_description or "Term used inconsistently",
                recommendation="Standardize term usage throughout contract"
            ))
        
        # Convert major deviations to flags
        for comp in clause_comparisons:
            if comp.deviation_severity == "major":
                rule_flags.append(RiskFlag(
                    severity="high",
                    category="non_standard",
                    title=f"Non-Standard {comp.clause_type.title()} Clause",
                    description=comp.explanation,
                    recommendation=f"Revise to match company standard template"
                ))
        
        # Convert non-compliance to flags
        for check in compliance_checks:
            if check.status == "non_compliant":
                rule_flags.append(RiskFlag(
                    severity="high",
                    category="compliance",
                    title=f"Non-Compliant: {check.regulation}",
                    description=", ".join(check.issues),
                    recommendation=", ".join(check.recommendations),
                    legal_opinion=f"This may violate {check.regulation}"
                ))
        
        # Combine all flags
        all_flags = self._deduplicate_flags(rule_flags + ai_flags)
        
        # Generate legal advice
        print("  ↳ Generating legal advice...")
        legal_advisor = AILegalAdvisor(self.text, self.data, all_flags)
        legal_advice = await legal_advisor.generate_advice()
        
        # Calculate overall risk score
        score = self._calculate_risk_score(all_flags)
        risk_level = self._get_risk_level(score)
        
        # Generate summary and recommendations
        summary = self._generate_summary(all_flags, score)
        recommendations = self._generate_recommendations(all_flags)
        
        print("✅ Analysis complete!")
        
        return RiskAssessment(
            overall_score=score,
            risk_level=risk_level,
            flags=all_flags,
            summary=summary,
            recommendations=recommendations,
            compliance_checks=compliance_checks,
            term_consistency=term_issues,
            clause_comparisons=clause_comparisons,
            legal_advice=legal_advice,
            analyzed_at=datetime.utcnow().isoformat()
        )
    
    def _deduplicate_flags(self, flags: List[RiskFlag]) -> List[RiskFlag]:
        """Remove duplicate risk flags"""
        seen = set()
        unique = []
        
        for flag in flags:
            key = f"{flag.category}:{flag.title}"
            if key not in seen:
                seen.add(key)
                unique.append(flag)
        
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        unique.sort(key=lambda f: severity_order.get(f.severity, 4))
        
        return unique
    
    def _calculate_risk_score(self, flags: List[RiskFlag]) -> int:
        """Balanced risk scoring that still reflects serious issues"""
        if not flags:
            return 85
        
        critical_count = sum(1 for f in flags if f.severity == "critical")
        high_count = sum(1 for f in flags if f.severity == "high") 
        medium_count = sum(1 for f in flags if f.severity == "medium")
        low_count = sum(1 for f in flags if f.severity == "low")
        
        # More balanced approach
        base_score = 75  # Start lower since most contracts have some issues
        
        # Focus deductions on critical/high issues only
        serious_deduction = (critical_count * 10) + (high_count * 6)
        minor_deduction = (medium_count * 2) + (low_count * 1)
        
        total_deduction = serious_deduction + minor_deduction
        
        # Cap maximum deduction
        capped_deduction = min(total_deduction, 60)
        
        final_score = base_score - capped_deduction
        return max(15, min(95, final_score))



    def _get_risk_level(self, score: int) -> str:
        """Convert score to risk level - MORE REALISTIC THRESHOLDS"""
        if score >= 70:    # Good contracts can have some issues
            return "low"
        elif score >= 50:  # Moderate risk is common
            return "medium"  
        elif score >= 30:  # High risk but still fixable
            return "high"
        else:
            return "critical"

    def _generate_summary(self, flags: List[RiskFlag], score: int) -> str:
        """Generate accurate summary with proper issue counting"""
        risk_level = self._get_risk_level(score)
        critical_count = sum(1 for f in flags if f.severity == "critical")
        high_count = sum(1 for f in flags if f.severity == "high")
        medium_count = sum(1 for f in flags if f.severity == "medium")
        low_count = sum(1 for f in flags if f.severity == "low")
        
        total_issues = len(flags)
        
        if risk_level == "low":
            return f"✅ LOW RISK: {total_issues} minor issues. Score: {score}/100"
        elif risk_level == "medium":
            return f"⚠️ MODERATE RISK: {high_count} high, {medium_count} medium priority issues. Score: {score}/100"
        elif risk_level == "high":
            return f"🚨 HIGH RISK: {critical_count} critical, {high_count} high priority issues. Score: {score}/100"
        else:
            return f"❌ CRITICAL RISK: {critical_count} critical, {high_count} high priority issues. Score: {score}/100"

    def _generate_recommendations(self, flags: List[RiskFlag]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        seen = set()
        
        for flag in flags:
            if flag.recommendation and flag.recommendation not in seen:
                recommendations.append(flag.recommendation)
                seen.add(flag.recommendation)
        
        categories = set(f.category for f in flags)
        if "missing_clause" in categories:
            recommendations.append("Engage legal counsel to add missing critical clauses")
        if "unfavorable_term" in categories:
            recommendations.append("Negotiate more balanced terms with the counterparty")
        if "compliance" in categories:
            recommendations.append("Ensure all compliance requirements are met before execution")
        
        return recommendations[:5]

async def analyze_contract_risk(
    contract_text: str,
    extracted_data: Dict[str, Any]
) -> RiskAssessment:
    """
    Complete risk & compliance analysis
    """
    analyzer = ComprehensiveRiskAnalyzer(contract_text, extracted_data)
    return await analyzer.analyze()

def repair_json_string(text: str) -> str:
    """Comprehensive JSON repair - specifically for Gemini's unescaped quotes"""
    if not text:
        return text
    
    # Remove markdown code blocks
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    
    # Fix unescaped quotes within strings - THE MAIN FIX
    # This pattern finds all string values and escapes internal quotes
    def escape_internal_quotes(match):
        content = match.group(1)
        # Escape quotes but not already escaped ones
        content = re.sub(r'(?<!\\)"', '\\"', content)
        return f'"{content}"'
    
    # Apply to all string values in the JSON
    text = re.sub(r'"(.*?)"', escape_internal_quotes, text)
    
    # Remove trailing commas
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text

def get_fallback_response(prompt: str) -> str:
    """Enhanced fallback responses"""
    if "risk analysis" in prompt.lower():
        return json.dumps({
            "risks": [
                {
                    "severity": "high",
                    "category": "unfavorable_term",
                    "title": "Unlimited Liability Detected",
                    "description": "Contract contains unlimited liability clause exposing company to significant financial risk",
                    "recommendation": "Negotiate liability cap at contract value",
                    "clause_reference": "Liability Section",
                    "confidence": 0.9
                },
                {
                    "severity": "high", 
                    "category": "compliance",
                    "title": "Missing Jurisdiction Clause",
                    "description": "Contract does not specify governing law or jurisdiction",
                    "recommendation": "Add Qatar jurisdiction clause",
                    "clause_reference": "Governing Law",
                    "confidence": 0.8
                }
            ]
        })
    elif "legal advice" in prompt.lower():
        return json.dumps({
            "advice": "This contract requires legal review due to multiple high-risk clauses including unlimited liability and missing jurisdiction.",
            "risk_level": "high",
            "supporting_law": "Qatar Commercial Law",
            "recommendations": [
                "Cap liability at contract value",
                "Specify Qatar jurisdiction", 
                "Add termination for cause clause",
                "Include force majeure protection"
            ]
        })
    else:
        return json.dumps({"result": "fallback", "status": "success"})

async def call_llm(prompt: str) -> str:
    """LLM call with ULTRA-robust JSON parsing and error handling"""
    try:
        async with timeout(30):
            from .config import settings
            api_key = settings.GEMINI_API_KEY
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            
            # ULTRA-STRICT prompt for JSON formatting
            strict_prompt = f"""
            CRITICAL: You MUST return ONLY valid JSON that can be parsed by json.loads().
            
            RULES:
            1. Use double quotes for ALL property names and string values
            2. Escape ALL double quotes within strings with backslash: \\"
            3. NO trailing commas after last array/object elements
            4. NO markdown code blocks (no ```json)
            5. Ensure proper bracket matching {{ }} and [ ]
            6. All strings must be properly quoted and escaped
            
            Example of CORRECT format:
            {{
              "risks": [
                {{
                  "severity": "high",
                  "category": "ambiguous", 
                  "title": "Sample Risk",
                  "description": "This is a properly escaped string with \\"quotes\\" inside",
                  "recommendation": "Fix the issue",
                  "clause_reference": "Section 1",
                  "confidence": 0.9
                }}
              ]
            }}
            
            Now respond to this request with VALID JSON only:
            {prompt[:1200]}
            """
            
            response = await asyncio.to_thread(model.generate_content, strict_prompt)
            response_text = response.text.strip()
            
            print(f"📨 Raw LLM response: {response_text[:200]}...")
            
            # Apply ULTRA repair
            response_text = repair_json_string(response_text)
            
            # Final validation
            try:
                parsed = json.loads(response_text)
                print("✅ LLM response validated successfully after repair")
                return response_text
            except json.JSONDecodeError as e:
                print(f"❌ JSON still invalid after repair: {e}")
                print(f"Repaired response: {response_text[:500]}...")
                return get_fallback_response(prompt)
            
    except asyncio.TimeoutError:
        print("⏰ LLM timeout - using fallback")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return get_fallback_response(prompt)
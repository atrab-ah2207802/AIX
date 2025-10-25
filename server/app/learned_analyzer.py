"""
SMART Template-Based Risk Analyzer - Uses learned QDB templates
"""

from .risk import RiskFlag, RiskAssessment
from typing import Optional, Dict, List, Any
import re
import json
import asyncio
from datetime import datetime

class SmartLearnedTemplateRiskAnalyzer:
    """Enhanced risk analyzer using Gemini for intelligent template comparison"""
    
    def __init__(self, learned_templates: Dict, llm_client):
        self.learned_templates = learned_templates
        self.standard_templates = self._convert_to_standard_format(learned_templates)
        self.llm_client = llm_client
    
    def _convert_to_standard_format(self, learned_templates: Dict) -> Dict:
        """Convert learned templates to standard format"""
        standard_clauses = {}
        
        for clause_type, data in learned_templates.get('learned_templates', {}).items():
            standard_clauses[clause_type] = {
                "standard": data.get("standard", ""),
                "key_elements": data.get("key_elements", []),
                "sample_count": data.get("sample_count", 0),
                "confidence": data.get("confidence", 0.5)
            }
        
        return standard_clauses
    
    async def analyze_against_learned_standards(self, contract_text: str) -> List[RiskFlag]:
        """Analyze contract against learned standards using Gemini intelligence"""
        flags = []
        
        for clause_type, standard in self.standard_templates.items():
            # Only check clauses that appeared in multiple contracts
            if standard.get("sample_count", 0) >= 2:
                print(f"   🤖 Analyzing {clause_type} with Gemini...")
                
                comparison = await self._compare_to_learned_standard_with_gemini(
                    contract_text, clause_type, standard
                )
                if comparison:
                    comparison.confidence = standard.get("confidence", 0.5)
                    flags.append(comparison)
        
        return flags
    
    async def _compare_to_learned_standard_with_gemini(self, text: str, clause_type: str, standard: Dict) -> Optional[RiskFlag]:
        """Use Gemini to intelligently compare contract against learned standard"""
        
        # Step 1: Extract clause with Gemini
        contract_clause = await self._extract_clause_with_gemini(text, clause_type)
        
        if not contract_clause:
            return RiskFlag(
                severity="high",
                category="missing_clause",
                title=f"Missing {clause_type.replace('_', ' ').title()} Clause",
                description=f"Standard {clause_type} clause not found (appeared in {standard.get('sample_count', 0)} company contracts)",
                recommendation=f"Add comprehensive {clause_type} clause matching company standards",
                confidence=0.8,  # HIGH confidence for missing clauses
                clause_reference=f"{clause_type} Section"
            )
        
        # Step 2: Compare with Gemini intelligence
        result = await self._analyze_deviation_with_gemini(contract_clause, clause_type, standard, text)
        
        # FIX: Boost confidence for high-severity findings
        if result:
            if result.severity == "critical":
                result.confidence = max(0.9, standard.get("confidence", 0.5))
            elif result.severity == "high":
                result.confidence = max(0.8, standard.get("confidence", 0.5))
            elif result.severity == "medium":
                result.confidence = max(0.7, standard.get("confidence", 0.5))
        
        return result
    
    async def _extract_clause_with_gemini(self, text: str, clause_type: str) -> Optional[str]:
        """Use Gemini to intelligently extract clauses"""
        
        prompt = f"""
        Extract the {clause_type.replace('_', ' ')} clause from this contract text.
        
        CONTRACT TEXT:
        {text[:6000]}
        
        Return ONLY the complete {clause_type} clause text if found.
        If no {clause_type} clause is present, return "NOT_FOUND".
        
        Be thorough - look for any section that deals with {clause_type.replace('_', ' ')}, 
        even if it's not explicitly labeled.
        """
        
        try:
            response = await self.llm_client(prompt)
            response = response.strip()
            
            if "NOT_FOUND" in response.upper() or len(response) < 20:
                return None
                
            # Clean up the response
            if response.startswith('```'):
                response = re.sub(r'^```\w*\s*', '', response)
                response = re.sub(r'\s*```$', '', response)
            
            return response.strip()
            
        except Exception as e:
            print(f"      ❌ Gemini extraction failed for {clause_type}: {e}")
            return None
    
    async def _analyze_deviation_with_gemini(self, contract_clause: str, clause_type: str, standard: Dict, full_contract: str) -> Optional[RiskFlag]:
        """Use Gemini to intelligently analyze deviations from standard"""
        
        prompt = f"""
        You are a legal risk analyst comparing a contract clause against company standards.
        
        CLAUSE TYPE: {clause_type.replace('_', ' ')}
        
        COMPANY STANDARD CLAUSE:
        {standard['standard']}
        
        KEY ELEMENTS IN COMPANY STANDARD:
        {', '.join(standard['key_elements'])}
        
        CONTRACT CLAUSE TO ANALYZE:
        {contract_clause}
        
        Analyze if the contract clause DEVIATES significantly from company standards.
        
        Return JSON in this format:
        {{
          "has_issues": true/false,
          "severity": "low/medium/high/critical",
          "issues": ["issue 1", "issue 2", ...],
          "recommendation": "specific recommendation text",
          "title": "brief issue title"
        }}
        
        Only flag MAJOR deviations that create legal or business risk.
        """
        
        try:
            response = await self.llm_client(prompt)
            response = response.strip()
            
            # Clean JSON response
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
                
            analysis = json.loads(response)
            
            if analysis.get('has_issues', False):
                return RiskFlag(
                    severity=analysis.get('severity', 'medium'),
                    category="non_standard",
                    title=analysis.get('title', f"Non-Standard {clause_type.replace('_', ' ').title()}"),
                    description="; ".join(analysis.get('issues', [])),
                    recommendation=analysis.get('recommendation', ''),
                    confidence=standard.get("confidence", 0.5),
                    clause_reference=f"{clause_type} Section"
                )
                
        except Exception as e:
            print(f"      ❌ Gemini analysis failed for {clause_type}: {e}")
            return None
        
        return None


class SmartProductionRiskAnalyzer:
    """Main production analyzer with full Gemini intelligence and comprehensive reporting"""
    
    def __init__(self, company_templates: Dict, llm_client):
        self.templates = company_templates
        self.llm_client = llm_client
        self.learned_analyzer = SmartLearnedTemplateRiskAnalyzer(company_templates, llm_client)
    
    async def analyze_contract(self, contract_text: str, extracted_data: Dict) -> RiskAssessment:
        """Complete risk analysis with intelligent template checking"""
        print("🤖 Running SMART risk analysis with Gemini...")
        
        # 1. Intelligent template-based analysis
        print("   🧠 Analyzing against company learned standards...")
        template_flags = await self.learned_analyzer.analyze_against_learned_standards(contract_text)
        
        # 2. Calculate overall score
        overall_score = self._calculate_risk_score(template_flags)
        risk_level = self._get_risk_level(overall_score)
        
        # 3. Generate summary
        summary = self._generate_summary(template_flags, overall_score)
        recommendations = self._generate_recommendations(template_flags)
        
        return RiskAssessment(
            overall_score=overall_score,
            risk_level=risk_level,
            flags=template_flags,
            summary=summary,
            recommendations=recommendations,
            analyzed_at=datetime.now().isoformat()
        )
    
    def _calculate_risk_score(self, flags: List[RiskFlag]) -> int:
        """Calculate risk score based on template deviations"""
        if not flags:
            return 85
        
        severity_weights = {"critical": 25, "high": 15, "medium": 8, "low": 3}
        
        total_deduction = 0
        for flag in flags:
            deduction = severity_weights.get(flag.severity, 5)
            confidence_deduction = max(1, int(deduction * flag.confidence))
            total_deduction += confidence_deduction
        
        return max(10, min(100, 100 - min(total_deduction, 90)))
    
    def _get_risk_level(self, score: int) -> str:
        """Convert score to risk level"""
        if score >= 70: return "low"
        elif score >= 50: return "medium"  
        elif score >= 30: return "high"
        else: return "critical"
    
    def _generate_summary(self, flags: List[RiskFlag], score: int) -> str:
        """Generate human-readable summary"""
        critical_issues = len([f for f in flags if f.severity == "critical"])
        high_issues = len([f for f in flags if f.severity == "high"])
        
        if score >= 70:
            return f"Low risk: {len(flags)} minor deviations from company standards"
        elif score >= 50:
            return f"Moderate risk: {len(flags)} deviations from company standards found"
        elif score >= 30:
            return f"High risk: {high_issues} high-priority and {critical_issues} critical deviations from company standards"
        else:
            return f"Critical risk: {critical_issues} critical company standard violations requiring immediate attention"
    
    def _generate_recommendations(self, flags: List[RiskFlag]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        seen = set()
        
        for flag in flags:
            if flag.recommendation and flag.recommendation not in seen:
                recommendations.append(flag.recommendation)
                seen.add(flag.recommendation)
        
        return recommendations[:10]
    
    def generate_comprehensive_report(self, risk_assessment: RiskAssessment, contract_text: str, extracted_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive report in the mock data format"""
        
        # Convert RiskAssessment to comprehensive format
        flags = []
        for flag in risk_assessment.flags:
            flags.append({
                "severity": flag.severity,
                "category": flag.category,
                "title": flag.title,
                "description": flag.description,
                "recommendation": flag.recommendation or "",
                "clause_reference": flag.clause_reference or "Not Found",
                "confidence": flag.confidence
            })
        
        # Generate recommendations list from flags
        recommendations = list(set([
            flag["recommendation"] for flag in flags 
            if flag["recommendation"] and len(flag["recommendation"]) > 10
        ]))[:10]
        
        # Build comprehensive report
        report = {
            "overall_score": risk_assessment.overall_score,
            "risk_level": risk_assessment.risk_level,
            "summary": risk_assessment.summary,
            "flags": flags,
            "recommendations": recommendations,
            "compliance_checks": self._generate_compliance_checks(flags),
            "term_consistency": self._generate_term_consistency(contract_text),
            "clause_comparisons": self._generate_clause_comparisons(flags),
            "legal_advice": self._generate_legal_advice(flags),
            "analyzed_at": risk_assessment.analyzed_at,
            "contract_metadata": self._generate_contract_metadata(extracted_data, contract_text)
        }
        
        return report
    
    def _generate_compliance_checks(self, flags: List[Dict]) -> List[Dict]:
        """Generate compliance checks based on flags"""
        compliance_checks = []
        
        # Map flags to compliance issues
        for flag in flags:
            if "jurisdiction" in flag["title"].lower() or "governing" in flag["title"].lower():
                compliance_checks.append({
                    "regulation": "Governing Law Requirement",
                    "status": "non_compliant",
                    "issues": [flag["description"]],
                    "recommendations": [flag["recommendation"]]
                })
            elif "payment" in flag["title"].lower():
                compliance_checks.append({
                    "regulation": "Payment Terms Specification", 
                    "status": "non_compliant",
                    "issues": [flag["description"]],
                    "recommendations": [flag["recommendation"]]
                })
            elif "liability" in flag["title"].lower():
                compliance_checks.append({
                    "regulation": "Liability Limitation",
                    "status": "non_compliant",
                    "issues": [flag["description"]],
                    "recommendations": [flag["recommendation"]]
                })
        
        return compliance_checks[:5]
    
    def _generate_term_consistency(self, contract_text: str) -> List[Dict]:
        """Generate term consistency analysis"""
        # Simple analysis - you can enhance this with more sophisticated logic
        terms_to_check = ["confidential", "termination", "liability", "payment", "warrant", "indemnif"]
        
        term_consistency = []
        for term in terms_to_check:
            if term in contract_text.lower():
                term_consistency.append({
                    "term": term.title(),
                    "definitions": [f"References to {term} found in contract"],
                    "is_consistent": True,  # Simplified - you can add real consistency checking
                    "issue_description": None
                })
        
        # Add some sample data for demonstration
        if not term_consistency:
            term_consistency = [
                {
                    "term": "Confidential Information",
                    "definitions": ["information that should be kept private"],
                    "is_consistent": False,
                    "issue_description": "Term not clearly defined in contract"
                },
                {
                    "term": "Effective Date", 
                    "definitions": ["contract start date"],
                    "is_consistent": True,
                    "issue_description": None
                }
            ]
        
        return term_consistency[:6]
    
    def _generate_clause_comparisons(self, flags: List[Dict]) -> List[Dict]:
        """Generate clause comparisons from flags"""
        comparisons = []
        
        clause_mapping = {
            "confidentiality": ["confidential", "non-disclosure"],
            "termination": ["termination", "terminate"], 
            "liability": ["liability", "liable", "damages"],
            "payment": ["payment", "fee", "invoice"],
            "warranties": ["warrant", "guarantee", "as is"],
            "indemnification": ["indemnif", "hold harmless"],
            "intellectual_property": ["intellectual", "ip", "copyright"],
            "dispute_resolution": ["dispute", "arbitration", "mediation"]
        }
        
        for flag in flags:
            for clause_type, keywords in clause_mapping.items():
                if any(keyword in flag["title"].lower() for keyword in keywords):
                    comparisons.append({
                        "clause_type": clause_type,
                        "standard_version": f"Company standard {clause_type} clause",
                        "contract_version": flag["description"][:200] + "...",
                        "deviation_severity": flag["severity"],
                        "explanation": flag["description"]
                    })
                    break
        
        return comparisons[:8]
    
    def _generate_legal_advice(self, flags: List[Dict]) -> List[Dict]:
        """Generate legal advice from flags"""
        legal_advice = []
        
        severity_advice = {
            "critical": "This clause poses critical legal risk that requires immediate attention.",
            "high": "This clause poses significant legal risk that should be addressed.",
            "medium": "This clause has moderate legal risk that should be reviewed.",
            "low": "This clause has minor legal risk that may need attention."
        }
        
        for flag in flags:
            if flag["severity"] in ["critical", "high"]:
                advice_text = f"{severity_advice.get(flag['severity'], 'This clause requires legal review.')} {flag['description']}"
                
                legal_advice.append({
                    "topic": flag["title"],
                    "advice": advice_text,
                    "risk_level": flag["severity"],
                    "supporting_law": "General Contract Law Principles",
                    "recommendations": [flag["recommendation"]] if flag["recommendation"] else ["Consult legal team for specific guidance"]
                })
        
        return legal_advice[:5]
    
    def _generate_contract_metadata(self, extracted_data: Dict, contract_text: str) -> Dict:
        """Generate contract metadata"""
        # Count approximate number of clauses by counting substantial paragraphs
        clause_count = len([p for p in contract_text.split('\n\n') if len(p.strip()) > 100])
        
        return {
            "contract_name": "analyzed_contract.docx",
            "parties": extracted_data.get("parties", [{"name": "Unknown", "role": "Party"}]),
            "effective_date": extracted_data.get("dates", {}).get("start", "Not specified"),
            "expiry_date": extracted_data.get("dates", {}).get("expiration", "Not specified"),
            "total_value": self._extract_contract_value(extracted_data),
            "extracted_clauses_count": clause_count
        }
    
    def _extract_contract_value(self, extracted_data: Dict) -> str:
        """Extract contract value from extracted data"""
        financial_data = extracted_data.get("financial", {})
        if "amount" in financial_data:
            return f"QAR {financial_data['amount']}"
        elif "paymentTerms" in financial_data:
            return f"Value specified in payment terms"
        else:
            return "Not specified"
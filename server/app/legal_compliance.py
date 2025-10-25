"""
FIXED LEGAL COMPLIANCE ANALYZER - Integrated with Risk Analysis
"""

import json
import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

class LegalComplianceAnalyzer:
    """Real legal compliance analyzer using Gemini"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.legal_database_path = "legal_database"
        self.legal_frameworks = {
            "qatar": {
                "civil_code_contracts": "Qatar Civil Code - Contracts",
                "commercial_companies_law": "Qatar Commercial Companies Law", 
                "labour_law": "Qatar Labour Law",
                "data_protection": "Qatar Data Protection Regulations"
            },
            "uk": {
                "unfair_contract_terms_1977": "UK Unfair Contract Terms Act 1977",
                "sale_of_goods_1979": "UK Sale of Goods Act 1979",
                "supply_of_goods_services_1982": "UK Supply of Goods and Services Act 1982",
                "data_protection_2018": "UK Data Protection Act 2018"
            },
            "us": {
                "uniform_commercial_code": "US Uniform Commercial Code Article 2",
                "restatement_contracts": "US Restatement of Contracts Second"
            }
        }
    
    async def analyze_legal_compliance(
        self, 
        contract_text: str, 
        jurisdiction: str,
        risk_flags: List[Dict] = None,
        contract_id: str = None
    ) -> Dict[str, Any]:
        """
        Analyze contract compliance with jurisdiction laws using REAL Gemini
        
        Args:
            contract_text: Full contract text
            jurisdiction: Target jurisdiction (qatar, uk, us)
            risk_flags: Previously identified risk flags
            contract_id: Optional contract identifier
        """
        print(f"⚖️ LEGAL COMPLIANCE ANALYSIS: {jurisdiction.upper()}")
        
        if not contract_id:
            contract_id = f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        jurisdiction = jurisdiction.lower()
        
        # Load country-specific laws
        laws = self._load_country_laws(jurisdiction)
        
        if not laws:
            print(f"⚠️ No legal database found for {jurisdiction}")
            return self._create_empty_compliance_report(jurisdiction, contract_id)
        
        print(f"📚 Loaded {len(laws)} laws for {jurisdiction}")
        
        # Analyze compliance for each law using REAL Gemini
        compliance_results = []
        for law_name, law_content in laws.items():
            print(f"   🔍 Analyzing: {law_name}...")
            
            compliance = await self._analyze_law_compliance(
                contract_text, 
                law_name, 
                law_content, 
                risk_flags or [],
                jurisdiction
            )
            
            if compliance:
                compliance_results.append(compliance)
        
        # Build comprehensive report
        compliance_report = {
            "contract_id": contract_id,
            "jurisdiction": jurisdiction.upper(),
            "analyzed_at": datetime.now().isoformat(),
            "compliance_summary": self._generate_compliance_summary(compliance_results),
            "law_analysis": compliance_results,
            "legal_risks": self._extract_legal_risks(compliance_results),
            "recommendations": self._generate_legal_recommendations(compliance_results),
            "critical_violations": self._identify_critical_violations(compliance_results),
            "metadata": {
                "total_laws_available": len(laws),
                "total_laws_analyzed": len(compliance_results),
                "analysis_method": "Gemini AI Legal Analysis",
                "legal_database_used": True
            }
        }
        
        # Save report
        self._save_compliance_report(compliance_report)
        
        print(f"✅ Legal compliance analysis complete")
        print(f"   Score: {compliance_report['compliance_summary']['overall_compliance_score']}/100")
        print(f"   Status: {compliance_report['compliance_summary']['status']}")
        
        return compliance_report

    async def _analyze_law_compliance(
        self, 
        contract_text: str, 
        law_name: str, 
        law_text: str, 
        risk_flags: List[Dict],
        jurisdiction: str
    ) -> Optional[Dict]:
        """REAL Gemini analysis comparing contract with actual laws"""
        
        # Build context from risk flags
        risk_context = ""
        if risk_flags:
            risk_context = "\n\nKNOWN RISKS IN CONTRACT:\n"
            for flag in risk_flags[:5]:
                risk_context += f"- {flag.get('title', '')}: {flag.get('description', '')}\n"
        
        prompt = f"""
        LEGAL COMPLIANCE ANALYSIS - Be Specific and Critical

        You are a legal expert analyzing contract compliance with {law_name}.

        JURISDICTION: {jurisdiction.upper()}
        LAW: {law_name}

        LAW CONTENT (Key Provisions):
        {law_text[:4000]}

        CONTRACT TO ANALYZE:
        {contract_text[:4000]}
        {risk_context}

        **CRITICAL ANALYSIS REQUIRED:**
        
        1. Identify SPECIFIC violations of this law
        2. Reference ACTUAL articles/sections violated
        3. Flag missing REQUIRED provisions under this law
        4. Assess enforceability issues
        5. Identify legal exposure and risks

        **Return EXACT JSON format:**
        {{
          "compliance_status": "compliant|partially_compliant|non_compliant",
          "compliance_score": 0-100,
          "specific_articles_violated": [
            "Article X.Y: Specific violation description",
            "Section Z: Another specific issue"
          ],
          "compliance_issues": [
            "Specific legal issue 1",
            "Specific legal issue 2"
          ],
          "legal_risks": [
            "Specific legal risk 1",
            "Specific legal risk 2"
          ],
          "recommendations": [
            "Specific actionable fix 1",
            "Specific actionable fix 2"
          ],
          "severity": "low|medium|high|critical",
          "missing_required_clauses": [
            "Required clause 1",
            "Required clause 2"
          ]
        }}

        **SCORING GUIDE:**
        - 90-100: Fully compliant
        - 70-89: Mostly compliant (minor issues)
        - 50-69: Partially compliant (significant issues)
        - 0-49: Non-compliant (critical violations)

        BE CRITICAL: If there are known risks, find the legal violations.
        BE SPECIFIC: Reference actual law provisions.
        BE REALISTIC: Score based on actual compliance.
        """
        
        try:
            response = await self.llm_client(prompt)
            response = response.strip()
            
            # Clean JSON
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            analysis = json.loads(response)
            
            # Validate and structure the response
            return self._structure_compliance_result(analysis, law_name)
            
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON parse error for {law_name}: {e}")
            return self._create_fallback_analysis(law_name, risk_flags, "json_error")
        except Exception as e:
            print(f"   ❌ Analysis failed for {law_name}: {e}")
            return self._create_fallback_analysis(law_name, risk_flags, "analysis_error")

    def _structure_compliance_result(self, analysis: Dict, law_name: str) -> Dict:
        """Structure and validate the compliance result"""
        
        # Ensure all required fields exist
        result = {
            "law": law_name,
            "compliance_status": analysis.get("compliance_status", "unknown"),
            "compliance_score": int(analysis.get("compliance_score", 50)),
            "specific_articles_violated": analysis.get("specific_articles_violated", []),
            "compliance_issues": analysis.get("compliance_issues", []),
            "legal_risks": analysis.get("legal_risks", []),
            "recommendations": analysis.get("recommendations", []),
            "severity": analysis.get("severity", "medium"),
            "missing_required_clauses": analysis.get("missing_required_clauses", [])
        }
        
        # Ensure lists
        for key in ["specific_articles_violated", "compliance_issues", "legal_risks", "recommendations", "missing_required_clauses"]:
            if not isinstance(result[key], list):
                result[key] = [result[key]] if result[key] else []
        
        # Validate compliance status
        valid_statuses = ["compliant", "partially_compliant", "non_compliant", "unknown"]
        if result["compliance_status"] not in valid_statuses:
            result["compliance_status"] = "unknown"
        
        # Validate severity
        valid_severities = ["low", "medium", "high", "critical"]
        if result["severity"] not in valid_severities:
            result["severity"] = "medium"
        
        return result

    def _create_fallback_analysis(self, law_name: str, risk_flags: List[Dict], error_type: str) -> Dict:
        """Create fallback when Gemini analysis fails"""
        
        # Check if we have critical risks
        has_critical = any(
            flag.get('severity') in ['critical', 'high'] 
            for flag in risk_flags
        )
        
        if has_critical:
            return {
                "law": law_name,
                "compliance_status": "non_compliant",
                "compliance_score": 35,
                "specific_articles_violated": ["Analysis incomplete - critical risks detected"],
                "compliance_issues": [
                    f"Legal analysis failed ({error_type})",
                    "Contract contains high-risk clauses requiring legal review"
                ],
                "legal_risks": ["Unknown compliance status due to analysis failure"],
                "recommendations": [
                    "Consult legal counsel for complete compliance review",
                    f"Manual review required for {law_name}"
                ],
                "severity": "high",
                "missing_required_clauses": []
            }
        else:
            return {
                "law": law_name,
                "compliance_status": "unknown",
                "compliance_score": 50,
                "specific_articles_violated": [],
                "compliance_issues": [f"Legal analysis could not be completed ({error_type})"],
                "legal_risks": ["Compliance status unknown"],
                "recommendations": ["Review with legal team"],
                "severity": "medium",
                "missing_required_clauses": []
            }

    def _load_country_laws(self, jurisdiction: str) -> Dict[str, str]:
        """Load jurisdiction-specific laws from database"""
        jurisdiction_path = os.path.join(self.legal_database_path, jurisdiction.lower())
        laws = {}
        
        if not os.path.exists(jurisdiction_path):
            print(f"⚠️ Legal database path not found: {jurisdiction_path}")
            return laws
        
        try:
            for filename in os.listdir(jurisdiction_path):
                if filename.endswith('.txt'):
                    law_key = filename.replace('.txt', '')
                    law_name = self.legal_frameworks.get(jurisdiction, {}).get(
                        law_key, 
                        law_key.replace('_', ' ').title()
                    )
                    
                    file_path = os.path.join(jurisdiction_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        laws[law_name] = f.read()
            
            return laws
            
        except Exception as e:
            print(f"❌ Failed to load laws: {e}")
            return {}

    def _generate_compliance_summary(self, results: List[Dict]) -> Dict:
        """Generate overall compliance summary"""
        if not results:
            return {
                "overall_compliance_score": 0,
                "status": "unknown",
                "total_laws_analyzed": 0,
                "compliant_laws": 0,
                "non_compliant_laws": 0,
                "critical_violations_count": 0
            }
        
        total = len(results)
        compliant = len([r for r in results if r['compliance_status'] == 'compliant'])
        non_compliant = len([r for r in results if r['compliance_status'] in ['partially_compliant', 'non_compliant']])
        critical = len([r for r in results if r['severity'] == 'critical'])
        
        # Calculate weighted average score
        scores = [r['compliance_score'] for r in results]
        avg_score = round(sum(scores) / len(scores)) if scores else 0
        
        # Determine overall status
        if avg_score >= 80:
            status = "compliant"
        elif avg_score >= 60:
            status = "partially_compliant"
        else:
            status = "non_compliant"
        
        return {
            "overall_compliance_score": avg_score,
            "status": status,
            "total_laws_analyzed": total,
            "compliant_laws": compliant,
            "non_compliant_laws": non_compliant,
            "critical_violations_count": critical
        }

    def _extract_legal_risks(self, results: List[Dict]) -> List[Dict]:
        """Extract legal risks from compliance analysis"""
        risks = []
        
        for result in results:
            if result['compliance_status'] in ['partially_compliant', 'non_compliant']:
                risks.append({
                    "law": result['law'],
                    "severity": result['severity'],
                    "issues": result['compliance_issues'],
                    "articles_violated": result['specific_articles_violated'],
                    "risks": result['legal_risks'],
                    "compliance_score": result['compliance_score']
                })
        
        return risks

    def _identify_critical_violations(self, results: List[Dict]) -> List[Dict]:
        """Identify critical violations"""
        violations = []
        
        for result in results:
            if result['severity'] == 'critical':
                violations.append({
                    "law": result['law'],
                    "issues": result['compliance_issues'][:3],
                    "articles_violated": result['specific_articles_violated'],
                    "recommendations": result['recommendations'][:2]
                })
        
        return violations

    def _generate_legal_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate consolidated legal recommendations"""
        recommendations = []
        seen = set()
        
        for result in results:
            for rec in result.get('recommendations', []):
                if isinstance(rec, str) and rec not in seen and len(rec) > 10:
                    recommendations.append(rec)
                    seen.add(rec)
        
        return recommendations[:10]

    def _create_empty_compliance_report(self, jurisdiction: str, contract_id: str) -> Dict:
        """Create empty report when no laws available"""
        return {
            "contract_id": contract_id,
            "jurisdiction": jurisdiction.upper(),
            "analyzed_at": datetime.now().isoformat(),
            "compliance_summary": {
                "overall_compliance_score": 0,
                "status": "unknown",
                "total_laws_analyzed": 0,
                "compliant_laws": 0,
                "non_compliant_laws": 0,
                "critical_violations_count": 0
            },
            "law_analysis": [],
            "legal_risks": [],
            "recommendations": [f"No legal database found for {jurisdiction}"],
            "critical_violations": [],
            "metadata": {
                "total_laws_available": 0,
                "total_laws_analyzed": 0,
                "analysis_method": "Gemini AI",
                "legal_database_used": False
            }
        }

    def _save_compliance_report(self, report: Dict):
        """Save compliance report to file"""
        os.makedirs("data/legal_compliance", exist_ok=True)
        
        # Save individual report
        filename = f"data/legal_compliance/{report['contract_id']}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved compliance report: {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
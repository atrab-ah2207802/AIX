"""
COMPLETE RISK ANALYSIS INTEGRATION
Combines base risk analysis + template comparison + legal compliance
"""

from typing import Dict, List, Any
import asyncio
from datetime import datetime

# Import from your modules
from .risk import analyze_contract_risk, call_llm, RiskAssessment
from .legal_compliance import LegalComplianceAnalyzer
from .learned_analyzer import SmartProductionRiskAnalyzer

class CompleteRiskAnalyzer:
    """
    Complete risk analyzer that integrates:
    1. Base risk analysis (from risk.py)
    2. Template-based comparison (from learned_analyzer.py)
    3. Legal compliance checking (from legal_compliance.py)
    """
    
    def __init__(self, company_templates: Dict = None):
        """
        Initialize complete analyzer
        
        Args:
            company_templates: Learned templates from template_learner.py
        """
        self.llm_client = call_llm
        self.legal_analyzer = LegalComplianceAnalyzer(self.llm_client)
        
        # Initialize template analyzer if templates provided
        if company_templates:
            self.template_analyzer = SmartProductionRiskAnalyzer(
                company_templates, 
                self.llm_client
            )
        else:
            self.template_analyzer = None
            print("⚠️ No company templates provided - template analysis disabled")
    
    async def analyze_complete(
        self, 
        contract_text: str, 
        extracted_data: Dict,
        jurisdiction: str = "qatar"
    ) -> Dict[str, Any]:
        """
        Complete risk analysis combining all methods
        
        Args:
            contract_text: Full contract text
            extracted_data: Previously extracted contract data
            jurisdiction: Target jurisdiction (qatar, uk, us)
            
        Returns:
            Complete risk report with all analyses
        """
        print("=" * 60)
        print("🚀 COMPLETE RISK ANALYSIS STARTED")
        print("=" * 60)
        
        # STEP 1: Base Risk Analysis
        print("\n📊 STEP 1: Base Risk Analysis")
        base_risk = await analyze_contract_risk(
            contract_text,
            extracted_data,
            jurisdiction
        )
        
        print(f"   ✅ Base analysis complete: {len(base_risk.flags)} risks found")
        print(f"   Risk Score: {base_risk.overall_score}/100 ({base_risk.risk_level})")
        
        # STEP 2: Template-Based Analysis (if available)
        template_flags = []
        if self.template_analyzer:
            print("\n🧠 STEP 2: Template-Based Analysis")
            template_assessment = await self.template_analyzer.analyze_contract(
                contract_text,
                extracted_data
            )
            template_flags = template_assessment.flags
            print(f"   ✅ Template analysis complete: {len(template_flags)} deviations found")
        else:
            print("\n⏭️  STEP 2: Template analysis skipped (no templates)")
        
        # STEP 3: Legal Compliance Analysis
        print(f"\n⚖️  STEP 3: Legal Compliance Analysis ({jurisdiction.upper()})")
        
        # Convert RiskFlags to dict format for legal analyzer
        risk_flags_dict = [
            {
                "severity": flag.severity,
                "category": flag.category,
                "title": flag.title,
                "description": flag.description,
                "recommendation": flag.recommendation
            }
            for flag in base_risk.flags
        ]
        
        legal_compliance = await self.legal_analyzer.analyze_legal_compliance(
            contract_text,
            jurisdiction,
            risk_flags_dict,
            contract_id=extracted_data.get("contract_id", "unknown")
        )
        
        print(f"   ✅ Legal compliance complete")
        print(f"   Compliance Score: {legal_compliance['compliance_summary']['overall_compliance_score']}/100")
        print(f"   Status: {legal_compliance['compliance_summary']['status'].upper()}")
        
        # STEP 4: Merge Results
        print("\n🔄 STEP 4: Merging All Results")
        complete_report = self._merge_all_results(
            base_risk,
            template_flags,
            legal_compliance,
            contract_text,
            extracted_data,
            jurisdiction
        )
        
        print("\n" + "=" * 60)
        print("✅ COMPLETE RISK ANALYSIS FINISHED")
        print(f"   Overall Risk Score: {complete_report['overall_score']}/100")
        print(f"   Risk Level: {complete_report['risk_level'].upper()}")
        print(f"   Total Flags: {len(complete_report['all_flags'])}")
        print(f"   Critical Issues: {complete_report['critical_count']}")
        print(f"   Legal Compliance: {legal_compliance['compliance_summary']['status'].upper()}")
        print("=" * 60)
        
        return complete_report
    
    def _merge_all_results(
        self,
        base_risk: RiskAssessment,
        template_flags: List,
        legal_compliance: Dict,
        contract_text: str,
        extracted_data: Dict,
        jurisdiction: str
    ) -> Dict[str, Any]:
        """Merge all analysis results into comprehensive report"""
        
        # Combine all flags
        all_flags = []
        
        # Add base risk flags
        for flag in base_risk.flags:
            all_flags.append({
                "source": "base_analysis",
                "severity": flag.severity,
                "category": flag.category,
                "title": flag.title,
                "description": flag.description,
                "recommendation": flag.recommendation,
                "clause_reference": flag.clause_reference,
                "confidence": flag.confidence
            })
        
        # Add template flags (if any)
        for flag in template_flags:
            all_flags.append({
                "source": "template_comparison",
                "severity": flag.severity,
                "category": flag.category,
                "title": flag.title,
                "description": flag.description,
                "recommendation": flag.recommendation,
                "clause_reference": flag.clause_reference,
                "confidence": flag.confidence
            })
        
        # Add legal compliance issues as flags
        for risk in legal_compliance.get('legal_risks', []):
            all_flags.append({
                "source": "legal_compliance",
                "severity": risk.get('severity', 'high'),
                "category": "legal_violation",
                "title": f"Legal Issue: {risk.get('law', 'Unknown Law')}",
                "description": "; ".join(risk.get('issues', [])),
                "recommendation": "; ".join(risk.get('risks', [])),
                "clause_reference": ", ".join(risk.get('articles_violated', [])[:2]),
                "confidence": 0.90
            })
        
        # Calculate comprehensive scores
        overall_score = self._calculate_comprehensive_score(
            base_risk.overall_score,
            legal_compliance['compliance_summary']['overall_compliance_score'],
            all_flags
        )
        
        risk_level = self._get_risk_level(overall_score)
        
        # Count critical issues
        critical_count = len([f for f in all_flags if f['severity'] == 'critical'])
        high_count = len([f for f in all_flags if f['severity'] == 'high'])
        
        # Generate consolidated recommendations
        all_recommendations = list(set(
            base_risk.recommendations +
            legal_compliance.get('recommendations', [])
        ))
        
        # Build comprehensive report
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "contract_metadata": {
                "contract_id": extracted_data.get("contract_id", "unknown"),
                "jurisdiction": jurisdiction.upper(),
                "parties": extracted_data.get("parties", []),
                "effective_date": extracted_data.get("dates", {}).get("start"),
                "expiry_date": extracted_data.get("dates", {}).get("expiration")
            },
            
            # Overall Scores
            "overall_score": overall_score,
            "risk_level": risk_level,
            "critical_count": critical_count,
            "high_count": high_count,
            
            # All Risk Flags
            "all_flags": all_flags,
            "total_flags": len(all_flags),
            
            # Base Risk Analysis
            "base_risk_analysis": {
                "score": base_risk.overall_score,
                "risk_level": base_risk.risk_level,
                "summary": base_risk.summary,
                "flags_count": len(base_risk.flags)
            },
            
            # Legal Compliance
            "legal_compliance": legal_compliance,
            
            # Template Comparison (if available)
            "template_comparison": {
                "analyzed": len(template_flags) > 0,
                "deviations_found": len(template_flags),
                "flags": template_flags if template_flags else []
            },
            
            # Consolidated Recommendations
            "recommendations": all_recommendations[:15],
            
            # Executive Summary
            "executive_summary": self._generate_executive_summary(
                overall_score,
                critical_count,
                high_count,
                legal_compliance,
                all_flags
            ),
            
            # Compliance Checks (formatted for frontend)
            "compliance_checks": self._format_compliance_checks(legal_compliance),
            
            # Legal Advice
            "legal_advice": self._format_legal_advice(legal_compliance, all_flags),
            
            # Analysis Metadata
            "analysis_metadata": {
                "methods_used": [
                    "base_risk_analysis",
                    "legal_compliance_check",
                    "template_comparison" if template_flags else None
                ],
                "jurisdiction_analyzed": jurisdiction.upper(),
                "laws_analyzed": legal_compliance['metadata']['total_laws_analyzed'],
                "total_analysis_time": "Complete"
            }
        }
    
    def _calculate_comprehensive_score(
        self,
        base_score: int,
        legal_score: int,
        all_flags: List[Dict]
    ) -> int:
        """Calculate overall score from all sources"""
        
        # Weight: 40% base risk, 60% legal compliance
        weighted_score = (base_score * 0.4) + (legal_score * 0.6)
        
        # Apply penalty for critical flags
        critical_penalty = len([f for f in all_flags if f['severity'] == 'critical']) * 5
        high_penalty = len([f for f in all_flags if f['severity'] == 'high']) * 3
        
        final_score = max(0, min(100, weighted_score - critical_penalty - high_penalty))
        
        return round(final_score)
    
    def _get_risk_level(self, score: int) -> str:
        """Convert score to risk level"""
        if score >= 75:
            return "low"
        elif score >= 55:
            return "medium"
        elif score >= 35:
            return "high"
        else:
            return "critical"
    
    def _generate_executive_summary(
        self,
        overall_score: int,
        critical_count: int,
        high_count: int,
        legal_compliance: Dict,
        all_flags: List[Dict]
    ) -> str:
        """Generate executive summary"""
        
        compliance_status = legal_compliance['compliance_summary']['status']
        
        if overall_score >= 75:
            summary = f"Contract shows low risk with compliance score of {overall_score}/100. "
        elif overall_score >= 55:
            summary = f"Contract shows moderate risk with compliance score of {overall_score}/100. "
        elif overall_score >= 35:
            summary = f"Contract shows high risk with compliance score of {overall_score}/100. "
        else:
            summary = f"Contract shows critical risk with compliance score of {overall_score}/100. "
        
        summary += f"Legal compliance status: {compliance_status.upper()}. "
        
        if critical_count > 0:
            summary += f"Found {critical_count} critical and {high_count} high-priority issues requiring immediate attention. "
        elif high_count > 0:
            summary += f"Found {high_count} high-priority issues requiring attention. "
        else:
            summary += "No critical issues identified. "
        
        # Add specific concerns
        legal_risks_count = len(legal_compliance.get('legal_risks', []))
        if legal_risks_count > 0:
            summary += f"Identified {legal_risks_count} legal compliance concerns. "
        
        summary += "Detailed analysis and recommendations provided below."
        
        return summary
    
    def _format_compliance_checks(self, legal_compliance: Dict) -> List[Dict]:
        """Format compliance checks for frontend display"""
        checks = []
        
        for law_analysis in legal_compliance.get('law_analysis', []):
            checks.append({
                "regulation": law_analysis.get('law', 'Unknown Law'),
                "status": law_analysis.get('compliance_status', 'unknown'),
                "score": law_analysis.get('compliance_score', 0),
                "issues": law_analysis.get('compliance_issues', []),
                "recommendations": law_analysis.get('recommendations', [])
            })
        
        return checks
    
    def _format_legal_advice(self, legal_compliance: Dict, all_flags: List[Dict]) -> List[Dict]:
        """Format legal advice for frontend display"""
        advice = []
        
        # Add critical legal risks
        for risk in legal_compliance.get('legal_risks', []):
            if risk.get('severity') in ['critical', 'high']:
                advice.append({
                    "topic": risk.get('law', 'Legal Compliance'),
                    "severity": risk.get('severity', 'high'),
                    "issues": risk.get('issues', []),
                    "risks": risk.get('risks', []),
                    "articles_violated": risk.get('articles_violated', []),
                    "advice": f"This contract has {len(risk.get('issues', []))} compliance issues with {risk.get('law')} that require legal review."
                })
        
        # Add critical flags as legal advice
        critical_flags = [f for f in all_flags if f['severity'] == 'critical'][:3]
        for flag in critical_flags:
            advice.append({
                "topic": flag['title'],
                "severity": flag['severity'],
                "issues": [flag['description']],
                "risks": [flag['recommendation']],
                "articles_violated": [flag.get('clause_reference', 'Not specified')],
                "advice": f"CRITICAL: {flag['description']}"
            })
        
        return advice[:10]


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def analyze_contract_complete_example():
    """
    Example usage of complete risk analyzer
    """
    
    # Load your learned templates (from template_learner.py)
    # company_templates = load_templates_from_file("templates.json")
    company_templates = None  # Or provide actual templates
    
    # Initialize analyzer
    analyzer = CompleteRiskAnalyzer(company_templates)
    
    # Your contract data
    contract_text = "..." # Full contract text
    extracted_data = {
        "contract_id": "CNT-2024-001",
        "parties": [{"name": "QDB", "role": "Client"}],
        "dates": {"start": "2024-01-01", "expiration": "2025-01-01"},
        "jurisdiction": "qatar"
    }
    
    # Run complete analysis
    result = await analyzer.analyze_complete(
        contract_text,
        extracted_data,
        jurisdiction="qatar"
    )
    
    # Access results
    print(f"Overall Score: {result['overall_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Total Flags: {result['total_flags']}")
    print(f"Legal Compliance: {result['legal_compliance']['compliance_summary']['status']}")
    
    return result


if __name__ == "__main__":
    # Run example
    asyncio.run(analyze_contract_complete_example())
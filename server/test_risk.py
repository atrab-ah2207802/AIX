"""
Test risk analysis module
"""

import asyncio
from app.risk import analyze_contract_risk

# Sample contract data
SAMPLE_TEXT = """
This Agreement is entered into between Company A and Company B.
The contract will automatically renew every year.
Either party may terminate with 180 days notice.
Company A shall have unlimited liability for any damages.
Payment terms: Net 90 days.
"""

SAMPLE_DATA = {
    "parties": [
        {"name": "Company A", "role": "Provider"},
        {"name": "Company B", "role": "Client"}
    ],
    "dates": {
        "start": "2024-01-01",
        "expiration": "2025-12-31"
    },
    "financial": {
        "paymentTerms": "Net 90"
    },
    "jurisdiction": ""
}

async def main():
    print("Running risk analysis...")
    result = await analyze_contract_risk(SAMPLE_TEXT, SAMPLE_DATA)
    
    print(f"\n{'='*60}")
    print(f"RISK SCORE: {result.overall_score}/100 ({result.risk_level.upper()})")
    print(f"{'='*60}")
    print(f"\n{result.summary}\n")
    
    print(f"ISSUES FOUND: {len(result.flags)}")
    for i, flag in enumerate(result.flags, 1):
        print(f"\n{i}. [{flag.severity.upper()}] {flag.title}")
        print(f"   {flag.description}")
        if flag.recommendation:
            print(f"   → {flag.recommendation}")
    
    print(f"\n{'='*60}")
    print("TOP RECOMMENDATIONS:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")
    
    print(f"\n{'='*60}")
    print("COMPLIANCE STATUS:")
    for standard, status in result.compliance_status.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {standard}")

if __name__ == "__main__":
    asyncio.run(main())
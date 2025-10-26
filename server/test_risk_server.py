# test_risk_simple.py - NO MODELS NEEDED
import requests
import json

BASE_URL = "http://localhost:8001"

def test_risk_simple():
    sample_data = {
        "doc_id": "test_001",
        "extraction": {
            "parties": [
                {"name": "QDB", "role": "Client"},
                {"name": "Vendor Inc", "role": "Supplier"}
            ],
            "dates": {
                "start": "2025-01-01",
                "expiration": "2025-12-31"
            },
            "financial": {
                "amount": "500000",
                "paymentTerms": "Net 60 days"
            }
        },
        "country": "qatar"
    }
    
    try:
        # Test health
        health = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Health: {health.json()}")
        
        # Test risk analysis - just get the raw JSON, don't validate models
        response = requests.post(f"{BASE_URL}/api/risk", json=sample_data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 SUCCESS! Your risk server is working!")
            print(f"   Score: {result.get('overall_score', 'N/A')}/100")
            print(f"   Level: {result.get('risk_level', 'N/A')}")
            print(f"   Flags: {len(result.get('flags', []))}")
            
            # Save full output
            with open("risk_server_output.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   📁 Saved to: risk_server_output.json")
            
            # Show some flags
            flags = result.get('flags', [])
            if flags:
                print("\n🔍 Top Flags:")
                for i, flag in enumerate(flags[:3], 1):
                    print(f"   {i}. [{flag.get('severity', 'N/A')}] {flag.get('title', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_risk_simple()
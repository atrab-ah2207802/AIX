# test_main_basic.py
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_main_health():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False

def test_risk_endpoint_with_sample_data():
    """Test your /api/risk endpoint with sample data"""
    # Sample data that matches your RiskRequest model
    sample_data = {
        "doc_id": "test_doc_123",
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
        response = requests.post(
            f"{BASE_URL}/api/risk",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Risk endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 SUCCESS! Your risk analysis is working!")
            print(f"   Risk Score: {result.get('overall_score')}/100")
            print(f"   Risk Level: {result.get('risk_level')}")
            print(f"   Flags Found: {len(result.get('flags', []))}")
            
            # Save the full output to see your JSON structure
            with open("main_output.json", "w") as f:
                json.dump(result, f, indent=2)
            print("   📁 Full output saved to: main_output.json")
            
        else:
            print(f"❌ Error: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Risk endpoint failed: {e}")
        return False

def main():
    print("🧪 Testing your main.py risk endpoint...")
    print("=" * 50)
    
    # First check if server is running
    if not test_main_health():
        print("\n💡 Start the server first with:")
        print("   uvicorn app.main:app --reload --port 8000")
        return
    
    # Test your risk endpoint
    print("\n🚀 Testing your risk analysis endpoint...")
    success = test_risk_endpoint_with_sample_data()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! Your main.py is working correctly!")
        print("   Check main_output.json to see your full risk analysis")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
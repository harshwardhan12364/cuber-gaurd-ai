import requests
import json
import sys

API_BASE = "http://127.0.0.1:8001/api/police"

def test_endpoint(name, method, endpoint, data=None):
    print(f"Testing {name} ({endpoint})...", end=" ", flush=True)
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE}{endpoint}")
        else:
            response = requests.post(f"{API_BASE}{endpoint}", json=data)
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            return response.json()
        else:
            print(f"❌ FAILED (Status: {response.status_code})")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def run_police_tests():
    print("=== CYBERGUARD POLICE AGENT END-TO-END TESTS ===\n")

    # 1. Test Statistics
    test_endpoint("Statistics", "GET", "/statistics")

    # 2. Test Prevention Tips
    test_endpoint("Prevention Tips", "GET", "/prevention-tips")

    # 3. Test Emergency Contacts
    test_endpoint("Emergency Contacts", "GET", "/emergency-contacts")

    # 4. Test Police Chat
    chat_data = {"query": "Hello Officer, I think I've been scammed."}
    chat_res = test_endpoint("Police Chat", "POST", "/chat", chat_data)
    if chat_res:
        print(f"   Response: {chat_res.get('response', 'N/A')}")

    # 5. Test Email Analysis
    email_data = {
        "email_content": "URGENT: Your account has unusual activity and is suspended. Click here to verify account immediately or it will expire. We need to confirm identity via wire transfer.",
        "subject": "SECURITY ALERT: SUSPENDED",
        "sender": "security@bank-verify-alert.com"
    }
    analysis_res = test_endpoint("Email Analysis", "POST", "/analyze-email", email_data)
    if analysis_res:
        analysis = analysis_res.get('analysis', {})
        print(f"   Threat Level: {analysis.get('threat_level', 'N/A')}")
        print(f"   Fraud Type: {analysis.get('fraud_type', 'N/A')}")
        print(f"   Risk Score: {analysis.get('risk_score', 'N/A')}")
        print(f"   Red Flags: {len(analysis.get('red_flags', []))}")

if __name__ == "__main__":
    run_police_tests()

import requests
import json
import sys
import time

API_URL = "http://127.0.0.1:8001/api"
API_KEY = "sk_test_123456789"

def log(msg, status="INFO"):
    colors = {"INFO": "\033[94m", "SUCCESS": "\033[92m", "ERROR": "\033[91m", "RESET": "\033[0m"}
    print(f"{colors.get(status, '')}[{status}] {msg}{colors['RESET']}")

def test_honeypot(text, expected_intent=None):
    url = f"{API_URL}/honeypot"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "sessionId": "TEST-123",
        "message": {
            "sender": "scammer",
            "text": text,
            "timestamp": "2024-01-01T12:00:00Z"
        },
        "metadata": {"persona": "skeptic"}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            intent = data['ml_analysis']['intent']
            reply = data['reply']
            intel = data['extracted_intelligence']
            
            log(f"Input: '{text[:30]}...' -> Intent: {intent} | Reply: '{reply[:30]}...'", "SUCCESS")
            
            if expected_intent and intent != expected_intent:
                log(f"Expected intent {expected_intent} but got {intent}", "ERROR")
                return False
                
            # Check intelligence extraction
            if "http" in text and not intel['phishingLinks']:
                log("Failed to extract link", "ERROR")
                return False
            if "9999999999" in text and not intel['phoneNumbers']:
                log("Failed to extract phone number", "ERROR")
                return False
                
            return True
        else:
            log(f"Honeypot API Failed: {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return False

def test_check(type, value):
    url = f"{API_URL}/check"
    try:
        response = requests.post(url, json={"type": type, "value": value})
        if response.status_code == 200:
            data = response.json()
            log(f"Check {type} ({value}): Score {data.get('score')} | Risk: {data.get('risk')}", "SUCCESS")
            return True
        else:
            log(f"Check API Failed: {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"Exception: {e}", "ERROR")
        return False

def run_tests():
    log("Starting National Competition Validation Suite...", "INFO")
    time.sleep(1) # Wait for server cold start
    
    passes = 0
    total = 0
    
    # 1. Test Urgency Scam
    total += 1
    if test_honeypot("Your account is blocked. Click here immediately.", "scam_urgency"): passes += 1
    
    # 2. Test Greed Scam
    total += 1
    if test_honeypot("You have won a lottery of 5 Crores! Send bank details.", "scam_greed"): passes += 1
    
    # 3. Test Threat Scam
    total += 1
    if test_honeypot("I am calling from Police Station. FIR registered against you.", "scam_fear"): passes += 1
    
    # 4. Test Extraction
    total += 1
    if test_honeypot("Pay now at http://evil-bank.com or call 9999999999", "scam_link"): passes += 1
    
    # 5. Test Tools
    total += 1
    if test_check("link", "http://fake-bank-login.xyz"): passes += 1
    
    total += 1
    if test_check("phone", "+923001234567"): passes += 1
    
    total += 1
    if test_check("upi", "lotterywinner@oksbi"): passes += 1

    print("-" * 30)
    if passes == total:
        log(f"ALL SYSTEMS NOMINAL. {passes}/{total} TESTS PASSED.", "SUCCESS")
    else:
        log(f"SYSTEM FAILURE. ONLY {passes}/{total} TESTS PASSED.", "ERROR")

if __name__ == "__main__":
    run_tests()

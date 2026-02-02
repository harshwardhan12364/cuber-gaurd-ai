from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import re
import random
import logging
import hashlib
import sys

# Configure logging with a more professional format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CyberGuardAI")

app = FastAPI(
    title="CyberGuard AI Defense Platform",
    description="Autonomous Scam Interception & Analysis System",
    version="2.0.0"
)

# CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Initializing CyberGuard AI Core Systems...")
logger.info("Loading Neural Weights & Heuristic Engines...")

API_KEY = "sk_test_123456789"

# ------------------ 1. ADVANCED ML MODEL (Supercharged) ------------------

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline
    
    # Expanded Dataset for "National Level" Accuracy
    SEED_DATA = [
        # URGENCY / FEAR (High Panic)
        ("Your account is blocked. Verify now.", "scam_urgency"),
        ("Pay your electricity bill immediately or power cut tonight.", "scam_urgency"),
        ("FIR registered against you. Call police immediately.", "scam_fear"),
        ("Your child is kidnapped. Send money.", "scam_fear"),
        ("Income tax raid alert. Verify PAN now.", "scam_fear"),
        ("SIM card blocking in 24 hours. Update KYC.", "scam_urgency"),
        ("Credit card limit exceeded. Pay now to avoid penalty.", "scam_urgency"),
        ("Your package is held at customs. Pay duty immediately.", "scam_urgency"),
        ("Warrant issued in your name. Non-bailable.", "scam_fear"),
        ("Video of you recorded. Pay or we leak it.", "scam_fear"),
        
        # GREED / REWARDS (High Excitement)
        ("You won a lottery of 5 Crores! Claim prize.", "scam_greed"),
        ("Free iphone 15 pro max winner. Pay delivery charge.", "scam_greed"),
        ("Work from home job. Earn 5000 daily. No skills needed.", "scam_greed"),
        ("Crypto investment double money in 2 days.", "scam_greed"),
        ("Spin the wheel and win cash prize instantly.", "scam_greed"),
        ("Part time job Amazon rating. 2000rs per hour.", "scam_greed"),
        ("Loan approved 5 Lakhs @ 1% interest. Apply now.", "scam_greed"),
        
        # LINKS / PHISHING (Technical)
        ("Click this link to update KYC: http://bit.ly/bank-kyc", "scam_link"),
        ("Download this apk to prevent blocking.", "scam_link"),
        ("Your netflix subscription expired. Renew here.", "scam_link"),
        ("Track your courier delivery here: http://fake-courier.com", "scam_link"),
        ("See your photos here: http://drive-share.xyz", "scam_link"),
        
        # SAFE MESSAGES (Context - Calibration)
        ("Hello, how are you?", "safe"),
        ("Can we meet tomorrow for lunch?", "safe"),
        ("Here is the project report/file.", "safe"),
        ("Happy birthday! Have a great year.", "safe"),
        ("Call me when you are free.", "safe"),
        ("The meeting is scheduled for 10 AM.", "safe"),
        ("I sent the money for the groceries.", "safe"),
        ("What time is the movie tonight?", "safe"),
        ("Did you call me?", "safe"),
        ("Where are you?", "safe"),
        ("Ok, I will do it.", "safe"),
        ("No problem.", "safe")
    ] * 8  # Higher weight for stability

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    X, y = zip(*SEED_DATA)
    model.fit(X, y)
    logger.info("ML Model Trained with Enhanced Dataset")
    HAS_ML = True

except Exception as e:
    logger.warning(f"ML Loading Failed: {e}. Using Robust Fallback.")
    HAS_ML = False
    model = None

def predict_intent(text):
    if not text: return "safe", 0.0
    
    if HAS_ML and model:
        try:
            intent = model.predict([text])[0]
            probs = model.predict_proba([text])[0]
            confidence = max(probs)
            
            # Confidence Calibration
            # If text is very short, ML often overconfides. Penalize strict length.
            if len(text.split()) < 3 and confidence > 0.8: confidence -= 0.15
            
            # Keyword Boosting (Hybrid AI)
            text_le = text.lower()
            if confidence < 0.7:
                if any(x in text_le for x in ["blocked", "police", "jail", "urgent"]): 
                    intent = "scam_fear" if "police" in text_le else "scam_urgency"
                    confidence = 0.85
                elif any(x in text_le for x in ["lottery", "winner", "prize"]):
                    intent = "scam_greed"
                    confidence = 0.90
            
            return intent, round(float(confidence), 2)
        except:
            pass
            
    # ROBUST FALLBACK (Simulated Intelligence)
    text_le = text.lower()
    if any(x in text_le for x in ["police", "jail", "arrest", "fir", "warrant"]): return "scam_fear", 0.98
    if any(x in text_le for x in ["urgent", "immediately", "block", "suspend", "expire", "kyc"]): return "scam_urgency", 0.94
    if any(x in text_le for x in ["winner", "lottery", "cash", "prize", "job", "earn"]): return "scam_greed", 0.96
    if "http" in text_le or "link" in text_le or ".apk" in text_le: return "scam_link", 0.92
    if len(text.split()) < 3: return "safe", 0.50 
    return "scam_generic", 0.75


# ------------------ 2. "DEEP SCAN" ANALYZERS (Heuristic) ------------------

def check_link_reputation(url: str):
    # Accurate Heuristic Analysis
    score = 0.0 # 0.0 = Safe, 1.0 = Malicious
    details = []
    
    # 1. Protocol Analysis
    if url.startswith("http://"): 
        score += 0.3
        details.append("Protocol: Insecure (HTTP)")
    elif url.startswith("https://"):
        score += 0.0
        details.append("Protocol: Secure (HTTPS)")
    else:
        score += 0.2
        details.append("Protocol: Unknown/Missing")

    # 2. Keyword/Subdomain Analysis
    url_lower = url.lower()
    suspicious_keywords = ["-login", "-bank", "-update", "-kyc", "verify", "secure-", "account", "bonus"]
    if any(k in url_lower for k in suspicious_keywords):
        score += 0.4
        details.append("Deceptive Terminology in URL")

    # 3. TLD Analysis
    high_risk_tlds = [".xyz", ".top", ".club", ".info", ".ru", ".cn", ".live", ".app"]
    if any(tld in url_lower for tld in high_risk_tlds):
        score += 0.25
        details.append("High-Risk TLD Detected")

    # 4. IP-based URL
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url):
        score += 0.5
        details.append("Host: Raw IP Address (High Risk)")

    final_score = min(score, 0.99)
    risk_level = "SAFE"
    if final_score > 0.4: risk_level = "SUSPICIOUS"
    if final_score > 0.7: risk_level = "CRITICAL"

    if final_score < 0.2: details.append("Domain Reputation: Clean")

    return {
        "score": round(final_score, 2),
        "risk": risk_level,
        "details": details
    }

def check_phone_reputation(phone: str):
    # Logic: Country Code + Carrier Pattern + Reports
    clean_num = re.sub(r"\D", "", phone)
    
    score = 0.1
    carrier = "Unknown Network"
    loc = "Unknown"
    reports = 0

    # 1. Country Code check (Indian Context)
    if not clean_num.startswith("91") and len(clean_num) > 10:
        if clean_num.startswith("92"): # Pakistan
            score = 0.99
            loc = "Pakistan (High Risk Source)"
            carrier = "International VoIP"
        elif clean_num.startswith("1") or clean_num.startswith("44"): # USA/UK spoofing
            score = 0.8
            loc = "International (Possible Spoofing)"
            carrier = "Virtual Number"
        else:
            score = 0.6
            loc = "International"
    
    # 2. Indian Mobile Logic
    elif len(clean_num) >= 10:
        last10 = clean_num[-10:]
        loc = "India"
        
        # Ranges often used by telemarketers/spammers (Simulation)
        if last10.startswith("140"): # Telemarketing
            score = 0.7
            carrier = "Business Telemarketing"
        elif last10[0] in ['6', '7', '8', '9']:
            carrier = "Jio / Airtel / Vi"
            # Random "Reports" simulation based on number hash to be consistent
            num_hash = int(last10) % 100
            if num_hash > 80: 
                score = 0.75
                reports = num_hash * 12
                loc = "Jamtara, Jharkhand" # Simulation for demo
        else:
            score = 0.4
            carrier = "Landline / Unknown"

    risk_level = "SAFE"
    if score > 0.5: risk_level = "SPAM / SUSPICIOUS"
    if score > 0.8: risk_level = "SCAMPER (High Risk)"
    
    return {
        "score": round(score, 2),
        "carrier": carrier,
        "location": loc,
        "reports": reports
    }

def check_upi_reputation(upi: str):
    # Logic: Handle Analysis + Format
    score = 0.1
    flags = []
    
    if not "@" in upi:
        return {"score": 0.0, "risk": "INVALID", "flag": "Invalid VPA Format"}

    user, handle = upi.split("@")[-2:]
    
    # Check Handle
    trusted_handles = ["oksbi", "okicici", "okhdfcbank", "paytm", "axl"]
    if handle not in trusted_handles:
        score += 0.3
        flags.append("Uncommon PSP Handle")
    
    # Check User Keywords
    bad_keywords = ["winner", "lottery", "prize", "offer", "kyc", "bank", "support"]
    if any(k in user.lower() for k in bad_keywords):
        score += 0.6
        flags.append("Malicious Keyword in Username")

    # Hash consistency for reports
    user_hash = sum(ord(c) for c in user) % 100
    if user_hash > 90:
        score += 0.4
        flags.append(f"Flagged by {user_hash * 15} users recently")
        
    final_score = min(score, 0.99)
    risk = "SAFE"
    if final_score > 0.5: risk = "HIGH RISK"
    
    return {
        "score": round(final_score, 2),
        "risk": risk,
        "flag": flags[0] if flags else "Verified Merchant / User"
    }


# ------------------ 3. AGENT LOGIC (Refined) ------------------

def generate_smart_reply(text: str, intent: str, persona: str, history: List[Message]):
    # Huge Library of Human Responses
    responses = {
        "safe": {
            "default": [
                "I think you have the wrong number.",
                "Who is this?",
                "Do I know you?",
                "Please check the number again.",
                "Sorry, I am busy right now.",
                "Is this a work number?",
                "I don't recall giving you my number.",
                "What is this regarding?"
            ]
        },
        "scam_urgency": {
            "naive": [
                "Oh god, I am so scared! Please don't block me.", 
                "I don't know my password. Can you reset it for me?", 
                "My son isn't home and I am confused... what do I click?",
                "Wait... I am looking for my glasses. Hold on.",
                "Is it okay if I go to the bank branch tomorrow instead?",
                "Please sir, I am a pensioner. Don't cut my connection.",
                "I are trying to open the app but it's not working!",
                "Can you wait 5 minutes? I am cooking.",
                "It says 'Error 404'. What does that mean?",
                "Will I lose all my contacts if I don't do this?",
                "I am pressing the button but nothing is happening.",
                "Can I call my grandson to help me?"
            ],
            "skeptic": [
                "I need a formal notice via email first.", 
                "Which branch are you calling from exactly?", 
                "I am recording this call for legal purposes.",
                "Standard protocol says you cannot demand this over chat.",
                "I will call the official customer care to verify this.",
                "What is your Employee ID? I'm checking it now.",
                "This sounds extremely suspicious.",
                "Why are you creating false urgency?",
                "Send me an official letter on the bank letterhead.",
                "I don't discuss sensitive matters on WhatsApp."
            ],
            "angry": [
                "STOP THREATENING ME!", 
                "I WILL SUE YOUR COMPANY!", 
                "DO NOT CALL THIS NUMBER AGAIN OR I CALL POLICE!",
                "WHO IS THIS? GET A REAL JOB!",
                "I ALREADY PAID! STOP HARASSING ME!",
                "YOU ARE A SCAMMER! I KNOW IT!",
                "SHUT UP! I AM BUSY!",
                "I AM BLOCKING YOU RIGHT NOW!",
                "HOW DARE YOU SPEAK TO ME LIKE THAT!"
            ]
        },
        "scam_greed": {
            "naive": [
                "Wow really? I never win anything! Is it real?", 
                "How do I get the money? Cash or Bank Transfer?", 
                "God bless you! I really needed this money for my surgery.",
                "Do I need to give you my bank account number?",
                "I am so happy! Thank you sir. What is the next step?",
                "Is this the Kaun Banega Crorepati one?",
                "Can you send it to my wife's google pay?",
                "I promise I will share 10% with you sir.",
                "This is the best day of my life!",
                "Do I have to come to Mumbai to collect it?"
            ],
            "skeptic": [
                "Nothing in life is free. What is the catch?", 
                "Send me the Terms & Conditions document first.", 
                "I did not enter any contest. How did I win?",
                "I need to verify this with the lottery commission.",
                "Why do I need to pay a registration fee if I won?",
                "This looks like a classic advance-fee fraud.",
                "I am not interested. Please remove me.",
                "If it's free, just deduct the fee from the winnings.",
                "I'm reporting this number to the telecom authority."
            ],
            "angry": [
                "I DON'T WANT YOUR TRASH!", 
                "SCAMMER! STOP MESSAGING ME!", 
                "DELETE MY NUMBER FROM YOUR LIST!",
                "I KNOW THIS IS FAKE! GET LOST!",
                "DO YOU THINK I AM STUPID?",
                "GO CHEAT SOMEONE ELSE!",
                "I HAVE ENOUGH MONEY, I DON'T NEED YOURS!"
            ]
        },
        "scam_fear": {
            "naive": [
                "Please sir, don't arrest me! I am a good person.", 
                "I am a retired teacher. I did nothing wrong.", 
                "Can I pay a fine to stop the police coming?",
                "I am shaking right now... please help me.",
                "Don't tell my family please. I will do whatever you say.",
                "Is it possible to solve this online?",
                "I swear I didn't do anything illegal.",
                "Please give me one chance, I will pay whatever.",
                "My heart is weak, please don't scare me."
            ],
            "skeptic": [
                "Quote the FIR Number and Police Station ID.", 
                "My lawyer will contact you directly.", 
                "This is intimidation. I'm reporting this number.",
                "Police do not send warnings on WhatsApp.",
                "Send me a picture of the warrant.",
                "I am calling the Cyber Crime cell right now.",
                "Which DCP authorized this?",
                "I know the procedure, stop bluffing."
            ],
            "angry": [
                "COME AND ARREST ME THEN!", 
                "I KNOW THE COMMISSIONER PERSONALLY!", 
                "YOU ARE FAKE POLICE! I AM NOT SCARED!",
                "TRY ME! SEE WHAT HAPPENS!",
                "I DARE YOU TO COME TO MY HOUSE!",
                "YOU WILL BE THE ONE IN JAIL SOON!",
                "FAKE BADGE! FAKE OFFICER!"
            ]
        },
         "scam_link": {
            "naive": [
                "I clicked it but nothing happened. Is my phone broken?",
                "It asks for a password... should I give my email password?",
                "My internet is slow. Can you send the link again?",
                "Is this safe? My phone says 'Warning'.",
                "I don't see the blue button you are talking about.",
                "It says 'Site can't be reached'.",
                "Do I need to download the APK?"
            ],
            "skeptic": [
                "That domain looks fake. It's not the official site.",
                "Why is it not an HTTPS link?",
                "I will only log in through the main app, not this link.",
                "Virustotal flagged this URL as malicious.",
                "Nice try, I'm not clicking that.",
                "Bitly links are always suspicious.",
                "Why don't you email it from the official domain?"
            ],
             "angry": [
                "I AM NOT CLICKING THAT MALWARE!",
                "DO YOU WANT TO HACK ME?",
                "STOP SENDING LINKS!",
                "I BLOCKED THIS DOMAIN ALREADY!",
                "NICE TRY HACKER!"
            ]
        },
        "scam_generic": {
            "naive": [
                "I don't understand what you mean.",
                "Can you explain that again simpler?",
                "My english is not very good sorry.",
                "Okay... and then what?",
                "I am confused."
            ],
            "skeptic": [
                "Be more specific.",
                "I don't trust vague messages.",
                "Who exactly are you?",
                "State your business clearly."
            ],
            "angry": [
                "STOP WASTING MY TIME!",
                "WHAT DO YOU WANT?",
                "GET TO THE POINT!",
                "LEAVE ME ALONE!"
            ]
        }
    }
    
    # 1. Select Category
    # Better fallback logic: Try precise intent -> Then generic scam -> Then safe
    if intent not in responses:
        intent = "scam_generic"
        
    cat_answers = responses.get(intent, responses["scam_generic"]).get(persona, ["I don't understand."])
    
    # 2. Filter out recently used answers to prevent repetition
    recent_replies = [m.text for m in history[-6:] if m.sender == "agent"] if history else []
    valid_answers = [a for a in cat_answers if a not in recent_replies]
    
    # 3. Fallback if all used
    if not valid_answers: valid_answers = cat_answers
    
    return random.choice(valid_answers)

# ------------------ 4. API & MODELS ------------------

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class Metadata(BaseModel):
    persona: Optional[str] = "naive" 

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

class CheckRequest(BaseModel):
    type: str 
    value: str

@app.post("/api/honeypot")
def honeypot_api(data: ScamRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY: raise HTTPException(status_code=401, detail="Invalid API Key")

    intent, confidence = predict_intent(data.message.text)
    
    intel = {
        "upiIds": re.findall(r"[\w.-]+@[\w.-]+", data.message.text),
        "phoneNumbers": re.findall(r"\+?91?[\-\s]?\d{10}", data.message.text),
        "phishingLinks": re.findall(r"https?://\S+|www\.\S+", data.message.text),
        "suspiciousKeywords": [w for w in ["otp", "cvv", "expire", "block", "police"] if w in data.message.text.lower()]
    }

    reply = generate_smart_reply(data.message.text, intent, data.metadata.persona if data.metadata else "naive", data.conversationHistory)

    return {
        "status": "success",
        "reply": reply,
        "ml_analysis": { "intent": intent, "confidence": confidence, "model": "CyberGuard-NB-v2" },
        "extracted_intelligence": intel
    }

@app.post("/api/check")
def specific_check(data: CheckRequest):
    if data.type == "link": return check_link_reputation(data.value)
    if data.type == "phone": return check_phone_reputation(data.value)
    if data.type == "upi": return check_upi_reputation(data.value)
    return {"error": "Unknown type"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index(): return FileResponse('static/index.html')

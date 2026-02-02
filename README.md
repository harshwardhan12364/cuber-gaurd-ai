# CyberGuard A.I. - Autonomous Scam Defense System

![CyberGuard Project Banner](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AI Model](https://img.shields.io/badge/AI-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%2B%20Tailwind-blue?style=for-the-badge&logo=tailwindcss&logoColor=white)

> **Winner/Finalist Project for National Innovation Competition**  
> *An intelligent defense system that safeguards users against digital fraud using real-time ML analysis and autonomous conversational agents.*

---

## 🚀 Overview

**CyberGuard A.I.** is a next-generation security platform designed to intercept, analyze, and neutralize social engineering attacks before they cause harm. It acts as a "digital bodyguard" for messaging apps.

### Key Features
*   **🧠 Real-Time Intent Detection**: Uses a trained Naive Bayes classifier to instantly categorize messages as *Urgency Scams*, *Greed/Lottery Fraud*, *Threats*, or *Safe*.
*   **🤖 Autonomous Interceptor**: An AI agent that engages with scammers automatically, wasting their time while extracting intelligence (phone numbers, UPI IDs, links).
*   **🔍 Deep Forensic Scanning**:
    *   **URL Analyzer**: Checks HTTP/HTTPS status, suspicious TLDs, and phishing patterns.
    *   **Phone Tracer**: Identifies carrier, region (HLR simulation), and risk level.
    *   **Financial Fraud Check**: Validates UPI handles against known scam patterns.
*   **🎨 Premium Cyber-Interface**: A futuristic, glassmorphism-based dashboard for real-time monitoring.

---

## 🛠️ Tech Stack

*   **Backend**: Python (FastAPI, Uvicorn)
*   **Machine Learning**: Scikit-Learn (TF-IDF Vectorization + Multinomial Naive Bayes)
*   **Frontend**: Native HTML5, JavaScript (ES6+), **Tailwind CSS** (via CDN)
*   **Security API**: Custom REST API Architecture

---

## ⚡ Deployment Instructions

### Prerequisites
*   Python 3.9+
*   Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/project-techno-blade.git
cd project-techno-blade
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch the Neural Core
```bash
python -m uvicorn main:app --reload
```
*The server will start at `http://127.0.0.1:8000`*

### Step 4: Access Dashboard
Open your browser and navigate to:
**`http://127.0.0.1:8000`**

---

## 📂 Project Structure
```
project-techno-blade/
├── main.py              # CORE ENGINE: API, ML Pipeline, & Logic
├── static/
│   └── index.html       # FRONTEND: The Cyber-Interface
├── requirements.txt     # Dependencies
├── .gitignore           # Git Configuration
└── README.md            # Documentation
```

---

## 🛡️ License
This project is developed for educational and competition purposes.

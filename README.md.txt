<div align="center">

# MOBILE & API HONEYPOT THREAT MONITOR

**Multi-Protocol Deception Engine, Encrypted Telemetry & Automated Threat Analytics**

![Python](https://img.shields.io/badge/Python-3.9%2B-ffffff?style=for-the-badge&logo=python&logoColor=111111)
![Flask](https://img.shields.io/badge/Flask-REST_API-ffffff?style=for-the-badge&logo=flask&logoColor=111111)
![Cryptography](https://img.shields.io/badge/Encryption-Fernet_AES-ffffff?style=for-the-badge&logo=letsencrypt&logoColor=111111)
![Android](https://img.shields.io/badge/Android-Chaquopy-ffffff?style=for-the-badge&logo=android&logoColor=111111)

</div>

---

A Python-based deception and threat-monitoring system with an Android client wrapper (via Chaquopy) designed to detect, log, and analyze unauthorized reconnaissance and exploitation attempts against exposed mobile backend APIs and TCP services.

<div align="center">
  <img src="assets/honeypot_dashboard.png" alt="Honeypot Analytics Dashboard" width="85%">
</div>

---

## Core Architecture & Features

* **Multi-Protocol Deception (`honepot_ccore.py`)**
  * **HTTP/REST API Decoys (Port 5000):** Simulates high-value mobile backend endpoints (`/api/v1/admin/login`, `/api/v1/users/data`, `/api/v1/config`) returning realistic decoy responses while capturing attacker IPs, HTTP methods, headers, and payloads.
  * **Raw TCP Socket Listener (Port 8080):** Emulates an exposed Apache server (`Apache/2.4.41`) to log raw banner-grabbing and port-scanning payloads.
* **Tamper-Resistant Encrypted Logging (`generate_key.py`, `show_logs.py`)**
  * Encrypts every captured interaction at rest using symmetric **Fernet (AES-128-CBC + HMAC)** encryption before writing to `honeypot.log`.
* **Automated Attack Simulation Suite (`pentest.py`)**
  * Built-in validation script that tests honeypot detection across six attack vectors: credential brute-forcing, SQL injection, directory traversal, IDOR enumeration, sensitive configuration exposure, and debug-mode probing.
* **Real-Time Threshold Alerting (`alert.py`)**
  * Background monitoring daemon that decrypts incoming logs, detects interaction spikes (5+ events within a 5-minute window), and dispatches JSON webhook alerts with cooldown rate-limiting.
* **Attack Pattern Analytics (`log_analyzer.py`, `dashboard.py`)**
  * Aggregates decrypted telemetry to identify top attacking IPs, targeted endpoints, and interaction frequency timelines, exporting visual reports via Matplotlib.
* **Android Integration (`android_client/`)**
  * Embeds the Python honeypot engine inside an Android application using **Chaquopy** to turn mobile devices into portable deception sensors.

---

## Repository Structure

```text
honeypot-threat-monitor/
├── backend/
│   ├── honepot_ccore.py       # Flask API decoys & raw TCP socket honeypot
│   ├── generate_key.py        # Fernet symmetric encryption key generator
│   ├── log_analyzer.py        # Log decryption & attack-pattern aggregation
│   ├── show_logs.py           # CLI viewer for formatted decrypted logs
│   ├── dashboard.py           # Matplotlib visual analytics generator
│   ├── alert.py               # Threshold-based webhook alerting daemon
│   ├── pentest.py             # Automated vulnerability & payload simulator
│   └── setup_environment.py   # Virtual environment & dependency installer
├── android_client/            # Android Studio & Chaquopy integration files
├── assets/
│   └── honeypot_dashboard.png # Sample analytics output
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
# 1. Clone repository & install dependencies
git clone [https://github.com/](https://github.com/)<your-username>/honeypot-threat-monitor.git
cd honeypot-threat-monitor
python -m venv venv
venv\Scripts\activate          # Windows (use `source venv/bin/activate` on Linux/macOS)
pip install -r requirements.txt

# 2. Generate Fernet encryption key (required before launch)
cd backend
python generate_key.py

# 3. Start HTTP (5000) & TCP (8080) honeypot listeners
python honepot_ccore.py

# 4. Run automated attack simulation (in a separate terminal)
python pentest.py

# 5. Decrypt logs & generate visual analytics dashboard
python show_logs.py
python dashboard.py
```

---

## Operational Security Notice

> **Warning:** Never commit `fernet.key` or raw `honeypot.log` files containing live network data to public version control. Deploy this system strictly within isolated lab environments or authorized networks.
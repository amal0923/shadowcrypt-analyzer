# 🔐 ShadowCrypt Analyzer

<p align="center">
   <img src="logo.png" width="700">
</p>

<p align="center">
  <b>Advanced Password Intelligence Tool</b><br>
  Analyze • Detect • Secure
</p>

---

## 🚀 Overview

**ShadowCrypt Analyzer** is a powerful password analysis tool built with Python.  
It evaluates password strength using entropy calculations, detects weak patterns, estimates crack time, and checks real-world data breaches using the Have I Been Pwned API.

Designed with a **hacker-style terminal UI**, this tool delivers both functionality and visual experience.

---

## ✨ Features

- 🔍 **Password Strength Analysis** (Weak / Medium / Strong)
- 📊 **Entropy Calculation**
- ⏳ **Crack Time Estimation**
- 🧠 **Common Pattern Detection**
- 🌐 **Breach Detection (HIBP API)**
- 🎨 **Terminal-style GUI (Tkinter)**
- ⚡ **Auto-scrolling Output**
- ⌨️ **Keyboard Shortcuts (Ctrl + A / C / V)**
- 📈 **Live Strength Progress Bar**
- 💡 **Security Suggestions Engine**

---


## 🛠️ Tech Stack

- **Language:** Python 3
- **GUI Framework:** Tkinter
- **API:** Have I Been Pwned (k-Anonymity Model)
- **Libraries:**
  - requests
  - hashlib
  - re
  - math

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/shadowcrypt-analyzer.git
cd shadowcrypt-analyzer
pip install -r requirements.txt


```bash
python shadowcrypt.py

[+] Analyzing Password...
[+] Strength: Strong
[+] Entropy: 192.72
[+] Crack Time: 10 billion years
[+] Not found in breaches

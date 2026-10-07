<div align="center">

# ⚡ Onyx Gate — Python Integration Example

[![Language](https://img.shields.io/badge/Language-Python%203.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Requests](https://img.shields.io/badge/HTTP-Requests-2B5B84?style=for-the-badge)](https://pypi.org/project/requests/)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-blue?style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

**A lightweight, cross-platform Python SDK and CLI loader for [Onyx Gate](https://auth.script-kittens.com).**

</div>

---

## 🚀 Overview

This repository provides a clean Python integration demonstrating how to protect CLI tools, automation scripts, and bots with Onyx Gate license verification and HWID locking.

### ✨ Features
- ⚡ **Minimal Footprint** — Only requires the standard `requests` package.
- 🛡️ **Cross-Platform HWID** — Automatically generates machine identifiers on Windows, Linux, and macOS.
- 🔑 **Session Management** — Supports login, registration, key redemption, and tier validation.
- 🎨 **Ready CLI Loader** — Interactive console loader example with formatted outputs.

---

## 📂 Project Structure

```text
├── skauth.py            # Drop-in Python SDK module
├── loader.py            # CLI loader & interactive prompt example
├── requirements.txt     # Python dependencies (requests)
└── README.md            # Documentation
```

---

## ⚡ Quick Start

### 1. Requirements
- Python 3.8 or newer
- `pip` package manager

### 2. Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fegrial/Onyx-Gate-Python-Example.git
   cd Onyx-Gate-Python-Example
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Open `loader.py` and set your `APP_ID`:
   ```python
   APP_ID = "YOUR_APP_ID_HERE"
   ```
4. Run the loader:
   ```bash
   python loader.py
   ```

---

## 💻 Code Integration

Add Onyx Gate protection to your script in seconds:

```python
from skauth import SKAuth

# 1. Initialize client
auth = SKAuth(app_id="YOUR_APP_ID", version="1.0")

# 2. Authenticate
res = auth.login(username="user123", password="password123")

if res.get("ok"):
    user_data = res.get("data", {})
    print(f"[+] Login successful! Welcome, {user_data.get('username')}")
    print(f"[+] Subscription plan: {user_data.get('plan')}")

    # 3. Check subscription gate
    if auth.is_paid():
        print("[+] Premium features unlocked!")
        # Run protected logic here
    else:
        print("[*] Running standard tier...")
else:
    print(f"[-] Authentication failed: {res.get('message')}")
```

### Key Redemption
```python
res = auth.redeem_key("ONYX-XXXX-XXXX-XXXX")
if res.get("ok"):
    print("[+] Key redeemed successfully!")
```

---

## 🛡️ API Reference

| Method | Description |
| :--- | :--- |
| `SKAuth(app_id, version)` | Initializes the auth client instance. |
| `auth.login(user, password)` | Authenticates user and verifies machine HWID. |
| `auth.register(user, pass, email, key)` | Registers a new account. |
| `auth.redeem_key(key)` | Activates or upgrades plan via license key. |
| `auth.is_paid()` | Returns `True` if active session is on a paid plan. |
| `auth.get_hwid()` | Calculates hardware identifier string. |

---

<div align="center">
<sub>Powered by <b>Onyx Gate</b> • Maintained by <a href="https://github.com/fegrial">fegrial</a></sub>
</div>

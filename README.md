<div align="center">

# Onyx Gate — Python SDK Example

**A lightweight Python SDK and CLI loader for [Onyx Gate](https://auth.script-kittens.com).**

</div>

---

## Files

| File | What it is |
| :--- | :--- |
| `skauth.py` | Drop-in SDK module — copy it into your project |
| `loader.py` | Working CLI loader example (login / register menu) |
| `requirements.txt` | `requests` |

## Quick start

```bash
git clone https://github.com/ScriptKittenss/Onyx-Gate-Python-Example.git
cd Onyx-Gate-Python-Example
pip install -r requirements.txt
```

Open `loader.py`, set your `APP_ID` (from the Onyx Gate dashboard), then:

```bash
python loader.py
```

## Use it in your own script

```python
from skauth import SKAuth

auth = SKAuth(app_id="YOUR_APP_ID", version="1.0")

res = auth.login("username", "password")
if not res.get("ok"):
    print(f"Login failed: {res.get('message')}")
    exit(1)

print(f"Welcome {auth.get_username()}! Plan: {auth.get_plan()}")

if auth.is_paid():
    print("Premium features unlocked.")
```

## API reference

| Method | Description |
| :--- | :--- |
| `SKAuth(app_id, version="1.0")` | Create the client. Computes the machine HWID. |
| `login(username, password)` | Authenticate. On success `auth.user` holds `username`, `plan`, `expires`, `email`, `apiKey`. On failure show `res["message"]` as-is. |
| `register(username, password, email="", license_key="")` | Create an account. `license_key` is optional. |
| `redeem(username, license_key)` | Apply a license key to an existing account. |
| `validate()` | Heartbeat — call every few minutes. Kicks banned/expired users, syncs plan changes. Needs a login first. |
| `get_var(name)` | Read a runtime variable (dashboard → Settings → Variables). Returns the value or `None`. |
| `download_file(file_id, save_path)` | Download a file from the Runtime Vault (dashboard → Files). Returns `True` on success. Needs a login first. |
| `is_paid()` | `True` when the plan isn't `free` (starter, pro, …). |
| `get_hwid()` | The machine HWID (SHA256, 32 hex chars). Same machine gives the same HWID in the C# and C++ SDKs. |
| `get_username()` / `get_plan()` / `get_expires()` | Shortcuts into `auth.user`. |

## Notes

- The App ID is public. Never put your app secret, a password, or a license key in source code.
- `version` must match the version set in your dashboard, or login returns "Update required".
- Logins are rate limited (15/min per IP), registrations 5 per 5 minutes per IP.
- Full endpoint docs: https://auth.script-kittens.com → Documentation.

---

<div align="center">
<sub>Powered by <b>Onyx Gate</b> • <a href="https://github.com/ScriptKittenss">ScriptKittenss</a></sub>
</div>

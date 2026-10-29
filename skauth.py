# ============================================================
#  Onyx Gate SDK  —  skauth.py
#  Drop-in Python SDK for https://auth.script-kittens.com
#  Requires: Python 3.8+,  pip install requests
# ============================================================

import hashlib
import os
import subprocess
import uuid

import requests


class SKAuth:
    BASE = "https://auth.script-kittens.com"

    def __init__(self, app_id, version="1.0"):
        self.app_id = app_id
        self.version = version
        self.user = None          # filled by login(): username, plan, expires, email, apiKey
        self.hwid = self.get_hwid()

    # ── HWID — disk serial hashed with SHA256 (first 32 hex chars) ──
    # Matches the C# and C++ SDKs: same machine => same HWID on all SDKs.
    def get_hwid(self):
        raw = ""
        try:
            if os.name == "nt":
                out = subprocess.check_output(
                    ["powershell", "-NoProfile", "-Command",
                     "(Get-CimInstance Win32_DiskDrive | Select-Object -First 1).SerialNumber"],
                    stderr=subprocess.DEVNULL, timeout=15,
                ).decode().strip()
                raw = out
        except Exception:
            pass
        if not raw:
            raw = str(uuid.getnode())  # MAC address fallback (any platform)
        return hashlib.sha256(raw.strip().encode()).hexdigest()[:32]

    # ── internal POST helper ──
    def _post(self, endpoint, payload):
        try:
            r = requests.post(f"{self.BASE}{endpoint}", json=payload, timeout=15)
            return r.json()
        except Exception as e:
            return {"ok": False, "message": f"Connection error: {e}"}

    # ── Login ───────────────────────────────────────────────
    # Returns the server response. On success, self.user is populated.
    # Show the server's message on failure (HWID mismatch, banned,
    # expired, update required, offline...) — display it, don't invent one.
    def login(self, username, password):
        d = self._post("/sdk/login", {
            "appId": self.app_id,
            "username": username,
            "password": password,
            "hwid": self.hwid,
            "version": self.version,
        })
        if d.get("ok"):
            self.user = d.get("user") or {}
        return d

    # ── Register a new account (license key optional) ───────
    def register(self, username, password, email="", license_key=""):
        return self._post("/sdk/register", {
            "appId": self.app_id,
            "username": username,
            "password": password,
            "email": email,
            "licenseKey": license_key,
        })

    # ── Redeem a license key on an existing account ─────────
    def redeem(self, username, license_key):
        return self._post("/sdk/redeem", {
            "appId": self.app_id,
            "username": username,
            "licenseKey": license_key,
        })

    # ── Validate — heartbeat ────────────────────────────────
    # Call every few minutes while your tool runs. Kicks banned /
    # expired users and syncs plan changes without re-login.
    # Uses the apiKey returned by login(); needs a successful login first.
    def validate(self):
        api_key = (self.user or {}).get("apiKey", "")
        if not api_key:
            return {"ok": False, "message": "Not logged in — call login() first."}
        r = self._post("/sdk/validate", {
            "appId": self.app_id,
            "apiKey": api_key,
            "hwid": self.hwid,
        })
        if r.get("ok") and self.user is not None:
            self.user["plan"] = r.get("plan", self.user.get("plan"))
            self.user["expires"] = r.get("expires", self.user.get("expires"))
        return r

    # ── Get a server-side runtime variable ──────────────────
    # Set in dashboard → Settings → Variables. Updates without
    # recompiling your tool (version checks, announcements, URLs...).
    def get_var(self, name):
        d = self._post("/sdk/variable", {"appId": self.app_id, "name": name})
        return d.get("value")

    # ── Download a file from the Runtime Vault ──────────────
    # file_id comes from dashboard → Files. Needs a logged-in user
    # (uses the apiKey from login). Returns True on success.
    def download_file(self, file_id, save_path):
        api_key = (self.user or {}).get("apiKey", "")
        if not api_key:
            return False
        try:
            r = requests.get(
                f"{self.BASE}/sdk/file",
                params={"appId": self.app_id, "fileId": file_id, "apiKey": api_key},
                timeout=30,
            )
            if r.status_code != 200 or not r.content:
                return False
            with open(save_path, "wb") as f:
                f.write(r.content)
            return True
        except Exception:
            return False

    # ── Helpers ─────────────────────────────────────────────
    def is_paid(self):
        # Any plan that isn't free counts as paid (starter, pro, ...).
        plan = (self.user or {}).get("plan", "free") or "free"
        return plan.lower() != "free"

    def get_username(self):
        return (self.user or {}).get("username", "")

    def get_plan(self):
        return (self.user or {}).get("plan", "free")

    def get_expires(self):
        return (self.user or {}).get("expires")

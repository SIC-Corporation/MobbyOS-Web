from browser import window
import hashlib
import base64
import os
import time

class SICryption:
    def __init__(self):
        self.sessions = {}
        self.secret = "SIC_CORE_SECRET_2026"

    # =========================
    # Cryptography
    # =========================
    def sha512(self, data):
        return hashlib.sha512(data.encode()).hexdigest()

    def encrypt(self, data):
        payload = f"{data}|{self.secret}"
        return base64.b64encode(payload.encode()).decode()

    def decrypt(self, token):
        try:
            raw = base64.b64decode(token).decode()
            data, secret = raw.rsplit("|", 1)
            if secret != self.secret:
                return None
            return data
        except:
            return None

    # =========================
    # Sessions
    # =========================
    def create_session(self, user):
        token = self.sha512(user + str(time.time()))
        self.sessions[user] = token
        return token

    def validate_session(self, user, token):
        return self.sessions.get(user) == token

    # =========================
    # WatcherDog PY
    # =========================
    def watchdog(self, msg):
        mode = window.localStorage.getItem("mobby_mode") or "adult"
        banned = ["<script", "eval(", "password", "root"]

        if mode == "kid":
            for b in banned:
                if b in msg.lower():
                    return None
        return msg

sicryption = SICryption()
window.sicryption = sicryption

from browser import window
import hashlib
import base64

class SICryption:
    def __init__(self):
        self.allowed_hash_alg = "sha512"
        self.active_sessions = {}

    # =========================
    # Encrypt / Decrypt Messages
    # =========================
    def hash_message(self, msg):
        return hashlib.sha512(msg.encode("utf-8")).hexdigest()

    def encode_base64(self, msg):
        return base64.b64encode(msg.encode("utf-8")).decode("utf-8")

    def decode_base64(self, msg):
        return base64.b64decode(msg.encode("utf-8")).decode("utf-8")

    # =========================
    # Session Validation
    # =========================
    def create_session(self, user_id):
        token = self.hash_message(user_id + "SECURE" + str(window.Date().now()))
        self.active_sessions[user_id] = token
        return token

    def validate_session(self, user_id, token):
        return self.active_sessions.get(user_id) == token

    # =========================
    # WatcherDog Integration
    # =========================
    def watcherDog(self, msg):
        mode = window.localStorage.getItem("mobby_mode") or "adult"
        blocked_words = ["hack", "kill", "password", "root", "<script>"]
        if mode == "kid":
            for word in blocked_words:
                if word in msg.lower():
                    return "WatcherDog Alert: Unsafe content blocked for Kid Mode."
        return msg

sicryption = SICryption()
window.sicryption = sicryption

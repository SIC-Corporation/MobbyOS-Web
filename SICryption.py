import base64
import hashlib
from datetime import datetime

class SICryption:
    """
    SIC Corp High-Advanced Encryption Module (V2.0)
    Creator: Roy (Owner of SIC Corp)
    """
    def __init__(self, master_key="Roy_SIC_Corp_2026"):
        self.key = hashlib.sha256(master_key.encode()).hexdigest()
        self.header = "SIC|SECURED|V2|"

    def _generate_dynamic_salt(self):
        return hashlib.md5(str(datetime.now().microsecond).encode()).hexdigest()[:8]

    def encrypt(self, data):
        if not data: return ""
        salt = self._generate_dynamic_salt()
        full_key = self.key + salt
        encrypted_chars = []
        for i in range(len(data)):
            key_c = full_key[i % len(full_key)]
            enc_c = chr((ord(data[i]) + ord(key_c)) % 1114112)
            encrypted_chars.append(enc_c)
        raw_combined = salt + "".join(encrypted_chars)
        encoded = base64.b64encode(raw_combined.encode()).decode()
        return f"{self.header}{encoded}"

    def decrypt(self, encrypted_data):
        if not encrypted_data or not encrypted_data.startswith(self.header):
            return encrypted_data
        try:
            clean_data = encrypted_data.replace(self.header, "")
            decoded_raw = base64.b64decode(clean_data).decode()
            salt = decoded_raw[:8]
            actual_content = decoded_raw[8:]
            full_key = self.key + salt
            decrypted_chars = []
            for i in range(len(actual_content)):
                key_c = full_key[i % len(full_key)]
                dec_c = chr((ord(actual_content[i]) - ord(key_c)) % 1114112)
                decrypted_chars.append(dec_c)
            return "".join(decrypted_chars)
        except:
            return "DECRYPTION_FAILED"

# --- ACCESS LEVEL LOGIC ---
# This is called by engine.py to check roles

def identify_access(email):
    """
    Validates user email and returns access tier.
    Used by MobbyOS to determine UI and Permissions.
    """
    admins = ["SICMailCenter1@gmail.com", "Roystonslijkerman@gmail.com"]
    email = email.lower().strip()

    if email in admins:
        return {
            "role": "ADMIN (SIC CORP)",
            "color": "#38bdf8", # Sky Blue
            "clearance": 3
        }
    
    elif "@kids.com" in email or "child" in email:
        return {
            "role": "KIDS MODE",
            "color": "#fbbf24", # Amber/Yellow
            "clearance": 1
        }
    
    else:
        return {
            "role": "ADULT NODE",
            "color": "#a855f7", # Purple
            "clearance": 2
        }

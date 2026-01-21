import base64
import hashlib
import json
from datetime import datetime

class SICryption:
    """
    SIC Corp Ultra-Advanced Encryption Module (V3.0)
    Proprietary Technology of Roy, SIC Corp.
    """
    def __init__(self, master_key="Roy_SIC_Corp_2026"):
        # Layer 1: SHA-256
        h1 = hashlib.sha256(master_key.encode()).hexdigest()
        # Layer 2: Recursive Hashing for complexity
        self.key = hashlib.sha3_512(h1.encode()).hexdigest()
        self.header = "SIC|VAULT|V3|"

    def _generate_dynamic_salt(self):
        # Generates a unique salt based on precise nanoseconds
        return hashlib.blake2b(str(datetime.now().timestamp()).encode()).hexdigest()[:12]

    def encrypt(self, data):
        if not data: return ""
        salt = self._generate_dynamic_salt()
        # Combine key and salt for the encryption stream
        working_key = hashlib.sha256((self.key + salt).encode()).hexdigest()
        
        encrypted_chars = []
        for i, char in enumerate(str(data)):
            key_c = working_key[i % len(working_key)]
            # Advanced Caesar-XOR Hybrid logic
            shift = (ord(char) + ord(key_c)) % 1114112
            encrypted_chars.append(chr(shift))
            
        raw_combined = salt + "".join(encrypted_chars)
        encoded = base64.urlsafe_b64encode(raw_combined.encode()).decode()
        return f"{self.header}{encoded}"

    def decrypt(self, encrypted_data):
        if not encrypted_data or not encrypted_data.startswith(self.header):
            return encrypted_data
        try:
            clean_data = encrypted_data.replace(self.header, "")
            decoded_raw = base64.urlsafe_b64decode(clean_data).decode()
            salt = decoded_raw[:12]
            actual_content = decoded_raw[12:]
            
            working_key = hashlib.sha256((self.key + salt).encode()).hexdigest()
            decrypted_chars = []
            for i, char in enumerate(actual_content):
                key_c = working_key[i % len(working_key)]
                shift = (ord(char) - ord(key_c)) % 1114112
                decrypted_chars.append(chr(shift))
            return "".join(decrypted_chars)
        except Exception:
            return "ERR_SIG_MISMATCH"

# --- GLOBAL ACCESS HANDLER ---

def identify_access(email):
    """
    The Gatekeeper. Connects MobbyOS to the SICryption Clearance Levels.
    """
    # Initialize the Vault
    vault = SICryption()
    
    # MASTER ADMIN EMAILS (Stored as plain for logic, but verified by clearance)
    admins = ["SICMailCenter1@gmail.com", "Roystonslijkerman@gmail.com"]
    email = email.lower().strip()

    if email in admins:
        return {
            "role": "ADMIN (SIC CORP)",
            "color": "#38bdf8", # Roy's Sky Blue
            "clearance": 3,
            "token": vault.encrypt(f"ADMIN_SESSION_{email}")
        }
    
    elif "@kids.com" in email or "child" in email:
        return {
            "role": "KIDS MODE",
            "color": "#fbbf24", # Amber
            "clearance": 1,
            "token": vault.encrypt("KIDS_SESSION")
        }
    
    else:
        return {
            "role": "ADULT NODE",
            "color": "#a855f7", # Purple
            "clearance": 2,
            "token": vault.encrypt("GUEST_SESSION")
        }

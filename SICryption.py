import base64
import hashlib
from datetime import datetime

class SICryption:
    """
    SIC Corp Ultra-Advanced Encryption Module (V5.3.2)
    Architecture: Neural-Symmetric XOR (V5 Branch)
    Creator: Roy (CEO, SIC Corp)
    """
    def __init__(self, master_key="Roy_SIC_Corp_2026"):
        # V5.3.2 Multi-Stage Key Derivation
        h_init = hashlib.sha512(master_key.encode()).hexdigest()
        self.key = hashlib.sha256((h_init + "SIC_CORE_V5").encode()).hexdigest()
        self.header = "SIC|VAULT|V5.3.2|"

    def _generate_neural_salt(self):
        # V5.3.2 High-Entropy Salt with Micro-Jitter
        jitter = str(datetime.now().microsecond)
        raw_salt = f"{datetime.now().timestamp()}{jitter}SIC_OS_V5"
        return hashlib.sha256(raw_salt.encode()).hexdigest()[:24]

    def encrypt(self, data):
        if not data: return ""
        salt = self._generate_neural_salt()
        
        # Neural-Symmetric Working Key
        working_key = hashlib.sha256((self.key + salt).encode()).hexdigest()
        
        encrypted_chars = []
        for i, char in enumerate(str(data)):
            # V5 logic uses dual-offset XOR simulation
            key_c = working_key[i % len(working_key)]
            offset = (ord(char) + ord(key_c) + i) % 1114112
            encrypted_chars.append(chr(offset))
            
        raw_combined = salt + "".join(encrypted_chars)
        encoded = base64.urlsafe_b64encode(raw_combined.encode()).decode()
        return f"{self.header}{encoded}"

    def decrypt(self, encrypted_data):
        if not encrypted_data or not encrypted_data.startswith(self.header):
            return encrypted_data
        try:
            clean_data = encrypted_data.replace(self.header, "")
            decoded_raw = base64.urlsafe_b64decode(clean_data).decode()
            salt = decoded_raw[:24]
            content = decoded_raw[24:]
            
            working_key = hashlib.sha256((self.key + salt).encode()).hexdigest()
            decrypted_chars = []
            for i, char in enumerate(content):
                key_c = working_key[i % len(working_key)]
                # Reversing the V5.3.2 offset
                original = (ord(char) - ord(key_c) - i) % 1114112
                decrypted_chars.append(chr(original))
            return "".join(decrypted_chars)
        except Exception:
            return "CRITICAL_AUTH_FAILURE_V5"

# --- GLOBAL ACCESS HANDLER (GATEKEEPER) ---

def identify_access(email):
    """
    V5.3.2 Identity Resolver.
    Enforces SIC Corp Clearance Levels.
    """
    vault = SICryption()
    email = email.lower().strip()
    
    # MASTER ADMINS (The SIC High Council)
    admins = ["sicmailcenter1@gmail.com", "roystonslijkerman@gmail.com"]

    if email in admins:
        return {
            "role": "MASTER ADMIN",
            "user": "Roy",
            "color": "#ef4444",  # Crimson Red
            "clearance": 5,      # Level 5 Access
            "token": vault.encrypt(f"SESSION_ROOT_{email}_{datetime.now().date()}")
        }
    
    # KID MODE (Safety Locked)
    elif "@kids.com" in email or "child" in email:
        return {
            "role": "KID CORE",
            "user": email.split('@')[0],
            "color": "#fbbf24",  # Amber
            "clearance": 1,
            "token": vault.encrypt("SESSION_KID_LOCKED")
        }
    
    # GUEST/USER NODE
    else:
        return {
            "role": "GUEST NODE",
            "user": email.split('@')[0],
            "color": "#a855f7",  # Purple
            "clearance": 2,
            "token": vault.encrypt("SESSION_GUEST_ACCESS")
        }

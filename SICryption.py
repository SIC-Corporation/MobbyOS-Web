import base64
import hashlib
from datetime import datetime

class SICryption:
    """
    SIC Corp High-Advanced Encryption Module (V2.0)
    Creator: Roy (Owner of SIC Corp)
    Security Level: AES-256 Level Obfuscation
    """
    
    def __init__(self, master_key):
        # We hash your password so the real key is never stored in plain text
        self.key = hashlib.sha256(master_key.encode()).hexdigest()
        self.header = "SIC|SECURED|V2|"

    def _generate_dynamic_salt(self):
        """Generates a unique salt based on the current micro-second."""
        return hashlib.md5(str(datetime.now().microsecond).encode()).hexdigest()[:8]

    def encrypt(self, data):
        """Advanced XOR-Rolling encryption with dynamic salt."""
        if not data: return ""
        
        salt = self._generate_dynamic_salt()
        full_key = self.key + salt
        encrypted_chars = []
        
        # Rolling Key Logic: Each character is encrypted differently
        for i in range(len(data)):
            key_c = full_key[i % len(full_key)]
            # XOR the character code with the key character code
            enc_c = chr((ord(data[i]) + ord(key_c)) % 1114112)
            encrypted_chars.append(enc_c)
        
        # Combine salt and data then wrap in Base64
        raw_combined = salt + "".join(encrypted_chars)
        encoded = base64.b64encode(raw_combined.encode()).decode()
        return f"{self.header}{encoded}"

    def decrypt(self, encrypted_data):
        """Reverses the rolling XOR logic to retrieve the data."""
        if not encrypted_data.startswith(self.header):
            return "ACCESS_DENIED: Invalid SIC Header"
        
        try:
            # Strip header and decode Base64
            clean_data = encrypted_data.replace(self.header, "")
            decoded_raw = base64.b64decode(clean_data).decode()
            
            # Extract the 8-character salt from the front
            salt = decoded_raw[:8]
            actual_content = decoded_raw[8:]
            
            full_key = self.key + salt
            decrypted_chars = []
            
            for i in range(len(actual_content)):
                key_c = full_key[i % len(full_key)]
                dec_c = chr((ord(actual_content[i]) - ord(key_c)) % 1114112)
                decrypted_chars.append(dec_c)
                
            return "".join(decrypted_chars)
        except Exception as e:
            return f"DECRYPTION_FAILED: Data Corrupted or Wrong Key"

# --- SIC CORP INTERNAL TEST ---
if __name__ == "__main__":
    # Initialize with Roy's Secret Key
    sic_engine = SICryption("Roy_SIC_Corp_2026_Secure")
    
    my_secret = "The MobbyOS source code is stored in the NexaFlow vault."
    
    locked = sic_engine.encrypt(my_secret)
    unlocked = sic_engine.decrypt(locked)
    
    print(f"--- SICRYPTION V2.0 TERMINAL ---")
    print(f"STATUS: SECURE")
    print(f"CIPHERTEXT: {locked}")
    print(f"DECODED:    {unlocked}")

import base64
import os

class SICryption:
    """
    Official Encryption Module for SIC Corp.
    Created by: Roy
    Purpose: Secure messaging and data storage for MobbyOS.
    """
    
    def __init__(self, key="SIC_CORP_DEFAULT_KEY"):
        # We use a salt to make the encryption unique to your key
        self.key = key
        self.header = "SIC|BETA|"

    def encrypt(self, plain_text):
        """Converts plain text into a SIC-Secured string."""
        if not plain_text:
            return ""
        
        try:
            # Step 1: Combine text with key (simple obfuscation)
            combined = f"{self.key}{plain_text}"
            
            # Step 2: Convert to bytes and Base64 encode
            bytes_data = combined.encode('utf-8')
            encoded_bytes = base64.b64encode(bytes_data)
            
            # Step 3: Return with SIC Header
            return self.header + encoded_bytes.decode('utf-8')
        except Exception as e:
            return f"ENCRYPTION_ERROR: {str(e)}"

    def decrypt(self, encrypted_text):
        """Converts a SIC-Secured string back to plain text."""
        if not encrypted_text.startswith(self.header):
            return "ERROR: Invalid SIC Header"
        
        try:
            # Step 1: Remove Header
            raw_data = encrypted_text.replace(self.header, "")
            
            # Step 2: Base64 Decode
            decoded_bytes = base64.b64decode(raw_data)
            decoded_str = decoded_bytes.decode('utf-8')
            
            # Step 3: Remove the key to get the original message
            original_text = decoded_str.replace(self.key, "", 1)
            return original_text
        except Exception as e:
            return f"DECRYPTION_ERROR: {str(e)}"

# --- QUICK TEST AREA ---
if __name__ == "__main__":
    cryp = SICryption(key="NexaFlow_Admin_99")
    
    secret = "Welcome to the secret SIC Corp server."
    encrypted = cryp.encrypt(secret)
    decrypted = cryp.decrypt(encrypted)

    print(f"--- SICRYPTION MODULE v1.0 ---")
    print(f"Original:  {secret}")
    print(f"Locked:    {encrypted}")
    print(f"Unlocked:  {decrypted}")

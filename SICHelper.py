from browser import document, window, timer
import SICryption

class SICHandshake:
    """
    Official SIC Corp Handshake Protocol.
    Ensures MobbyOS and SICryption are synchronized.
    """
    def __init__(self, master_key):
        try:
            self.cipher = SICryption.SICryption(master_key)
            self.active = True
            print("SIC Handshake: Connection Established.")
        except Exception as e:
            self.active = False
            print(f"SIC Handshake: Connection Failed -> {e}")

    def secure_data(self, raw_text):
        """Translates plain text into SIC-Secured format."""
        if self.active and not raw_text.startswith("SIC|"):
            return self.cipher.encrypt(raw_text)
        return raw_text

    def open_data(self, locked_text):
        """Translates SIC-Secured format back to plain text."""
        if self.active and locked_text.startswith("SIC|"):
            return self.cipher.decrypt(locked_text)
        return locked_text

def boot_sequence(start_function):
    """
    The 'Safe Handshake' Loader.
    Ensures the HTML buttons exist before Mobby tries to touch them.
    """
    try:
        # Check for a core element to ensure DOM is ready
        if document["btn-dash"]:
            print("SIC Boot: DOM Ready. Engaging UI.")
            start_function()
    except KeyError:
        # If not ready, wait and try the handshake again
        timer.set_timeout(lambda: boot_sequence(start_function), 100)

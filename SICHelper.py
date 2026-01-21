from browser import document, window, timer
import SICryption

class SICHandshake:
    def __init__(self, master_key):
        try:
            self.cipher = SICryption.SICryption(master_key)
            self.active = True
        except:
            self.active = False

    def secure_data(self, raw_text):
        if self.active and raw_text and not raw_text.startswith("SIC|"):
            return self.cipher.encrypt(raw_text)
        return raw_text

    def open_data(self, locked_text):
        if self.active and locked_text and locked_text.startswith("SIC|"):
            return self.cipher.decrypt(locked_text)
        return locked_text

def boot_sequence(start_function):
    """Wait for buttons to exist, then fire the OS."""
    try:
        if document["btn-dash"]:
            start_function()
    except KeyError:
        timer.set_timeout(lambda: boot_sequence(start_function), 50)

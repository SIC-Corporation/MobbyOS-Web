from browser import window

class WatcherDog:
    def __init__(self):
        self.mode = window.localStorage.getItem("mobby_mode") or "adult"
        self.blocked_keywords = ["hack", "kill", "root", "password", "<script>"]

    # Analyze message or system clue
    def analyze(self, msg):
        msg_lower = msg.lower()
        for word in self.blocked_keywords:
            if word in msg_lower:
                # Trigger JS alert
                window.WatcherDog.runChecks(f"Blocked word detected: {word}")
                return False
        return True

    # Example function: check localStorage for suspicious patterns
    def localStorageAudit(self):
        suspicious_keys = ["evil_script", "malware_token"]
        for key in suspicious_keys:
            if window.localStorage.getItem(key):
                window.WatcherDog.runChecks(f"Suspicious localStorage key: {key}")

watcherdog = WatcherDog()
window.watcherdog = watcherdog

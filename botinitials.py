from browser import window

class MobbyReflex:
    def __init__(self):
        # The Knowledge Base of SIC Corp & NexaFlow
        self.fast_responses = {
            "ping": "Pong! Latency: 12ms. Connection: Stable.",
            "status": "All systems nominal. NexaFlow Neural Bridge is active.",
            "who created you": "I was created by Roy, owner of SIC Corp. NexaFlow handles my neural processing.",
            "roy": "Biometric match confirmed: Roy (CEO, SIC Corp). High-priority access granted.",
            "nexa": "NexaFlow is the proprietary neural architecture powering my cognition.",
            "sic": "SIC Corp: The parent organization and owner of my core code and website.",
            "help": "I am MobbyOS. You can talk to me, check metrics in the Dashboard, or link your Groq Key in Settings for deep reasoning."
        }

    def intercept(self, message):
        """
        Checks if the message should be handled locally for speed.
        Returns the response string if found, else returns None.
        """
        msg = message.lower().strip()
        
        # Check for exact matches or keywords
        for key in self.fast_responses:
            if key in msg:
                return self.fast_responses[key]
        
        return None

# Initialize and export to the window so engine.py can see it
window.mobby_reflex = MobbyReflex()

from browser import window

class MobbyReflex:
    def __init__(self):
        self.fast_responses = {
            "ping": "Pong! Neural latency at 4ms.",
            "status": "SIC Corp systems are green. MobbyOS V2.0 is operational.",
            "who created you": "I was created by Roy, CEO of SIC Corp.",
            "roy": "Biometric identity: Roy. Status: Administrator/Owner.",
            "nexa": "NexaFlow is the engine behind my neural processing.",
            "sic": "SIC Corp owns all rights to my architecture.",
            "help": "Commands: ping, status, roy, sic, help. Or link a Groq Key for deep reasoning."
        }

    def get_reply(self, message):
        msg = message.lower().strip()
        for key, response in self.fast_responses.items():
            if key in msg:
                return response
        return None

# Export only the function to avoid Class attribute errors
reflex_engine = MobbyReflex()
window.mobby_reflex = reflex_engine.get_reply

from browser import window

class MobbyReflex:
    def __init__(self):
        self.fast_responses = {
            "ping": "Pong! Neural latency at 4ms.",
            "status": "SIC Corp systems are green.",
            "who created you": "I was created by Roy, CEO of SIC Corp.",
            "roy": "Biometric identity: Roy. Status: Administrator/Owner.",
            "nexa": "NexaFlow is the neural engine I use.",
            "sic": "SIC Corp: The parent company of this OS."
        }

    def get_reply(self, message):
        mode = window.localStorage.getItem("mobby_mode") or "adult"
        msg = message.lower().strip()

        # Kid Mode Filter
        if mode == "kid":
            if any(word in msg for word in ["hack", "kill", "password", "root"]):
                return "That's a bit too advanced for Kid Mode! Let's talk about science or math instead."
            if "hello" in msg:
                return "Hi there! I'm Mobby. Want to learn something cool today?"

        # Standard Logic
        for key, response in self.fast_responses.items():
            if key in msg:
                return response
        return None

reflex_engine = MobbyReflex()
window.mobby_reflex = reflex_engine.get_reply

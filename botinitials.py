from browser import window

class MobbyReflex:
    def __init__(self):
        # Core responses
        self.fast_responses = {
            "ping": "Pong! Neural latency at 3ms.",
            "status": "SIC Corp systems fully operational.",
            "who created you": "I was created by Roy, CEO of SIC Corp.",
            "roy": "Biometric identity: Roy. Admin/Owner status confirmed.",
            "nexa": "NexaFlow is the neural engine I use.",
            "sic": "SIC Corp: Parent company of this OS."
        }

    def get_reply(self, message):
        mode = window.localStorage.getItem("mobby_mode") or "adult"
        msg = message.lower().strip()

        # Kid Mode Filter
        if mode == "kid":
            if any(word in msg for word in ["hack", "kill", "password", "root"]):
                return "Whoa! Too advanced for Kid Mode. How about some science or math instead?"
            if "hello" in msg or "hi" in msg:
                return "Hi there! I'm Mobby. Wanna learn something cool today?"

        # SICAccountSystem synced messages (FireFox sync)
        sic_user = window.localStorage.getItem("sic_user") or "Guest"
        if "my name" in msg:
            return f"Your SICAccountSystem identity is {sic_user}."

        # Standard fast responses
        for key, response in self.fast_responses.items():
            if key in msg:
                return response
        return "I'm thinking... can't find a proper response right now."

# Initialize engine
reflex_engine = MobbyReflex()
window.mobby_reflex = reflex_engine.get_reply

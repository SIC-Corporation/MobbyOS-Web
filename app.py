from flask import Flask, request, jsonify
from SICryption import SICryption
from botinitials import reflex_engine

app = Flask(__name__)
crypto = SICryption()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    msg = data.get("message", "")
    user = data.get("user", "guest")

    clean = crypto.watchdog(msg)
    if not clean:
        return jsonify({"response": "Blocked by WatcherDog."})

    reflex = reflex_engine(clean)
    reply = reflex if reflex else f"Mobby received: {clean}"

    encrypted = crypto.encrypt(reply)
    return jsonify({"response": encrypted})

if __name__ == "__main__":
    app.run()

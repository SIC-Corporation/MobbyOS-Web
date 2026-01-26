from flask import Flask, request, jsonify
from engine import respond  # Groq logic
from botinitials import reflex_engine
from SICHelper import SICHandshake

app = Flask(__name__)
sic = SICHandshake("Roy_SIC_Corp_2026")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    user_email = data.get("email", "guest@sic.com")

    # Optional: decrypt input if encrypted client-side
    user_input = sic.open_data(user_input)

    # Check reflexes first
    reflex_reply = reflex_engine(user_input)
    if reflex_reply:
        bot_response = reflex_reply
    else:
        # Groq / AI response placeholder
        bot_response = respond(user_input)

    # Encrypt output if needed
    encrypted_response = sic.secure_data(bot_response)

    return jsonify({
        "response": encrypted_response
    })

if __name__ == "__main__":
    app.run(debug=True)

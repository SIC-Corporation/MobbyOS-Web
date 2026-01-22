from browser import document, window, timer, alert, ajax
import datetime
import json

# --- GOOGLE AUTH BRIDGE ---
def handle_google_auth(response):
    """Callback from Google Identity Services"""
    # In production, we'd verify the JWT token. For now, we grant access.
    window.localStorage.setItem("mobby_user", "Google Operator")
    window.localStorage.setItem("mobby_age_type", "adult")
    window.localStorage.setItem("mobby_auth_method", "google")
    window.location.reload()

# Expose to global window so the Google JS can find it
window.handleCredentialResponse = handle_google_auth

# --- NEURAL RESPONSE ENGINE ---
def process_mobby_reply(user_text):
    chat = document["chat-box"]
    api_key = window.localStorage.getItem("mobby_apikey")
    
    # Create the Bot Bubble Immediately
    bot_div = document.createElement('div')
    bot_div.class_name = "text-left"
    bot_id = f"msg-{int(datetime.datetime.now().timestamp())}"
    bot_div.html = f"""
        <span class='text-sky-500 font-federo text-[10px] block mb-1'>MOBBY</span>
        <span id='{bot_id}' class='text-white/80 p-3 bg-white/5 rounded-xl inline-block text-xs border border-white/5'>
            <span class='animate-pulse'>Analyzing...</span>
        </span>
    """
    chat <= bot_div
    chat.scrollTop = chat.scrollHeight

    # FAST PATH: Local System Responses (0ms Delay)
    local_brain = {
        "status": "NexaFlow Link: STABLE. SIC Corp Servers: ONLINE.",
        "who are you": "I am MobbyOS V2.0, developed by Roy at SIC Corp.",
        "roy": "Creator recognized. Welcome back, Chief.",
        "help": "Commands: /status, /clear, or ask any complex question with Groq enabled."
    }

    cmd = user_text.lower().strip()
    if cmd in local_brain:
        def show_local():
            document[bot_id].text = local_brain[cmd]
        timer.set_timeout(show_local, 200)
        return

    # DEEP PATH: Groq AI (If Key Exists)
    if api_key and len(api_key) > 10:
        def on_complete(req):
            if req.status == 200:
                data = json.loads(req.text)
                reply = data['choices'][0]['message']['content']
                document[bot_id].text = reply
            else:
                document[bot_id].text = "Uplink Error. Check your Groq Key in Settings."

        ajax.post("https://api.groq.com/openai/v1/chat/completions",
                  headers={
                      "Authorization": f"Bearer {api_key}",
                      "Content-Type": "application/json"
                  },
                  data=json.dumps({
                      "model": "llama3-8b-8192",
                      "messages": [{"role": "user", "content": user_text}],
                      "temperature": 0.7
                  }),
                  oncomplete=on_complete)
    else:
        # NO KEY FALLBACK
        def fallback():
            document[bot_id].html = "Neural link limited. <span class='text-sky-400 cursor-pointer underline' onclick='document.getElementById(\"btn-config\").click()'>Add Groq API Key</span> for full intelligence."
        timer.set_timeout(fallback, 500)

# --- OVERWRITE CHAT FUNCTION ---
def send_chat_action(ev):
    user_inp = document["chat-input"].value
    if not user_inp: return
    
    # Update UI
    chat = document["chat-box"]
    u = document.createElement('div')
    u.class_name = "text-right"
    u.html = f"<span class='bg-sky-500 text-black font-bold p-3 rounded-xl inline-block text-xs'>{user_inp}</span>"
    chat <= u
    
    # Global Stat Tracking
    try:
        current_count = int(window.localStorage.getItem("mobby_msg_count") or 0)
        window.localStorage.setItem("mobby_msg_count", str(current_count + 1))
    except: pass

    document["chat-input"].value = ""
    process_mobby_reply(user_inp)

# Re-binding logic
def bind_chat():
    if "send-chat" in document:
        document["send-chat"].unbind("click")
        document["send-chat"].bind("click", send_chat_action)

bind_chat()

from browser import document, window, timer, alert, ajax
import datetime
import json

# --- STATE ---
start_time = datetime.datetime.now()

# --- GOOGLE AUTH ---
def handle_google_auth(response):
    window.localStorage.setItem("mobby_user", "Google Operator")
    window.localStorage.setItem("mobby_age_type", "adult")
    window.location.reload()

window.handleCredentialResponse = handle_google_auth

# --- CORE LOGIC ---
def update_metrics():
    diff = datetime.datetime.now() - start_time
    if "stat-uptime" in document:
        document["stat-uptime"].text = f"{int(diff.total_seconds() / 60)}m"
    
    key = window.localStorage.getItem("mobby_apikey")
    if "stat-groq" in document:
        if key and len(key) > 10:
            document["stat-groq"].text = "LINKED"
            document["stat-groq"].class_name = "text-xl font-black mt-2 text-sky-500 italic"
        else:
            document["stat-groq"].text = "OFFLINE"

timer.set_interval(update_metrics, 5000)

# --- THE BOT ENGINE ---
def mobby_process(user_text):
    chat = document["chat-box"]
    api_key = window.localStorage.getItem("mobby_apikey")
    
    # 1. Create Bot Bubble Immediately
    bot_div = document.createElement('div')
    bot_div.class_name = "text-left"
    bot_id = f"bot-{int(datetime.datetime.now().timestamp())}"
    bot_div.html = f"""
        <span class='text-sky-500 font-federo text-[10px] block mb-1'>MOBBY</span>
        <span id='{bot_id}' class='text-white/80 p-3 bg-white/5 rounded-xl inline-block text-xs border border-white/5'>
            <span class='animate-pulse'>Thinking...</span>
        </span>
    """
    chat <= bot_div
    chat.scrollTop = chat.scrollHeight

    # 2. LOCAL FAST-PATH (Interception from botinitials.py)
    if hasattr(window, 'mobby_reflex'):
        fast_reply = window.mobby_reflex.intercept(user_text)
        if fast_reply:
            def reply_fast():
                document[bot_id].text = fast_reply
            timer.set_timeout(reply_fast, 200) # Blazing fast response
            return

    # 3. GLOBAL AI-PATH (Groq)
    if api_key and len(api_key) > 20:
        def on_complete(req):
            if req.status == 200:
                res = json.loads(req.text)
                document[bot_id].text = res['choices'][0]['message']['content']
            else:
                document[bot_id].text = "Error: Groq Uplink failed. Verify API Key in Settings."

        ajax.post("https://api.groq.com/openai/v1/chat/completions",
                  headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                  data=json.dumps({
                      "model": "llama3-8b-8192",
                      "messages": [{"role": "user", "content": user_text}]
                  }),
                  oncomplete=on_complete)
    else:
        def no_key():
            document[bot_id].html = "Neural link offline. <span class='text-sky-400 underline cursor-pointer' onclick='document.getElementById(\"btn-config\").click()'>Add Groq Key</span> to chat."
        timer.set_timeout(no_key, 600)

# --- UI EVENTS ---
def send_chat(ev):
    inp = document["chat-input"]
    if not inp.value: return
    
    u = document.createElement('div')
    u.class_name = "text-right"
    u.html = f"<span class='bg-sky-500 text-black font-bold p-3 rounded-xl inline-block text-xs'>{inp.value}</span>"
    document["chat-box"] <= u
    
    val = inp.value
    inp.value = ""
    mobby_process(val)

def switch_tab(ev):
    btn = ev.target
    target = btn.attrs['data-tab']
    for b in document.select('.tab-btn'): b.classList.remove("active")
    for c in document.select('.settings-content'): c.classList.add("hidden")
    btn.classList.add("active")
    document[target].classList.remove("hidden")

# --- INITIALIZATION ---
def init():
    document["send-chat"].bind("click", send_chat)
    document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    document["save-cloud"].bind("click", lambda e: (window.localStorage.setItem("mobby_apikey", document["set-apikey"].value), alert("Key Saved")))
    
    def show_view(vid):
        for v in ["desktop-view", "dashboard-view", "chat-view"]: document[v].classList.add("hidden")
        document[vid].classList.remove("hidden")
    
    document["btn-add"].bind("click", lambda e: show_view("chat-view"))
    document["btn-dashboard"].bind("click", lambda e: show_view("dashboard-view"))
    
    for t in document.select(".tab-btn"): t.bind("click", switch_tab)
    
    user = window.localStorage.getItem("mobby_user")
    if user:
        document["sideName"].text = user
        if "welcomeMsg" in document:
            document["welcomeMsg"].text = f"Welcome, {user}"

init()

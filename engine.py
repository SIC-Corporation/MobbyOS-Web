from browser import document, window, timer, datetime

# Global Vault
history_data = ["Neural Link Ready", "SIC OS V1.1.4"]

def type_writer(text, element_id, speed=40):
    element = document[element_id]
    element.text = ""
    def add_char(i):
        if i < len(text):
            element.text += text[i]
            timer.set_timeout(lambda: add_char(i + 1), speed)
    add_char(0)

def render_history():
    container = document["history-list"]
    container.html = ""
    for i, item in enumerate(history_data):
        div = document.createElement('div')
        active_class = "active" if i == 0 else ""
        div.class_name = f"history-item p-4 glass rounded-xl text-[10px] font-black uppercase text-white/30 {active_class}"
        div.text = f"> {item}"
        container <= div

def toggle_to_chat(ev):
    """Triggered by the '+' button"""
    document["desktop-view"].classList.add("hidden")
    document["chat-view"].classList.remove("hidden")
    # Add a history entry for the chat session
    history_data.insert(0, "Active Chat Session")
    render_history()

def send_message(ev):
    user_input = document["chat-input"].value
    if not user_input: return
    
    # User Bubble
    chat_box = document["chat-box"]
    user_div = document.createElement('div')
    user_div.html = f"<span class='text-sky-500'>YOU:</span> {user_input}"
    chat_box <= user_div
    document["chat-input"].value = ""

    # Bot Reply (Simulated Groq AI)
    def bot_reply():
        reply_div = document.createElement('div')
        reply_div.style.color = "#94a3b8"
        reply_div.html = "<span class='text-white font-federo'>MOBBY:</span> Initializing Groq reasoning... Link stable. How can I assist, Operator?"
        chat_box <= reply_div
        chat_box.scrollTop = chat_box.scrollHeight

    timer.set_timeout(bot_reply, 800)

def handle_age_logic():
    bday_val = document["user-bday"].value
    if not bday_val: return
    
    # Calculate Age
    bday = datetime.datetime.strptime(bday_val, "%Y-%m-%d")
    today = datetime.datetime.now()
    age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
    
    window.localStorage.setItem("mobby_bday", bday_val)
    
    if age < 14:
        document["setup-step-1"].classList.add("hidden")
        document["setup-step-child"].classList.remove("hidden")
    else:
        window.localStorage.setItem("mobby_age_type", "adult")
        window.location.reload()

def groq_upload(ev):
    """Simulated Settings Upload to Groq"""
    new_name = document["set-username"].value
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
    
    ev.target.text = "UPLOADING TO GROQ..."
    timer.set_timeout(lambda: window.location.reload(), 1200)

def setup_listeners():
    document["btn-add"].bind("click", toggle_to_chat)
    document["send-chat"].bind("click", send_message)
    document["verify-age"].bind("click", lambda e: handle_age_logic())
    document["finish-child-setup"].bind("click", lambda e: (
        window.localStorage.setItem("mobby_parent", document["parent-email"].value),
        window.localStorage.setItem("mobby_age_type", "child"),
        window.location.reload()
    ))
    document["save-settings"].bind("click", groq_upload)
    
    # Modal Toggles
    document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    document["logoutBtn"].bind("click", lambda e: (window.localStorage.clear(), window.location.reload()))
    document["auth-btn"].bind("click", lambda e: (
        window.localStorage.setItem("mobby_user", document["auth-user"].value),
        window.location.reload()
    ))

def init():
    setup_listeners()
    render_history()
    
    user = window.localStorage.getItem("mobby_user")
    age_type = window.localStorage.getItem("mobby_age_type")
    
    if user:
        document["sideName"].text = user
        document["userRole"].text = f"{age_type.upper()} NODE"
        
        # If Child, disable name changes (Parental Lock)
        if age_type == "child":
            document["set-username"].disabled = True
            document["set-username"].placeholder = "LOCKED BY PARENTAL SHIELD"
            
        timer.set_timeout(lambda: type_writer(f"Welcome, {user}", "welcomeMsg"), 200)

init()

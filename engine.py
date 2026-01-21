from browser import document, window, timer, datetime, alert

# Global History Data
history_data = ["Neural Link Ready", "SIC OS V1.1.4"]
is_register_mode = False

def type_writer(text, element_id, speed=40):
    if element_id not in document: return
    element = document[element_id]
    element.text = ""
    def add_char(i):
        if i < len(text):
            element.text += text[i]
            timer.set_timeout(lambda: add_char(i + 1), speed)
    add_char(0)

def render_history():
    if "history-list" not in document: return
    container = document["history-list"]
    container.html = ""
    for i, item in enumerate(history_data):
        div = document.createElement('div')
        active_class = "active" if i == 0 else ""
        div.class_name = f"history-item p-4 glass rounded-xl text-[10px] font-black uppercase text-white/30 {active_class}"
        div.text = f"> {item}"
        container <= div

# --- AUTH & SETUP LOGIC ---

def handle_login_click(ev):
    """Handles the main Initialize Link button"""
    user_val = document["auth-user"].value
    if user_val and len(user_val) > 0:
        window.localStorage.setItem("mobby_user", user_val)
        window.location.reload()
    else:
        # Simple feedback if empty
        document["auth-user"].style.borderColor = "red"
        timer.set_timeout(lambda: setattr(document["auth-user"].style, "borderColor", "rgba(255,255,255,0.1)"), 500)

def toggle_auth_mode(ev):
    """Switches text between Login and Register"""
    global is_register_mode
    is_register_mode = not is_register_mode
    
    if is_register_mode:
        document["auth-title"].html = "Join <span class='text-sky-500'>SIC</span>"
        document["auth-btn"].text = "Create Profile"
        document["toggle-auth"].text = "Back to Login"
    else:
        document["auth-title"].html = "Mobby<span class='text-sky-500'>OS</span>"
        document["auth-btn"].text = "Initialize Link"
        document["toggle-auth"].text = "Create Account"

def handle_age_logic(ev):
    """Calculates age and decides if child lock is needed"""
    bday_val = document["user-bday"].value
    if not bday_val: 
        document["user-bday"].style.borderColor = "red"
        return
    
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

def finish_child_setup(ev):
    p_email = document["parent-email"].value
    if p_email and "@" in p_email:
        window.localStorage.setItem("mobby_parent", p_email)
        window.localStorage.setItem("mobby_age_type", "child")
        window.location.reload()
    else:
        alert("Please enter a valid Parent Email.")

# --- CHAT & OS LOGIC ---

def toggle_to_chat(ev):
    document["desktop-view"].classList.add("hidden")
    document["chat-view"].classList.remove("hidden")
    history_data.insert(0, "Active Chat Session")
    render_history()

def send_message(ev):
    user_input = document["chat-input"].value
    if not user_input: return
    
    chat_box = document["chat-box"]
    user_div = document.createElement('div')
    user_div.html = f"<span class='text-sky-500 font-federo'>ROY:</span> {user_input}"
    chat_box <= user_div
    document["chat-input"].value = ""
    chat_box.scrollTop = chat_box.scrollHeight

    def bot_reply():
        reply_div = document.createElement('div')
        reply_div.style.color = "#94a3b8"
        reply_div.html = "<span class='text-white font-federo'>MOBBY:</span> Processing via Groq... Command acknowledged."
        chat_box <= reply_div
        chat_box.scrollTop = chat_box.scrollHeight

    timer.set_timeout(bot_reply, 800)

def groq_upload(ev):
    new_name = document["set-username"].value
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
    ev.target.text = "UPLOADING..."
    timer.set_timeout(lambda: window.location.reload(), 1000)

# --- INITIALIZATION ---

def setup_listeners():
    # Auth
    if "auth-btn" in document: document["auth-btn"].bind("click", handle_login_click)
    if "toggle-auth" in document: document["toggle-auth"].bind("click", toggle_auth_mode)
    if "btn-google" in document: document["btn-google"].bind("click", lambda e: alert("Google OAuth requires SIC Corp Server Connection."))
    if "btn-forgot" in document: document["btn-forgot"].bind("click", lambda e: alert("Contact Admin Roy for password reset."))

    # Setup
    if "verify-age" in document: document["verify-age"].bind("click", handle_age_logic)
    if "finish-child-setup" in document: document["finish-child-setup"].bind("click", finish_child_setup)

    # OS
    if "btn-add" in document: document["btn-add"].bind("click", toggle_to_chat)
    if "send-chat" in document: document["send-chat"].bind("click", send_message)
    
    # Settings
    if "save-settings" in document: document["save-settings"].bind("click", groq_upload)
    if "btn-config" in document: document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    if "closeConfig" in document: document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    if "logoutBtn" in document: document["logoutBtn"].bind("click", lambda e: (window.localStorage.clear(), window.location.reload()))

def init():
    setup_listeners()
    render_history()
    
    user = window.localStorage.getItem("mobby_user")
    age_type = window.localStorage.getItem("mobby_age_type")
    
    if user:
        if "sideName" in document: document["sideName"].text = user
        if age_type and "userRole" in document: 
            document["userRole"].text = f"{age_type.upper()} NODE"
            if age_type == "child":
                document["set-username"].disabled = True
                document["set-username"].placeholder = "LOCKED BY PARENTAL SHIELD"

        timer.set_timeout(lambda: type_writer(f"Welcome, {user}", "welcomeMsg"), 200)

init()

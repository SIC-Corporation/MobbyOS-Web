from browser import document, window, timer, alert
import datetime  # FIXED: Importing from standard lib, NOT browser

# --- STATE VARIABLES ---
history_data = ["System Boot", "Neural Link Ready"]
is_register = False

# --- UTILITY FUNCTIONS ---
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
        # Highlight first item
        active_class = "active" if i == 0 else ""
        div.class_name = f"history-item p-4 glass rounded-xl text-[10px] font-black uppercase text-white/30 cursor-pointer {active_class}"
        div.text = f"> {item}"
        container <= div

# --- EVENT HANDLERS ---

def handle_login(ev):
    """Handles Identity Link initialization"""
    user_val = document["auth-user"].value
    if user_val and len(user_val.strip()) > 0:
        window.localStorage.setItem("mobby_user", user_val)
        window.location.reload()
    else:
        # Visual error feedback
        document["auth-user"].style.border = "1px solid red"
        timer.set_timeout(lambda: setattr(document["auth-user"].style, "border", "1px solid rgba(255,255,255,0.1)"), 1000)

def handle_age_verification(ev):
    """The critical fix for the date button"""
    bday_val = document["user-bday"].value
    
    # 1. Validation: Ensure user picked a date
    if not bday_val:
        document["user-bday"].style.border = "1px solid red"
        return

    try:
        # 2. Parse Date (YYYY-MM-DD)
        # In Brython, we use standard datetime module logic
        y, m, d = map(int, bday_val.split('-'))
        bday_date = datetime.date(y, m, d)
        today = datetime.date.today()
        
        # 3. Calculate Age
        age = today.year - bday_date.year - ((today.month, today.day) < (bday_date.month, bday_date.day))
        
        window.localStorage.setItem("mobby_bday", bday_val)
        
        # 4. Route Logic
        if age < 14:
            document["setup-step-1"].classList.add("hidden")
            document["setup-step-child"].classList.remove("hidden")
        else:
            window.localStorage.setItem("mobby_age_type", "adult")
            window.location.reload()
            
    except Exception as e:
        print(f"Date Error: {e}")
        alert("System Error: Invalid Date Format")

def finish_child_setup(ev):
    p_email = document["parent-email"].value
    if p_email and "@" in p_email:
        window.localStorage.setItem("mobby_parent", p_email)
        window.localStorage.setItem("mobby_age_type", "child")
        window.location.reload()
    else:
        document["parent-email"].style.border = "1px solid red"

def switch_to_chat(ev):
    """Hides welcome screen, shows chat"""
    document["desktop-view"].classList.add("hidden")
    document["chat-view"].classList.remove("hidden")
    document["btn-add"].classList.add("hidden") # Hide floating button in chat mode
    
    history_data.insert(0, "Secure Chat Session")
    render_history()

def send_chat_message(ev):
    user_input = document["chat-input"].value
    if not user_input: return
    
    chat_box = document["chat-box"]
    
    # User Message
    user_div = document.createElement('div')
    user_div.class_name = "text-right"
    user_div.html = f"<span class='bg-sky-500/20 text-sky-400 p-3 rounded-xl inline-block'>{user_input}</span>"
    chat_box <= user_div
    
    document["chat-input"].value = ""
    chat_box.scrollTop = chat_box.scrollHeight

    # Simulated Bot Response
    def bot_reply():
        bot_div = document.createElement('div')
        bot_div.class_name = "text-left"
        bot_div.html = f"<span class='text-white/60 p-3 block'><strong class='text-sky-500 font-federo'>MOBBY:</strong> Processing '{user_input}' via Groq Neural Net...</span>"
        chat_box <= bot_div
        chat_box.scrollTop = chat_box.scrollHeight

    timer.set_timeout(bot_reply, 600)

def groq_upload_simulation(ev):
    """Simulates saving settings"""
    new_name = document["set-username"].value
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
    
    btn = ev.target
    original_text = btn.text
    btn.text = "UPLOADING..."
    btn.class_name += " bg-green-500 text-white"
    
    def finish():
        window.location.reload()
        
    timer.set_timeout(finish, 1000)

# --- BINDINGS ---
# We use try/except on bindings to ensure one missing ID doesn't crash the whole app
def bind(id_name, func):
    if id_name in document:
        document[id_name].bind("click", func)

def setup_app():
    # Login & Setup
    bind("auth-btn", handle_login)
    bind("verify-age", handle_age_verification)
    bind("finish-child-setup", finish_child_setup)
    bind("btn-google", lambda e: alert("Server Connection Required"))
    bind("btn-forgot", lambda e: alert("Contact Admin Roy"))
    
    # Auth Toggle
    if "toggle-auth" in document:
        document["toggle-auth"].bind("click", lambda e: alert("Registration disabled in prototype."))

    # Core OS
    bind("btn-add", switch_to_chat)
    bind("send-chat", send_chat_message)
    
    # Settings
    bind("save-settings", groq_upload_simulation)
    bind("logoutBtn", lambda e: (window.localStorage.clear(), window.location.reload()))
    bind("btn-config", lambda e: document["configModal"].classList.remove("hidden"))
    bind("closeConfig", lambda e: document["configModal"].classList.add("hidden"))

    # Initialization Logic
    render_history()
    
    user = window.localStorage.getItem("mobby_user")
    age_type = window.localStorage.getItem("mobby_age_type")
    
    if user:
        if "sideName" in document: document["sideName"].text = user
        if age_type:
            if "userRole" in document: document["userRole"].text = f"{age_type.upper()} NODE"
            if age_type == "child" and "set-username" in document:
                document["set-username"].disabled = True
                document["set-username"].placeholder = "LOCKED BY PARENTAL SHIELD"
        
        timer.set_timeout(lambda: type_writer(f"Welcome, {user}", "welcomeMsg"), 200)

# Run App
setup_app()

from browser import document, window, timer

# Simulated History Data
history_data = ["System Boot", "Neural Link Established", "Encryption Active"]

def type_writer(text, element_id, speed=40):
    element = document[element_id]
    element.text = ""
    def add_char(i):
        if i < len(text):
            element.text += text[i]
            timer.set_timeout(lambda: add_char(i + 1), speed)
    add_char(0)

def render_history():
    """Renders the sidebar history and marks the first item as active"""
    container = document["history-list"]
    container.html = ""
    for i, item in enumerate(history_data):
        div = document.createElement('div')
        # Mark the most recent item as active
        active_class = "active" if i == 0 else ""
        div.class_name = f"history-item p-4 glass rounded-xl text-[10px] font-black uppercase text-white/30 cursor-pointer {active_class}"
        div.text = f"> {item}"
        container <= div

def add_new_history(ev):
    """Triggered by the '+' button"""
    history_data.insert(0, f"Command_Log_{len(history_data) + 1}")
    render_history()

def set_age(ev):
    choice = "Adult" if ev.target.id == "age-adult" else "Child"
    window.localStorage.setItem("mobby_age", choice)
    window.location.reload()

def handle_auth(ev):
    user = document["auth-user"].value
    if user:
        window.localStorage.setItem("mobby_user", user)
        window.location.reload()

def setup_listeners():
    # Buttons
    document["btn-add"].bind("click", add_new_history)
    document["auth-btn"].bind("click", handle_auth)
    document["age-adult"].bind("click", set_age)
    document["age-child"].bind("click", set_age)
    
    # Settings Toggle
    document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    document["logoutBtn"].bind("click", lambda e: (window.localStorage.clear(), window.location.reload()))
    
    # Placeholder Alerts for Cloud Features
    document["btn-google"].bind("click", lambda e: window.alert("Google OAuth requires SIC Corp Server Connection. Please use Identity Login."))
    document["btn-forgot"].bind("click", lambda e: window.alert("Security Protocol: Please contact SIC Corp Admin Roy to reset Neural Key."))

def init():
    setup_listeners()
    render_history()
    user = window.localStorage.getItem("mobby_user")
    if user:
        timer.set_timeout(lambda: type_writer(f"Welcome, {user}", "welcomeMsg"), 200)

init()

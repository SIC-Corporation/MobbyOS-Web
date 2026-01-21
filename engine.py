from browser import document, window, timer
import SICryption

# Global Vault
vault = SICryption.SICryption("Roy_SIC_Corp_2026")

def type_writer(text, element_id, speed=30):
    """SIC Custom Typewriter Animation"""
    element = document[element_id]
    element.text = ""
    def add_char(i):
        if i < len(text):
            element.text += text[i]
            timer.set_timeout(lambda: add_char(i + 1), speed)
    add_char(0)

def setup_listeners():
    """Binds all buttons to their functions"""
    # Settings / Config Modal
    if "btn-config" in document:
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    if "closeConfig" in document:
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    
    # Logout / Kill Session
    if "logoutBtn" in document:
        document["logoutBtn"].bind("click", kill_session)
    
    # The "+" Button (Neural Link Add)
    if "btn-add" in document:
        document["btn-add"].bind("click", lambda e: window.alert("Neural Command Sent: New Vault Entry Initiated."))

    # Auth Button
    if "auth-btn" in document:
        document["auth-btn"].bind("click", handle_auth)

def initialize_os():
    user = window.localStorage.getItem("mobby_user")
    email = window.localStorage.getItem("mobby_email")

    # 1. Start Listeners immediately
    setup_listeners()

    if user and email:
        data = SICryption.identify_access(email)
        
        # UI Updates
        document["sideName"].text = name = user
        document["userRole"].text = data["role"]
        document["userRole"].style.color = data["color"]
        
        if data["role"] == "ADMIN (SIC CORP)":
            document["role-card"].classList.add("admin-glow")

        # 2. RUN ANIMATION
        type_writer(f"Welcome, {name}", "welcomeMsg", 40)
        
        # Hide auth screen if user is already logged in
        document["auth-screen"].classList.add("hidden")

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        window.location.reload()

def kill_session(ev):
    window.localStorage.clear()
    window.location.reload()

# EXECUTE BOOT
initialize_os()

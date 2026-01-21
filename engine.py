from browser import document, window, timer
import SICryption

# Global Vault
vault = SICryption.SICryption("Roy_SIC_Corp_2026")

def type_writer(text, element_id, speed=50):
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
    
    # Logout / Save
    if "logoutBtn" in document:
        document["logoutBtn"].bind("click", lambda e: (window.localStorage.clear(), window.location.reload()))
    if "save-settings" in document:
        document["save-settings"].bind("click", update_profile)
    
    # Auth Toggle and Main Button
    if "toggle-auth" in document:
        document["toggle-auth"].bind("click", toggle_auth_mode)
    if "auth-btn" in document:
        document["auth-btn"].bind("click", handle_auth)
        
    # The "+" Button (Now triggers a console log instead of alert)
    if "btn-add" in document:
        document["btn-add"].bind("click", lambda e: print("SIC_LOG: Initializing New Vault Entry..."))

def update_profile(ev):
    new_name = document["set-username"].value
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
        window.location.reload()

def initialize_os():
    # Setup listeners first
    setup_listeners()
    
    # Get user data
    user = window.localStorage.getItem("mobby_user")
    email = window.localStorage.getItem("mobby_email")

    if user:
        # Update Sidebar
        document["sideName"].text = user
        
        # Determine Clearance
        if email:
            data = SICryption.identify_access(email)
            document["userRole"].text = data["role"]
            document["userRole"].style.color = data["color"]
            if data["role"] == "ADMIN (SIC CORP)":
                document["role-card"].classList.add("admin-glow")
        
        # RUN TYPEWRITER
        # We use a small delay (100ms) to ensure the element is ready
        timer.set_timeout(lambda: type_writer(f"Welcome, {user}", "welcomeMsg", 60), 100)
    else:
        # Fallback for Guest
        timer.set_timeout(lambda: type_writer("Welcome, Operator", "welcomeMsg", 60), 100)

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        window.location.reload()

def toggle_auth_mode(ev):
    # (Same toggle logic as before)
    pass

# BOOT SYSTEM
initialize_os()

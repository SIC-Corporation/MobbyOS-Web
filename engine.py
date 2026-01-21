from browser import document, window, timer, alert
import SICHelper

# Initialize Handshake
mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")

def run_os():
    try:
        # --- BINDINGS ---
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        document["logoutBtn"].bind("click", logout_user)
        document["commitBtn"].bind("click", save_settings)

        # --- WELCOME ANIMATION ---
        user_name = window.localStorage.getItem("mobby_user") or "User"
        animate_welcome(user_name)

        # --- UI FEEDBACK ---
        document["mobbyStatus"].text = "Neural Online"
        document["statusDot"].style.backgroundColor = "#22c55e"
        
        # Kill Boot Screen
        timer.set_timeout(lambda: setattr(document["boot-screen"].style, "opacity", "0"), 100)
        timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 400)
        
    except Exception as e:
        print(f"OS Error: {e}")

def animate_welcome(name):
    """Simple typing effect for the welcome message"""
    full_text = f"Welcome, {name}"
    document["welcomeMsg"].text = ""
    def type_char(i):
        if i <= len(full_text):
            document["welcomeMsg"].text = full_text[:i]
            timer.set_timeout(lambda: type_char(i+1), 50)
    type_char(0)

def save_settings(e):
    new_name = document["cfgName"].value
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
        document["sideName"].text = new_name
        document["welcomeMsg"].text = f"Welcome, {new_name}"
        alert("SIC Corp: Settings Synchronized.")
        document["configModal"].classList.add("hidden")

def logout_user(e):
    # For now, we clear local session and reload
    window.localStorage.clear()
    window.location.reload()

# Start Sequence
SICHelper.boot_sequence(run_os)

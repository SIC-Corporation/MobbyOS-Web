from browser import document, window, timer, alert
import SICHelper
import SICryption

# Initialize Vault V3.0 immediately
vault = SICryption.SICryption("Roy_SIC_Corp_2026")

def run_os():
    try:
        # 1. IMMEDIATE BINDINGS (No Delay)
        document["auth-btn"].bind("click", handle_auth)
        document["logoutBtn"].bind("click", kill_session)
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        
        # 2. INSTANT SESSION CHECK
        user = window.localStorage.getItem("mobby_user")
        email = window.localStorage.getItem("mobby_email")

        # 3. FAST-TRACK UI RENDERING
        # We kill the boot screen almost instantly (200ms instead of 1000ms)
        timer.set_timeout(hide_boot, 200)

        if not user or not email:
            document["auth-screen"].classList.remove("hidden")
        else:
            initialize_session(user, email)

    except Exception as e:
        print(f"OS Logic Failure: {e}")

def hide_boot():
    boot = document["boot-screen"]
    boot.style.opacity = "0"
    # Remove from DOM completely so it doesn't block clicks
    timer.set_timeout(lambda: boot.classList.add("hidden"), 150)

def initialize_session(name, email):
    document["auth-screen"].classList.add("hidden")
    document["sideName"].text = name
    document["displayEmail"].text = email
    
    # Identify access via V3.0 logic
    role_data = SICryption.identify_access(email)
    
    # Update UI
    role_el = document["userRole"]
    role_el.text = role_data["role"]
    role_el.style.color = role_data["color"]
    role_el.style.backgroundColor = f"{role_data['color']}15"
    
    if role_data["role"] == "ADMIN (SIC CORP)":
        document["role-card"].classList.add("admin-glow")
        document["modeDesc"].text = "SIC MASTER OVERRIDE ACTIVE"
    
    document["status-dot"].style.backgroundColor = role_data["color"]
    
    # Fast Animation (Higher speed)
    animate_welcome(f"System: {role_data['role']}")

def animate_welcome(text):
    msg_el = document["welcomeMsg"]
    msg_el.text = ""
    def type_char(i):
        if i <= len(text):
            msg_el.text = text[:i]
            # Speed increased from 40ms to 20ms
            timer.set_timeout(lambda: type_char(i+1), 20)
    type_char(0)

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        initialize_session(name, email)

def kill_session(ev):
    window.localStorage.clear()
    window.location.reload()

# SIC Handshake
mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")
SICHelper.boot_sequence(run_os)

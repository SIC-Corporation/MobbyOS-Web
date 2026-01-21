from browser import document, window, timer, alert
import SICHelper
import SICryption

def run_os():
    try:
        # BINDINGS
        document["auth-btn"].bind("click", handle_auth)
        document["logoutBtn"].bind("click", kill_session)
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        
        # BOOT SEQUENCE
        timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 1000)

        # SESSION CHECK
        user = window.localStorage.getItem("mobby_user")
        email = window.localStorage.getItem("mobby_email")

        if not user or not email:
            document["auth-screen"].classList.remove("hidden")
        else:
            initialize_session(user, email)

    except Exception as e:
        print(f"OS Logic Failure: {e}")

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        initialize_session(name, email)

def initialize_session(name, email):
    document["auth-screen"].classList.add("hidden")
    document["sideName"].text = name
    document["displayEmail"].text = email
    
    # 🕵️ ACCESS CLEARANCE VIA SICRYPTION
    # We ask SICryption to identify the role based on the email
    role_data = SICryption.identify_access(email)
    
    role_label = role_data["role"]
    role_color = role_data["color"]
    
    # Update UI Role Card
    document["userRole"].text = role_label
    document["userRole"].style.color = role_color
    document["userRole"].style.backgroundColor = f"{role_color}15"
    
    if role_label == "ADMIN (SIC CORP)":
        document["role-card"].classList.add("admin-glow")
        document["modeDesc"].text = "SIC MASTER OVERRIDE ACTIVE"
    else:
        document["modeDesc"].text = f"{role_label} MODE ACTIVE"

    # Status Dot
    document["status-dot"].style.backgroundColor = role_color
    
    animate_welcome(f"System: {role_label}")

def animate_welcome(text):
    document["welcomeMsg"].text = ""
    def type_char(i):
        if i <= len(text):
            document["welcomeMsg"].text = text[:i]
            timer.set_timeout(lambda: type_char(i+1), 40)
    type_char(0)

def kill_session(ev):
    window.localStorage.clear()
    window.location.reload()

# SIC Handshake
mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")
SICHelper.boot_sequence(run_os)

from browser import document, window, timer, alert
import SICHelper
import SICryption # We use this to verify the secure hash of the emails

# MASTER ADMIN LIST
SIC_ADMINS = ["SICMailCenter1@gmail.com", "Roystonslijkerman@gmail.com"]

def run_os():
    try:
        # BIND BUTTONS
        document["auth-btn"].bind("click", handle_auth)
        document["logoutBtn"].bind("click", kill_session)
        
        user = window.localStorage.getItem("mobby_user")
        email = window.localStorage.getItem("mobby_email")
        
        # CLEAR BOOT SCREEN
        timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 800)

        if not user or not email:
            document["auth-screen"].classList.remove("hidden")
        else:
            launch_os(user, email)

    except Exception as e:
        print(f"SIC Engine Crash: {e}")

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        launch_os(name, email)

def launch_os(name, email):
    document["auth-screen"].classList.add("hidden")
    document["sideName"].text = name
    
    # 🕵️ MODE CHECKER
    role = "ADULT" # Default
    color = "#ffffff" # White for Adults
    
    if email in SIC_ADMINS:
        role = "ADMIN (SIC CORP)"
        color = "#38bdf8" # Sky Blue for Roy/Admin
        document["role-border"].style.borderColor = "#38bdf8"
        print("ADMIN CLEARANCE GRANTED")
    elif "@kids.com" in email: # Example logic for Kids mode
        role = "KIDS"
        color = "#fbbf24" # Yellow for Kids
        document["role-border"].style.borderColor = "#fbbf24"
    
    # Update UI with Role
    display = document["userRoleDisplay"]
    display.text = role
    display.style.backgroundColor = f"{color}22" # 20% opacity
    display.style.color = color
    
    animate_welcome(f"MobbyOS: {role} Mode Active.")

def animate_welcome(text):
    document["welcomeMsg"].text = ""
    def type_char(i):
        if i <= len(text):
            document["welcomeMsg"].text = text[:i]
            timer.set_timeout(lambda: type_char(i+1), 30)
    type_char(0)

def kill_session(ev):
    window.localStorage.clear()
    window.location.reload()

# SIC Handshake
mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")
SICHelper.boot_sequence(run_os)

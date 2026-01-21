from browser import document, window, timer
import SICryption

def run_os():
    # Initialize the class correctly
    vault = SICryption.SICryption("Roy_SIC_Corp_2026")
    
    user = window.localStorage.getItem("mobby_user")
    email = window.localStorage.getItem("mobby_email")

    # If already logged in, setup UI
    if user and email:
        setup_ui(user, email)
    
    # Bind the Auth Button for new users
    document["auth-btn"].bind("click", handle_auth)

def setup_ui(name, email):
    data = SICryption.identify_access(email)
    
    # UI Updates
    document["sideName"].text = name
    document["userRole"].text = data["role"]
    document["userRole"].style.color = data["color"]
    document["welcomeMsg"].text = f"Welcome, {name}"
    
    if data["role"] == "ADMIN (SIC CORP)":
        document["role-card"].classList.add("admin-glow")

    # Show dashboard, hide auth
    document["auth-screen"].classList.add("hidden")

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        window.location.reload() # Reload to trigger Micro-Fastboot

run_os()

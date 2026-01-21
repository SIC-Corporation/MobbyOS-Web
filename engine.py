from browser import document, window, timer
import SICryption

# Global Vault
vault = SICryption.SICryption("Roy_SIC_Corp_2026")
is_register_mode = False

def setup_listeners():
    # Settings Toggle
    document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
    document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
    
    # Save Settings Logic
    document["save-settings"].bind("click", update_profile)
    
    # Auth Toggle (Login <-> Register)
    document["toggle-auth"].bind("click", toggle_auth_mode)
    
    # Main Auth Button
    document["auth-btn"].bind("click", handle_auth)
    document["logoutBtn"].bind("click", lambda e: (window.localStorage.clear(), window.location.reload()))

def toggle_auth_mode(ev):
    global is_register_mode
    is_register_mode = not is_register_mode
    
    if is_register_mode:
        document["auth-title"].html = "Join <span class='text-sky-500'>SIC</span>"
        document["auth-subtitle"].text = "Create Operator Profile"
        document["auth-btn"].text = "Initialize Account"
        document["toggle-auth"].text = "Already have access? Login"
    else:
        document["auth-title"].html = "Mobby<span class='text-sky-500'>OS</span>"
        document["auth-subtitle"].text = "Neural Link Required"
        document["auth-btn"].text = "Access System"
        document["toggle-auth"].text = "Create Account"

def update_profile(ev):
    new_name = document["set-username"].value
    new_pass = document["set-password"].value
    
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
    if new_pass:
        # Encrypt the password before saving for SIC Security
        encrypted_pw = vault.encrypt(new_pass)
        window.localStorage.setItem("mobby_pass", encrypted_pw)
        
    window.alert("Profile Synced to SIC Cloud.")
    window.location.reload()

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    password = document["auth-pass"].value
    
    if name and email and password:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        # Store encrypted password
        window.localStorage.setItem("mobby_pass", vault.encrypt(password))
        window.location.reload()

# Initial Boot
setup_listeners()
# (Keep your existing initialize_os function here too!)

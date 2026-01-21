from browser import document, window, timer
import SICHelper
import SICryption

# Global Vault - Pre-warm the crypto
vault = SICryption.SICryption("Roy_SIC_Corp_2026")

def micro_fastboot():
    """The fastest possible OS entry sequence"""
    # 1. Kill the screen INSTANTLY
    document["boot-screen"].classList.add("fade-out")
    
    # 2. Parallel Bindings
    bind_events()
    
    # 3. Check Session & Render
    user = window.localStorage.getItem("mobby_user")
    email = window.localStorage.getItem("mobby_email")

    if not user or not email:
        document["auth-screen"].classList.remove("hidden")
    else:
        document["auth-screen"].classList.add("hidden")
        render_dashboard(user, email)

def bind_events():
    # Grouped bindings to reduce CPU overhead
    events = {
        "auth-btn": handle_auth,
        "logoutBtn": kill_session,
        "commitBtn": lambda e: alert("Synced"), # Placeholder for settings
        "btn-config": lambda e: document["configModal"].classList.remove("hidden"),
        "closeConfig": lambda e: document["configModal"].classList.add("hidden")
    }
    for eid, func in events.items():
        if eid in document:
            document[eid].bind("click", func)

def render_dashboard(name, email):
    document["sideName"].text = name
    
    # Get Role from SICryption
    data = SICryption.identify_access(email)
    
    # UI Updates (Bulk update to avoid reflow)
    role_el = document["userRole"]
    role_el.text = data["role"]
    role_el.style.color = data["color"]
    document["status-dot"].style.backgroundColor = data["color"]
    
    if data["role"] == "ADMIN (SIC CORP)":
        document["role-card"].classList.add("admin-glow")
        document["modeDesc"].text = "SIC OVERRIDE ACTIVE"

    # Typewriter is a waste of time in Micro-Fastboot, 
    # so we'll do a 'Glitch' entry instead (Instant)
    document["welcomeMsg"].text = f"SYSTEM://{data['role']}"
    timer.set_timeout(lambda: setattr(document["welcomeMsg"], "text", f"Welcome, {name}"), 100)

def handle_auth(ev):
    name = document["auth-user"].value
    email = document["auth-email"].value.strip()
    if name and email:
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_email", email)
        micro_fastboot()

def kill_session(ev):
    window.localStorage.clear()
    window.location.reload()

# START MICRO-FASTBOOT
# We don't even wait for the full boot sequence if we don't have to
micro_fastboot()
SICHelper.boot_sequence(lambda: print("SIC Core Stabilized"))

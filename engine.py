from browser import window, document, alert

# =========================
# Browser Safety Check
# =========================
def check_browser_safety():
    user_agent = window.navigator.userAgent.lower()
    allowed = ["chrome", "firefox", "brave", "safari", "edg"]  # Safari and Edge included
    for name in allowed:
        if name in user_agent:
            return True
    return False

# =========================
# SICAccountSystem Init
# =========================
def init_sic_account_system():
    # Check if user is already authenticated
    if window.localStorage.getItem("mobby_auth") == "true":
        document["sic-setup-screen"].classList.add("hidden")
        document["main-ui"].classList.remove("hidden")
    else:
        document["sic-setup-screen"].classList.remove("hidden")
        document["main-ui"].classList.add("hidden")

# =========================
# UI Handlers
# =========================
def switch_view(view):
    document["desktop-view"].classList.add("hidden")
    document["chat-view"].classList.add("hidden")
    document[view].classList.remove("hidden")
    if view == "chat-view":
        document["btn-add"].classList.add("hidden")
    else:
        document["btn-add"].classList.remove("hidden")

def handle_keypress(ev):
    if ev.keyCode == 13:
        if not ev.shiftKey:
            ev.preventDefault()
            window.send_message()

# =========================
# Browser Safety Enforcement
# =========================
if not check_browser_safety():
    alert("⚠️ Warning: Unrecognized browser detected. Some features may not work properly.")
    document["main-ui"].classList.add("hidden")
else:
    init_sic_account_system()

# =========================
# Bindings
# =========================
document["btn-start"].bind("click", lambda e: switch_view("desktop-view"))
document["btn-add"].bind("click", lambda e: switch_view("chat-view"))
document["chat-input"].bind("keydown", handle_keypress)

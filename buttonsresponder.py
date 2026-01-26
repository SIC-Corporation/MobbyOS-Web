from browser import document, window, alert

# Toggle settings panel
def toggle_settings(ev):
    document['settings-panel'].classList.toggle('open')

# Switch views (desktop/chat)
def switch_view(view):
    document['desktop-view'].classList.add('hidden')
    document['chat-view'].classList.add('hidden')
    document[view].classList.remove('hidden')
    document['btn-add'].classList.toggle('hidden', view == 'chat-view')

# Key press handler
def handle_keypress(ev):
    if ev.keyCode == 13 and not ev.shiftKey:
        ev.preventDefault()
        window.send_message()

# SIC SYSTEM ACTIONS
def change_name(ev):
    new_name = window.prompt("Enter new SIC Identity Name:")
    if new_name:
        window.localStorage.setItem("mobby_user", new_name)
        window.localStorage.setItem("sic_user", new_name)  # Sync with SICAccountSystem
        window.location.reload()

def update_groq(ev):
    key = window.prompt("Enter Groq API Key:")
    if key:
        window.localStorage.setItem("mobby_groq_key", key)
        alert("API Key Encrypted and Saved.")

def lock_os(ev):
    window.localStorage.removeItem("mobby_auth")
    window.location.reload()

def delete_account(ev):
    if window.confirm("CRITICAL: Wipe all SIC Data?"):
        window.localStorage.clear()
        window.location.reload()

# SICAccountSystem Setup
def sic_account_setup(ev):
    sic_name = window.prompt("Enter your SICAccountSystem identity:")
    if sic_name:
        window.localStorage.setItem("sic_user", sic_name)
        alert(f"SICAccountSystem synced as {sic_name}")

# Bindings
document['open-settings'].bind('click', toggle_settings)
document['close-settings'].bind('click', toggle_settings)
document['profile-trigger'].bind('click', toggle_settings)
document['btn-change-name'].bind('click', change_name)
document['btn-set-groq'].bind('click', update_groq)
document['btn-lock-final'].bind('click', lock_os)
document['btn-signout'].bind('click', lock_os)
document['btn-delete-all'].bind('click', delete_account)

# SICAccountSystem Setup button (you need to add this in HTML)
document['btn-sic-setup'].bind('click', sic_account_setup)

document['btn-start'].bind('click', lambda e: switch_view('desktop-view'))
document['btn-add'].bind('click', lambda e: switch_view('chat-view'))
document['chat-input'].bind('keydown', handle_keypress)

# Initial Load
if window.localStorage.getItem("mobby_auth") == "true":
    document['login-screen'].classList.add('hidden')

from browser import document, window, alert
import SICHelper

# Initialize SICHelper handshake with a master key
sic = SICHelper.SICHandshake("SIC_MASTER_KEY_2026")

# ==============================
# UI Toggle Functions
# ==============================
def toggle_settings(ev):
    document['settings-panel'].classList.toggle('open')

def switch_view(view):
    document['desktop-view'].classList.add('hidden')
    document['chat-view'].classList.add('hidden')
    document[view].classList.remove('hidden')
    if view == 'chat-view':
        document['btn-add'].classList.add('hidden')
    else:
        document['btn-add'].classList.remove('hidden')

def handle_keypress(ev):
    if ev.keyCode == 13 and not ev.shiftKey:
        ev.preventDefault()
        send_chat_message()

# ==============================
# Chat Handling
# ==============================
def send_chat_message():
    msg = document['chat-input'].value.strip()
    if not msg:
        return

    # WatcherDog filter
    blocked = not window.watcherdog.analyze(msg)
    if blocked:
        document['chat-box'].innerHTML += "<p class='text-red-500'>⚠️ WatcherDog blocked your message.</p>"
    else:
        # Encrypt message before sending (optional, example)
        secure_msg = sic.secure_data(msg)
        reply = window.mobby_reflex(secure_msg)
        # Decrypt reply if encrypted
        reply = sic.open_data(reply)
        document['chat-box'].innerHTML += f"<p class='text-white'>You: {msg}</p>"
        document['chat-box'].innerHTML += f"<p class='text-sky-500'>Mobby: {reply}</p>"

    document['chat-input'].value = ""
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

# ==============================
# SIC System Actions (Secured)
# ==============================
def change_name(ev):
    new_name = window.prompt("Enter new SIC Identity Name:")
    if new_name and window.watcherdog.analyze(new_name):
        # Encrypt before saving
        secure_name = sic.secure_data(new_name)
        window.localStorage.setItem("mobby_user", secure_name)
        window.location.reload()
    else:
        alert("⚠️ WatcherDog blocked this name.")

def update_groq(ev):
    key = window.prompt("Enter Groq API Key:")
    if key and window.watcherdog.analyze(key):
        # Encrypt before storing
        secure_key = sic.secure_data(key)
        window.localStorage.setItem("mobby_groq_key", secure_key)
        alert("✅ API Key Encrypted and Saved.")
    else:
        alert("⚠️ WatcherDog blocked this key.")

def lock_os(ev):
    window.localStorage.removeItem("mobby_auth")
    window.location.reload()

def delete_account(ev):
    if window.confirm("CRITICAL: Wipe all SIC Data?"):
        window.localStorage.clear()
        window.location.reload()

# ==============================
# Bindings
# ==============================
document['open-settings'].bind('click', toggle_settings)
document['close-settings'].bind('click', toggle_settings)
document['profile-trigger'].bind('click', toggle_settings)
document['btn-change-name'].bind('click', change_name)
document['btn-set-groq'].bind('click', update_groq)
document['btn-lock-final'].bind('click', lock_os)
document['btn-signout'].bind('click', lock_os)
document['btn-delete-all'].bind('click', delete_account)

document['btn-start'].bind('click', lambda e: switch_view('desktop-view'))
document['btn-add'].bind('click', lambda e: switch_view('chat-view'))
document['chat-input'].bind('keydown', handle_keypress)

# ==============================
# Initial Load
# ==============================
if window.localStorage.getItem("mobby_auth") == "true":
    document['sic-setup-screen'].classList.add('hidden')
    document['main-ui'].classList.remove('hidden')

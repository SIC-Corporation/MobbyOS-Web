from browser import document, window, alert
import SICHelper

sic = SICHelper.SICHandshake("SIC_MASTER_KEY_2026")

def safe_bind(el_id, event, func):
    try:
        document[el_id].bind(event, func)
    except KeyError:
        pass  # element might not exist yet

# Toggle settings panel
def toggle_settings(ev):
    try:
        document['settings-panel'].classList.toggle('open')
    except KeyError:
        pass

def switch_view(view):
    for v in ['desktop-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view].classList.remove('hidden')
    if view == 'chat-view':
        document['btn-add'].classList.add('hidden')
    else:
        document['btn-add'].classList.remove('hidden')

def handle_keypress(ev):
    if ev.keyCode == 13 and not ev.shiftKey:
        ev.preventDefault()
        send_chat_message()

def send_chat_message():
    msg = document['chat-input'].value.strip()
    if not msg: return

    blocked = not window.watcherdog.analyze(msg)
    if blocked:
        document['chat-box'].innerHTML += "<p class='text-red-500'>⚠️ WatcherDog blocked your message.</p>"
    else:
        secure_msg = sic.secure_data(msg)
        reply = window.mobby_reflex(secure_msg)
        reply = sic.open_data(reply)
        document['chat-box'].innerHTML += f"<p class='text-white'>You: {msg}</p>"
        document['chat-box'].innerHTML += f"<p class='text-sky-500'>Mobby: {reply}</p>"

    document['chat-input'].value = ""
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

# SIC System actions
def change_name(ev):
    new_name = window.prompt("Enter new SIC Identity Name:")
    if new_name and window.watcherdog.analyze(new_name):
        secure_name = sic.secure_data(new_name)
        window.localStorage.setItem("mobby_user", secure_name)
        window.location.reload()
    else:
        alert("⚠️ WatcherDog blocked this name.")

def update_groq(ev):
    key = window.prompt("Enter Groq API Key:")
    if key and window.watcherdog.analyze(key):
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

# BIND BUTTONS SAFELY
safe_bind('open-settings', 'click', toggle_settings)
safe_bind('close-settings', 'click', toggle_settings)
safe_bind('profile-trigger', 'click', toggle_settings)
safe_bind('btn-change-name', 'click', change_name)
safe_bind('btn-set-groq', 'click', update_groq)
safe_bind('btn-lock-final', 'click', lock_os)
safe_bind('btn-signout', 'click', lock_os)
safe_bind('btn-delete-all', 'click', delete_account)
safe_bind('btn-start', 'click', lambda e: switch_view('desktop-view'))
safe_bind('btn-add', 'click', lambda e: switch_view('chat-view'))
safe_bind('chat-input', 'keydown', handle_keypress)

# Initial Load
if window.localStorage.getItem("mobby_auth") == "true":
    document['sic-setup-screen'].classList.add('hidden')
    document['main-ui'].classList.remove('hidden')

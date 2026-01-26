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
        try: document[v].classList.add('hidden')
        except KeyError: pass
    try: document[view].classList.remove('hidden')
    except KeyError: pass
    try:
        if view == 'chat-view':
            document['btn-add'].classList.add('hidden')
        else:
            document['btn-add'].classList.remove('hidden')
    except KeyError: pass

def handle_keypress(ev):
    if ev.keyCode == 13 and not ev.shiftKey:
        ev.preventDefault()
        send_chat_message()

def send_chat_message():
    try:
        msg = document['chat-input'].value.strip()
        if not msg: return
    except KeyError:
        return

    blocked = not getattr(window.watcherdog, "analyze", lambda x: True)(msg)
    chat_box = document.get('chat-box')
    if blocked:
        if chat_box: chat_box.innerHTML += "<p class='text-red-500'>⚠️ WatcherDog blocked your message.</p>"
    else:
        secure_msg = sic.secure_data(msg)
        reply = getattr(window, "mobby_reflex", lambda x: "No reply")(secure_msg)
        reply = sic.open_data(reply)
        if chat_box:
            chat_box.innerHTML += f"<p class='text-white'>You: {msg}</p>"
            chat_box.innerHTML += f"<p class='text-sky-500'>Mobby: {reply}</p>"

    try: document['chat-input'].value = ""
    except KeyError: pass
    if chat_box: chat_box.scrollTop = chat_box.scrollHeight

# SIC System actions
def change_name(ev):
    new_name = window.prompt("Enter new SIC Identity Name:")
    if new_name and getattr(window.watcherdog, "analyze", lambda x: True)(new_name):
        secure_name = sic.secure_data(new_name)
        window.localStorage.setItem("mobby_user", secure_name)
        window.location.reload()
    else:
        alert("⚠️ WatcherDog blocked this name.")

def update_groq(ev):
    key = window.prompt("Enter Groq API Key:")
    if key and getattr(window.watcherdog, "analyze", lambda x: True)(key):
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
for el, event, func in [
    ('open-settings','click',toggle_settings),
    ('close-settings','click',toggle_settings),
    ('profile-trigger','click',toggle_settings),
    ('btn-change-name','click',change_name),
    ('btn-set-groq','click',update_groq),
    ('btn-lock-final','click',lock_os),
    ('btn-signout','click',lock_os),
    ('btn-delete-all','click',delete_account),
    ('btn-start','click',lambda e: switch_view('desktop-view')),
    ('btn-add','click',lambda e: switch_view('chat-view')),
    ('chat-input','keydown',handle_keypress)
]:
    safe_bind(el, event, func)

# --- Initial Load safely ---
mobby_auth = window.localStorage.getItem("mobby_auth")
if mobby_auth and mobby_auth.lower() == "true":
    try:
        document['sic-setup-screen'].classList.add('hidden')
        document['main-ui'].classList.remove('hidden')
    except KeyError:
        pass

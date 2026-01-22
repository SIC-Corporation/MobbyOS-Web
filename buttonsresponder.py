from browser import document, window

def toggle_settings(ev):
    document['settings-panel'].classList.toggle('open')

def switch_view(view):
    document['desktop-view'].classList.add('hidden')
    document['chat-view'].classList.add('hidden')
    document[view].classList.remove('hidden')
    # Toggle the PLUS button visibility
    if view == 'chat-view':
        document['btn-add'].classList.add('hidden')
    else:
        document['btn-add'].classList.remove('hidden')

def handle_keypress(ev):
    """
    Logic:
    Enter -> Send Message
    Shift + Enter -> Allow default (New Line)
    """
    if ev.keyCode == 13: # Enter key
        if not ev.shiftKey:
            ev.preventDefault()
            # Call the send function from engine.py
            window.send_message()

def lock_system(ev):
    window.localStorage.clear()
    window.location.reload()

# Bindings
document['open-settings'].bind('click', toggle_settings)
document['close-settings'].bind('click', toggle_settings)
document['profile-trigger'].bind('click', toggle_settings)
document['btn-lock-final'].bind('click', lock_system)
document['btn-signout'].bind('click', lock_system)

document['btn-start'].bind('click', lambda e: switch_view('desktop-view'))
document['btn-add'].bind('click', lambda e: switch_view('chat-view'))

# Keyboard binding for the input
document['chat-input'].bind('keydown', handle_keypress)

# Initialization
if window.localStorage.getItem("mobby_auth") == "true":
    document['login-screen'].classList.add('hidden')

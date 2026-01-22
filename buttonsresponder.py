from browser import document, window, alert

def handle_manual_auth(ev):
    email = document['auth-email'].value
    password = document['auth-pass'].value
    
    if email and password:
        # Standard manual entry logic
        window.localStorage.setItem("mobby_email", email)
        window.localStorage.setItem("mobby_user", email.split('@')[0])
        window.localStorage.setItem("mobby_auth", "true")
        document['login-screen'].classList.add('hidden')
        document['mode-screen'].classList.remove('hidden')
    else:
        alert("SIC System: Credentials needed to proceed.")

def set_mode(mode_name):
    window.localStorage.setItem("mobby_mode", mode_name)
    window.location.reload()

def lock_os(ev):
    # Total system wipe of local session
    window.localStorage.clear()
    window.location.reload()

def switch_view(view):
    document['desktop-view'].classList.add('hidden')
    document['chat-view'].classList.add('hidden')
    document[view].classList.remove('hidden')

# Bindings
document['btn-auth-submit'].bind('click', handle_manual_auth)
document['mode-adult'].bind('click', lambda e: set_mode('Adult'))
document['mode-kid'].bind('click', lambda e: set_mode('Kid'))
document['mode-guest'].bind('click', lambda e: set_mode('Guest'))
document['btn-lock'].bind('click', lock_os)
document['btn-start'].bind('click', lambda e: switch_view('desktop-view'))
document['btn-add'].bind('click', lambda e: switch_view('chat-view'))

# Check state on load
if window.localStorage.getItem("mobby_auth") == "true":
    document['login-screen'].classList.add('hidden')
    if not window.localStorage.getItem("mobby_mode"):
        document['mode-screen'].classList.remove('hidden')

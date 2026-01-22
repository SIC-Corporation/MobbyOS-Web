from browser import document, window, alert

def handle_manual_auth(ev):
    email = document['auth-email'].value
    password = document['auth-pass'].value
    
    if email and password:
        window.localStorage.setItem("mobby_email", email)
        window.localStorage.setItem("mobby_user", email.split('@')[0])
        window.localStorage.setItem("mobby_auth", "true")
        document['login-screen'].classList.add('hidden')
        document['mode-screen'].classList.remove('hidden')
    else:
        alert("SIC Security: Credentials Required.")

def select_mode(mode):
    window.localStorage.setItem("mobby_mode", mode)
    window.location.reload()

def lock_system(ev):
    window.localStorage.clear()
    window.location.reload()

def toggle_view(view_id):
    for v in ['desktop-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')

# Bindings
document['btn-auth-submit'].bind('click', handle_manual_auth)
document['mode-adult'].bind('click', lambda e: select_mode('Adult'))
document['mode-kid'].bind('click', lambda e: select_mode('Kid'))
document['mode-guest'].bind('click', lambda e: select_mode('Guest'))
document['btn-lock'].bind('click', lock_system)
document['btn-start'].bind('click', lambda e: toggle_view('desktop-view'))
document['btn-add'].bind('click', lambda e: toggle_view('chat-view'))

# Startup Logic
if window.localStorage.getItem("mobby_auth") == "true" and window.localStorage.getItem("mobby_mode"):
    document['login-screen'].classList.add('hidden')
    document['mode-screen'].classList.add('hidden')
elif window.localStorage.getItem("mobby_auth") == "true":
    document['login-screen'].classList.add('hidden')
    document['mode-screen'].classList.remove('hidden')

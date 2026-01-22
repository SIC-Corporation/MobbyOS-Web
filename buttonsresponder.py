from browser import document, window, alert

def handle_google_login(response):
    # This is called by the Google Script in index.html
    window.localStorage.setItem("mobby_auth", "true")
    document['login-screen'].classList.add('hidden')
    alert("Google Identity Verified. Welcome to SIC Corp.")

window.handleGoogleLogin = handle_google_login

def set_mode(mode_type):
    window.localStorage.setItem("mobby_mode", mode_type)
    document['mode-indicator'].text = f"{mode_type.upper()} MODE"
    alert(f"System switched to {mode_type} Mode.")

def toggle_view(view_id):
    for v in ['desktop-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')
    document[view_id].classList.add('view-fade')

# Bindings
document['btn-start'].bind('click', lambda e: toggle_view('desktop-view'))
document['btn-add'].bind('click', lambda e: toggle_view('chat-view'))
document['btn-config'].bind('click', lambda e: document['configModal'].classList.remove('hidden'))
document['closeConfig'].bind('click', lambda e: document['configModal'].classList.add('hidden'))
document['set-kidmode'].bind('click', lambda e: set_mode("kid"))
document['set-adultmode'].bind('click', lambda e: set_mode("adult"))
document['btn-auth-submit'].bind('click', lambda e: document['login-screen'].classList.add('hidden'))

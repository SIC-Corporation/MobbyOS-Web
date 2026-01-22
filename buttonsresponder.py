from browser import document, window, alert

def handle_auth(ev):
    name = document['auth-name'].value
    if name:
        # Save to Browser Storage
        window.localStorage.setItem("mobby_user", name)
        window.localStorage.setItem("mobby_auth", "true")
        
        # Update UI
        document['sideName'].text = name
        document['sidePFP'].src = f"https://ui-avatars.com/api/?name={name}&background=38bdf8&color=fff"
        document['login-screen'].classList.add('hidden')
    else:
        alert("Please enter a name for the SIC Registry.")

def toggle_view(view_id):
    for v in ['desktop-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')

# Bindings
document['btn-auth-submit'].bind('click', handle_auth)
document['btn-start'].bind('click', lambda e: toggle_view('desktop-view'))
document['btn-add'].bind('click', lambda e: toggle_view('chat-view'))

# Check if already logged in on boot
if window.localStorage.getItem("mobby_auth") == "true":
    document['login-screen'].classList.add('hidden')
    document['sideName'].text = window.localStorage.getItem("mobby_user")

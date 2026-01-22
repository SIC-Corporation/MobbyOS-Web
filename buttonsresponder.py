from browser import document, window, alert

def toggle_view(view_id):
    for v in ['desktop-view', 'dashboard-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')
    # Toggle + button
    if view_id == 'chat-view':
        document['btn-add'].classList.add('hide-node')
    else:
        document['btn-add'].classList.remove('hide-node')

def handle_auth(ev):
    # Simple login logic for Roy
    email = document['auth-email'].value
    if "@" in email:
        document['login-screen'].style.display = 'none'
    else:
        alert("Enter a valid SIC Corp Email")

def switch_tab(ev):
    target = ev.target.getAttribute('data-tab')
    # Hide all contents
    for content in document.select('.tab-content'):
        content.classList.add('hidden')
    document[target].classList.remove('hidden')
    # Update buttons
    for btn in document.select('.tab-btn'):
        btn.classList.remove('active')
    ev.target.classList.add('active')

# --- Global Mappings ---
document['btn-start'].bind('click', lambda e: toggle_view('desktop-view'))
document['btn-dashboard'].bind('click', lambda e: toggle_view('dashboard-view'))
document['btn-config'].bind('click', lambda e: document['configModal'].classList.remove('hidden'))
document['closeConfig'].bind('click', lambda e: document['configModal'].classList.add('hidden'))
document['btn-auth-submit'].bind('click', handle_auth)
document['btn-forgot'].bind('click', lambda e: alert("Recovery link sent to SIC email server."))

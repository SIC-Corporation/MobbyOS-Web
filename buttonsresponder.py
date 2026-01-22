from browser import document, window, alert

def toggle_view(view_id):
    # Instant hide/show for performance
    for v in ['desktop-view', 'dashboard-view', 'chat-view']:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')
    
    # Show/Hide the floating + button
    if view_id == 'chat-view':
        document['btn-add'].classList.add('hidden')
    else:
        document['btn-add'].classList.remove('hidden')

def handle_auth(ev):
    email = document['auth-email'].value
    if "@" in email:
        document['login-screen'].classList.add('hidden')
    else:
        alert("Authorization Failed: Invalid SIC Email.")

def switch_tab(ev):
    target_id = ev.target.getAttribute('data-tab')
    # Switch tab buttons
    for btn in document.select('.tab-btn'):
        btn.classList.remove('active')
    ev.target.classList.add('active')
    
    # Switch tab content
    for content in document.select('.tab-content'):
        content.classList.add('hidden')
    document[target_id].classList.remove('hidden')

# Bindings
document['btn-start'].bind('click', lambda e: toggle_view('desktop-view'))
document['btn-dashboard'].bind('click', lambda e: toggle_view('dashboard-view'))
document['btn-config'].bind('click', lambda e: document['configModal'].classList.remove('hidden'))
document['closeConfig'].bind('click', lambda e: document['configModal'].classList.add('hidden'))
document['btn-auth-submit'].bind('click', handle_auth)
document['btn-forgot'].bind('click', lambda e: alert("Access Reset Request sent to Roy."))

# Bind Tab switching
for btn in document.select('.tab-btn'):
    btn.bind('click', switch_tab)

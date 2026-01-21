from browser import document, window, timer, datetime

# Global State
history_data = ["Neural Link Ready"]

def calculate_age(birth_date_str):
    """Calculates age from YYYY-MM-DD string"""
    bday = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = datetime.datetime.now()
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))

def toggle_view(view_name):
    """Switches between Desktop and Chat"""
    if view_name == "chat":
        document["desktop-view"].classList.add("hidden")
        document["chat-view"].classList.remove("hidden")
    else:
        document["chat-view"].classList.add("hidden")
        document["desktop-view"].classList.remove("hidden")

def handle_age_verification(ev):
    bday_val = document["user-bday"].value
    if not bday_val: return
    
    age = calculate_age(bday_val)
    window.localStorage.setItem("mobby_bday", bday_val)
    
    if age < 14:
        document["setup-step-1"].classList.add("hidden")
        document["setup-step-child"].classList.remove("hidden")
    else:
        window.localStorage.setItem("mobby_age_type", "adult")
        window.location.reload()

def finish_child_setup(ev):
    p_email = document["parent-email"].value
    if p_email:
        window.localStorage.setItem("mobby_parent", p_email)
        window.localStorage.setItem("mobby_age_type", "child")
        window.location.reload()

def groq_upload_simulation(ev):
    """Simulates Groq processing for settings/setup updates"""
    btn = ev.target
    original_text = btn.text
    btn.text = "GROQ PROCESSING..."
    
    def complete():
        btn.text = "UPLOAD COMPLETE"
        timer.set_timeout(lambda: window.location.reload(), 1000)
        
    # Simulate a 1.5s delay for 'Groq processing'
    timer.set_timeout(complete, 1500)

def init():
    user = window.localStorage.getItem("mobby_user")
    age_type = window.localStorage.getItem("mobby_age_type")
    
    # Update Sidebar with the real name
    if user:
        document["sideName"].text = user
        document["userRole"].text = f"{age_type.upper()} NODE"
    
    # Event Listeners
    document["verify-age"].bind("click", handle_age_verification)
    document["finish-child-setup"].bind("click", finish_child_setup)
    document["save-settings"].bind("click", groq_upload_simulation)
    
    # The "+" button now redirects to chat
    document["btn-add"].bind("click", lambda e: toggle_view("chat"))

init()

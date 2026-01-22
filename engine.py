from browser import document, window, timer, alert
import datetime

# --- STATE ---
history_data = ["System Boot", "V2.0 Loaded"]
start_time = datetime.datetime.now()
msg_count = 0

# --- UTILS ---
def update_stats():
    # Update Uptime
    now = datetime.datetime.now()
    diff = now - start_time
    minutes = int(diff.total_seconds() / 60)
    if "stat-uptime" in document:
        document["stat-uptime"].text = f"{minutes}m"
    if "stat-msgs" in document:
        document["stat-msgs"].text = str(msg_count)

# Start stats timer (every 10s)
timer.set_interval(update_stats, 10000)

def render_history():
    if "history-list" not in document: return
    container = document["history-list"]
    container.html = ""
    for i, item in enumerate(history_data):
        div = document.createElement('div')
        active_class = "active" if i == 0 else ""
        div.class_name = f"history-item p-3 rounded-lg text-[9px] font-black uppercase text-white/40 cursor-pointer truncate {active_class}"
        div.text = f"> {item}"
        container <= div

# --- AUTH & SETUP ---
def handle_login(ev):
    user_val = document["auth-user"].value
    pass_val = document["auth-pass"].value
    
    if not user_val:
        document["auth-user"].style.border = "1px solid red"
        return

    stored_pass = window.localStorage.getItem("mobby_pass")
    
    # Logic: If password exists, check it. If not, this is first setup/registration.
    if stored_pass and stored_pass != pass_val:
        alert("ACCESS DENIED: Invalid Password")
        return

    # Success
    window.localStorage.setItem("mobby_user", user_val)
    if not stored_pass and pass_val:
        window.localStorage.setItem("mobby_pass", pass_val) # Set pass on first login if typed
        
    window.location.reload()

def handle_age_verify(ev):
    bday_val = document["user-bday"].value
    if not bday_val: return
    
    try:
        y, m, d = map(int, bday_val.split('-'))
        bday_date = datetime.date(y, m, d)
        today = datetime.date.today()
        age = today.year - bday_date.year - ((today.month, today.day) < (bday_date.month, bday_date.day))
        
        window.localStorage.setItem("mobby_bday", bday_val)
        
        if age < 14:
            document["setup-step-1"].classList.add("hidden")
            document["setup-step-child"].classList.remove("hidden")
        else:
            window.localStorage.setItem("mobby_age_type", "adult")
            window.location.reload()
    except:
        pass

# --- NAVIGATION ---
def switch_view(view_id):
    # Hide all views
    document["desktop-view"].classList.add("hidden")
    document["chat-view"].classList.add("hidden")
    document["dashboard-view"].classList.add("hidden")
    document["btn-add"].classList.remove("hidden")
    
    # Show target
    document[view_id].classList.remove("hidden")
    
    if view_id == "chat-view":
        document["btn-add"].classList.add("hidden")
        history_data.insert(0, "Chat Active")
    elif view_id == "dashboard-view":
        history_data.insert(0, "Viewing Metrics")
        update_stats()
        
    render_history()

# --- SETTINGS TABS ---
def switch_tab(ev):
    # Get the clicked button
    btn = ev.target
    target_id = btn.attrs['data-tab']
    
    # Reset all buttons
    for b in document.select('.tab-btn'):
        b.classList.remove("active")
    
    # Hide all contents
    for c in document.select('.settings-content'):
        c.classList.add("hidden")
        
    # Activate clicked
    btn.classList.add("active")
    document[target_id].classList.remove("hidden")

def save_profile(ev):
    val = document["set-username"].value
    if val:
        window.localStorage.setItem("mobby_user", val)
        ev.target.text = "Saved!"
        timer.set_timeout(lambda: window.location.reload(), 500)

def save_security(ev):
    val = document["set-password"].value
    if val:
        window.localStorage.setItem("mobby_pass", val)
        ev.target.text = "Password Updated"
        timer.set_timeout(lambda: setattr(ev.target, 'text', 'UPDATE PASSWORD'), 2000)

def save_cloud(ev):
    val = document["set-apikey"].value
    if val:
        window.localStorage.setItem("mobby_apikey", val)
        ev.target.text = "Key Securely Stored"

def delete_account(ev):
    if window.confirm("WARNING: This will wipe all SIC Corp data. Continue?"):
        window.localStorage.clear()
        window.location.reload()

# --- CHAT ---
def send_chat(ev):
    global msg_count
    user_inp = document["chat-input"].value
    if not user_inp: return
    
    msg_count += 1
    chat = document["chat-box"]
    
    # User
    u = document.createElement('div')
    u.class_name = "text-right"
    u.html = f"<span class='bg-sky-500 text-black font-bold p-3 rounded-xl inline-block text-xs'>{user_inp}</span>"
    chat <= u
    document["chat-input"].value = ""
    chat.scrollTop = chat.scrollHeight
    
    # Bot
    def reply():
        b = document.createElement('div')
        b.class_name = "text-left"
        b.html = f"<span class='text-sky-500 font-federo text-xs block mb-1'>MOBBY</span><span class='text-white/80 p-3 bg-white/5 rounded-xl inline-block text-xs'>Processed: {user_inp}</span>"
        chat <= b
        chat.scrollTop = chat.scrollHeight
    timer.set_timeout(reply, 600)

# --- BINDINGS ---
def bind(id, func):
    if id in document: document[id].bind("click", func)

def init():
    # Auth
    bind("auth-btn", handle_login)
    bind("verify-age", handle_age_verify)
    bind("finish-child-setup", lambda e: (window.localStorage.setItem("mobby_age_type", "child"), window.location.reload()))
    
    # Nav
    bind("btn-add", lambda e: switch_view("chat-view"))
    bind("btn-dashboard", lambda e: switch_view("dashboard-view"))
    
    # Settings Modal
    bind("btn-config", lambda e: document["configModal"].classList.remove("hidden"))
    bind("closeConfig", lambda e: document["configModal"].classList.add("hidden"))
    bind("logoutBtn", lambda e: (window.localStorage.clear(), window.location.reload()))
    
    # Settings Forms
    bind("save-profile", save_profile)
    bind("save-security", save_security)
    bind("save-cloud", save_cloud)
    bind("delete-account", delete_account)
    
    # Tabs
    for btn in document.select('.tab-btn'):
        btn.bind("click", switch_tab)
        
    # Chat
    bind("send-chat", send_chat)
    
    # Load User Data
    user = window.localStorage.getItem("mobby_user")
    age = window.localStorage.getItem("mobby_age_type")
    
    if user:
        if "sideName" in document: document["sideName"].text = user
        if "welcomeMsg" in document: 
             # Typewriter effect
            txt = f"Welcome, {user}"
            target = document["welcomeMsg"]
            def type(i):
                if i < len(txt):
                    target.text += txt[i]
                    timer.set_timeout(lambda: type(i+1), 50)
            type(0)
            
        if age == "child" and "set-username" in document:
            document["set-username"].disabled = True
            document["set-username"].placeholder = "LOCKED (CHILD SAFETY)"

init()

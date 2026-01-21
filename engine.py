from browser import document, window, timer, alert
import SICHelper

mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")

def run_os():
    try:
        # 1. BIND BUTTONS
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        document["commitBtn"].bind("click", save_settings)
        document["logoutBtn"].bind("click", logout_action)
        document["entryBtn"].bind("click", login_action)
        
        # 2. CHECK SESSION
        current_user = window.localStorage.getItem("mobby_username")
        
        if not current_user:
            document["login-screen"].classList.remove("hidden")
        else:
            start_dashboard(current_user)

        # 3. STATUS UPDATE
        document["mobbyStatus"].text = "Neural Online"
        document["statusDot"].style.backgroundColor = "#22c55e"
        
        timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 500)
        
    except Exception as e:
        print(f"OS Error: {e}")

def start_dashboard(name):
    document["login-screen"].classList.add("hidden")
    document["sideName"].text = name
    animate_text(f"Welcome, {name}")

def animate_text(full_text):
    document["welcomeMsg"].text = ""
    def type_char(index):
        if index <= len(full_text):
            document["welcomeMsg"].text = full_text[:index]
            timer.set_timeout(lambda: type_char(index + 1), 50)
    type_char(0)

def login_action(ev):
    name = document["loginUser"].value
    if name:
        window.localStorage.setItem("mobby_username", name)
        start_dashboard(name)

def save_settings(ev):
    new_name = document["cfgName"].value
    if new_name:
        window.localStorage.setItem("mobby_username", new_name)
        document["sideName"].text = new_name
        animate_text(f"Hello, {new_name}")
        document["configModal"].classList.add("hidden")

def logout_action(ev):
    window.localStorage.clear()
    window.location.reload()

SICHelper.boot_sequence(run_os)

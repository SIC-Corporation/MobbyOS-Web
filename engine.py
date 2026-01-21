from browser import document, window, timer, alert
import SICHelper

# Initialize the SIC Handshake
mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")

def run_os():
    try:
        # 1. ATTACH BUTTON LOGIC
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        document["commitBtn"].bind("click", save_settings)
        document["logoutBtn"].bind("click", logout_action)
        
        # 2. UI STATUS
        document["mobbyStatus"].text = "Neural Online"
        document["statusDot"].style.backgroundColor = "#22c55e"
        
        # 3. RUN WELCOME ANIMATION
        current_user = window.localStorage.getItem("mobby_username") or "User"
        document["sideName"].text = current_user
        animate_text(f"Welcome, {current_user}")

        # 4. KILL BOOT SCREEN
        timer.set_timeout(hide_boot, 500)
        
        print("MobbyOS: Neural Handshake Successful.")
    except Exception as e:
        print(f"Engine Crash: {e}")

def animate_text(full_text):
    """Creates the 'Typing' animation for the welcome message."""
    document["welcomeMsg"].text = ""
    def type_char(index):
        if index <= len(full_text):
            document["welcomeMsg"].text = full_text[:index]
            timer.set_timeout(lambda: type_char(index + 1), 50)
    type_char(0)

def save_settings(ev):
    new_name = document["cfgName"].value
    if new_name:
        window.localStorage.setItem("mobby_username", new_name)
        document["sideName"].text = new_name
        animate_text(f"Hello, {new_name}")
        document["configModal"].classList.add("hidden")
        alert("Profile Updated in Cloud.")

def logout_action(ev):
    if window.confirm("SIC Corp: Terminate session?"):
        window.localStorage.clear()
        window.location.reload()

def hide_boot():
    document["boot-screen"].style.opacity = "0"
    timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 300)

# Start Engine
SICHelper.boot_sequence(run_os)

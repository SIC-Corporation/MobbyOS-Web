from browser import document, window, timer
import SICHelper

def run_os():
    try:
        # Bind UI Elements
        document["btn-config"].bind("click", lambda e: document["configModal"].classList.remove("hidden"))
        document["closeConfig"].bind("click", lambda e: document["configModal"].classList.add("hidden"))
        
        # UI Feedback
        document["mobbyStatus"].text = "Online"
        document["statusDot"].style.backgroundColor = "#22c55e"
        
        # Kill Boot Screen (Fast)
        timer.set_timeout(lambda: setattr(document["boot-screen"].style, "opacity", "0"), 100)
        timer.set_timeout(lambda: document["boot-screen"].classList.add("hidden"), 400)
        print("MobbyOS Engine: Handshake Complete.")
    except Exception as e:
        print(f"UI Error: {e}")

# The Startup Sequence
try:
    mobby_link = SICHelper.SICHandshake("Roy_SIC_Corp_2026")
    # Wait for the HTML buttons to exist, then fire run_os
    SICHelper.boot_sequence(run_os)
except Exception as e:
    print(f"Handshake Failed: {e}")

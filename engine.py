from browser import document, window, html, timer
import json
import SICHelper # Handshake initialized

# --- INITIALIZE SIC HANDSHAKE ---
# Using a static master key for SIC Corp internal protocols
handshake = SICHelper.SICHandshake("SIC_CORP_MASTER_2026")

class MobbyState:
    is_chat_open = False
    messages_sent = 0

state = MobbyState()

# --- UI LOGIC ---
def type_text(element, text, delay=30):
    element.html = ""
    def _type(i):
        if i < len(text):
            element.html += text[i]
            timer.set_timeout(lambda: _type(i + 1), delay)
    _type(0)

def update_identity():
    """Syncs the user name from storage with SIC decryption"""
    raw_name = window.localStorage.getItem("mobby_username")
    # Decrypt if it's a SIC-secured string, otherwise use guest
    display_name = handshake.open_data(raw_name) if raw_name else "OPERATOR"
    
    document['user-display-name'].text = display_name
    document['sideName'].text = display_name

def show_view(view_id):
    views = ['desktop-view', 'dashboard-view', 'chat-view']
    for v in views:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')
    
    # Show the + button only on Home or Dashboard
    if view_id == 'chat-view':
        document['btn-add'].classList.add('hide-node')
    else:
        document['btn-add'].classList.remove('hide-node')

# --- BUTTON ACTIONS ---
def open_nexus(ev):
    state.is_chat_open = True
    show_view('chat-view')
    
    # Welcome sequence
    document['chat-box'].html = "" # Clear previous
    welcome_msg = "NEURAL LINK ESTABLISHED. HOW CAN I ASSIST, OPERATOR?"
    msg_div = html.DIV(className="text-sky-400 font-bold text-sm mb-4")
    document['chat-box'] <= msg_div
    type_text(msg_div, welcome_msg)

def send_message(ev=None):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
        
    document['chat-box'] <= html.DIV(f"USER: {user_input}", className="text-white/50 text-xs mb-2 pl-4 border-l border-white/10")
    document['chat-input'].value = ""
    
    state.messages_sent += 1
    document['stat-msgs'].text = str(state.messages_sent)
    
    reflex_response = window.mobby_reflex(user_input)
    response_div = html.DIV(className="text-sky-500 font-bold mb-6")
    document['chat-box'] <= response_div
    
    if reflex_response:
        type_text(response_div, f"MOBBY: {reflex_response}")
    else:
        type_text(response_div, "MOBBY: [CLOUD UPLINK PENDING... CHECK API KEY]")

# --- BINDINGS ---
def init_os():
    update_identity()
    document['btn-add'].bind('click', open_nexus)
    document['send-chat'].bind('click', send_message)
    document['btn-start'].bind('click', lambda e: show_view('desktop-view'))
    document['btn-dashboard'].bind('click', lambda e: show_view('dashboard-view'))
    document['btn-config'].bind('click', lambda e: document['configModal'].classList.remove('hidden'))
    document['closeConfig'].bind('click', lambda e: document['configModal'].classList.add('hidden'))

# Start the boot sequence via SICHelper logic
SICHelper.boot_sequence(init_os)

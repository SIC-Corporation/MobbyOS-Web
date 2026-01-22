from browser import document, window, html, timer
import json

# --- STATE MANAGEMENT ---
class MobbyState:
    is_chat_open = False
    messages_sent = 0

state = MobbyState()

# --- UI ANIMATIONS ---
def type_text(element, text, delay=30):
    """Creates a futuristic typing effect for Mobby's text."""
    element.html = ""
    def _type(i):
        if i < len(text):
            element.html += text[i]
            timer.set_timeout(lambda: _type(i + 1), delay)
    _type(0)

def show_view(view_id):
    """Switches between Desktop, Dashboard, and Chat."""
    views = ['desktop-view', 'dashboard-view', 'chat-view']
    for v in views:
        document[v].classList.add('hidden')
    document[view_id].classList.remove('hidden')

# --- CORE FUNCTIONS ---
def open_nexus(ev):
    """Triggered by the '+' button"""
    state.is_chat_open = True
    document['btn-add'].classList.add('hidden') # Auto-hide the button
    show_view('chat-view')
    
    # Welcoming Animation
    welcome_msg = "NEURAL LINK ESTABLISHED. HOW CAN I ASSIST, OPERATOR?"
    msg_div = html.DIV(className="text-sky-400 font-bold text-sm mb-4")
    document['chat-box'] <= msg_div
    type_text(msg_div, welcome_msg)

def send_message(ev=None):
    user_input = document['chat-input'].value.strip()
    if not user_input:
        return
        
    # Append User Message
    document['chat-box'] <= html.DIV(f"USER: {user_input}", className="text-white/50 text-xs mb-2 pl-4 border-l border-white/10")
    document['chat-input'].value = ""
    
    # 1. Check for "Reflex" (Local Bot Responses)
    reflex_response = window.mobby_reflex(user_input)
    
    # 2. Display Response with Animation
    response_div = html.DIV(className="text-sky-500 font-bold mb-6")
    document['chat-box'] <= response_div
    
    if reflex_response:
        type_text(response_div, f"MOBBY: {reflex_response}")
    else:
        # Fallback to Groq (Logic to be wrapped in try/except to prevent the red error)
        type_text(response_div, "MOBBY: [CLOUD UPLINK PENDING... CHECK API KEY]")

# --- BINDINGS ---
document['btn-add'].bind('click', open_nexus)
document['send-chat'].bind('click', send_message)
document['btn-dashboard'].bind('click', lambda e: show_view('dashboard-view'))

# Initialize Dashboard metrics
document['stat-msgs'].text = str(state.messages_sent)

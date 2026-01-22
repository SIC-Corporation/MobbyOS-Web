from browser import document, window, html, timer

def type_text(element, text):
    element.html = ""
    def _type(i):
        if i < len(text):
            element.html += text[i]
            timer.set_timeout(lambda: _type(i + 1), 20)
    _type(0)

def send_to_mobby(ev):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    
    # Append User Message
    document['chat-box'] <= html.DIV(f"USER: {user_input}", className="text-white/20 text-[10px] mb-2 pl-4 border-l border-white/5 font-inter")
    document['chat-input'].value = ""
    
    # Response Container
    res_div = html.DIV(className="text-sky-500 font-bold mb-6 text-sm")
    document['chat-box'] <= res_div
    
    # Check the Neural Bridge (botinitials.py)
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(user_input)
        if reply:
            type_text(res_div, f"MOBBY: {reply}")
        else:
            type_text(res_div, "MOBBY: No local reflex found. Connect Groq Key for deep reasoning.")
    else:
        res_div.text = "MOBBY: UPLINK ERROR - BRIDGE NOT FOUND."

def update_profile(ev):
    name = document['set-username'].value
    if name:
        document['user-display-name'].text = name
        document['sideName'].text = name
        window.localStorage.setItem("mobby_user", name)
        alert("ID confirmed.")

# Global Bindings
document['send-chat'].bind('click', send_to_mobby)
document['save-profile'].bind('click', update_profile)
document['btn-add'].bind('click', lambda e: toggle_view('chat-view'))

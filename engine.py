from browser import document, window, html, timer

def create_bubble(name, text, pfp, is_user=True):
    user_class = "msg-user" if is_user else ""
    bubble_class = "bubble-user" if is_user else "bubble-bot"
    
    container = html.DIV(className=f"msg-container {user_class}")
    img = html.IMG(src=pfp, className="w-10 h-10 rounded-full border border-white/10 shadow-sm")
    
    msg_body = html.DIV(className="flex flex-col")
    msg_body <= html.SPAN(name, className="text-[9px] uppercase opacity-40 mb-1 px-2")
    msg_body <= html.DIV(text, className=f"bubble {bubble_class}")
    
    container <= img
    container <= msg_body
    
    document['chat-box'] <= container
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

def send_message(ev=None):
    # This function handles both the click and the Enter key
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    
    # Get stored data or defaults
    name = window.localStorage.getItem("mobby_user") or "Roy"
    pfp = window.localStorage.getItem("mobby_pfp") or f"https://ui-avatars.com/api/?name={name}&background=38bdf8&color=fff"
    
    create_bubble(name, user_input, pfp, True)
    document['chat-input'].value = ""
    
    # Bot Response Trigger
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(user_input)
        if reply:
            timer.set_timeout(lambda: create_bubble("MOBBY", reply, "https://i.imgur.com/r6oJp4O.png", False), 600)

def key_handler(ev):
    if ev.keyCode == 13: # 13 is the Enter Key
        send_message()

# Bindings
document['send-chat'].bind('click', send_message)
document['chat-input'].bind('keydown', key_handler)

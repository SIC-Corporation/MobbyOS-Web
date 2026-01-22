from browser import document, window, html, timer

def create_bubble(name, text, pfp, is_user=True):
    # CSS classes must match the <style> in index.html
    user_alignment = "msg-user" if is_user else ""
    bubble_style = "bubble-user" if is_user else "bubble-bot"
    
    # Outer Container
    container = html.DIV(className=f"msg-container {user_alignment}")
    
    # Avatar
    img = html.IMG(src=pfp, className="w-10 h-10 rounded-full border border-white/10 shadow-sm")
    
    # Text Content
    msg_group = html.DIV(className="flex flex-col")
    name_tag = html.SPAN(name, className=f"text-[9px] uppercase opacity-40 mb-1 {'text-right px-2' if is_user else 'px-2'}")
    text_bubble = html.DIV(text, className=f"bubble {bubble_style}")
    
    msg_group <= name_tag
    msg_group <= text_bubble
    
    # Assemble
    container <= img
    container <= msg_group
    
    document['chat-box'] <= container
    
    # Auto-scroll to bottom
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

def send_message(ev=None):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    
    # Data Persistence from LocalStorage (Firefox Friendly)
    name = window.localStorage.getItem("mobby_user") or "Roy"
    pfp = window.localStorage.getItem("mobby_pfp") or f"https://ui-avatars.com/api/?name={name}&background=38bdf8&color=fff"
    
    create_bubble(name, user_input, pfp, True)
    document['chat-input'].value = ""
    
    # Artificial Intelligence Reflex
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(user_input)
        if reply:
            timer.set_timeout(lambda: create_bubble("MOBBY", reply, "https://i.imgur.com/r6oJp4O.png", False), 700)

def key_handler(ev):
    if ev.keyCode == 13: 
        send_message()

# Bindings for controls
document['send-chat'].bind('click', send_message)
document['chat-input'].bind('keydown', key_handler)

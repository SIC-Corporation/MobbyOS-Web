from browser import document, window, html, timer

def create_bubble(name, text, pfp, is_user=True):
    email = window.localStorage.getItem("mobby_email") or ""
    mode = window.localStorage.getItem("mobby_mode") or "Adult"
    
    # ADMIN PROTECTION
    is_admin = email.lower().strip() in ["sicmailcenter1@gmail.com", "roystonslijkerman@gmail.com"]
    
    user_alignment = "msg-user" if is_user else ""
    bubble_style = "bubble-user" if is_user else "bubble-bot"
    
    if is_admin and is_user:
        name = "ADMIN [ROY]"
        bubble_style += " admin-glow"

    container = html.DIV(className=f"msg-container {user_alignment}")
    img = html.IMG(src=pfp, className=f"w-10 h-10 rounded-full border border-white/10 {'border-red-500' if is_admin and is_user else ''}")
    
    msg_group = html.DIV(className="flex flex-col")
    name_tag = html.SPAN(name, className=f"text-[9px] uppercase font-bold mb-1 px-2 {'text-red-500' if is_admin and is_user else 'opacity-40'}")
    text_bubble = html.DIV(text, className=f"bubble {bubble_style}")
    
    msg_group <= name_tag
    msg_group <= text_bubble
    container <= img
    container <= msg_group
    
    document['chat-box'] <= container
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

def send_message(ev=None):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    
    name = window.localStorage.getItem("mobby_user") or "Roy"
    pfp = window.localStorage.getItem("mobby_pfp") or f"https://ui-avatars.com/api/?name={name}&background=38bdf8&color=fff"
    
    create_bubble(name, user_input, pfp, True)
    document['chat-input'].value = ""
    
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(user_input)
        if reply:
            timer.set_timeout(lambda: create_bubble("MOBBY", reply, "https://i.imgur.com/r6oJp4O.png", False), 600)

# Sidebar Update
if window.localStorage.getItem("mobby_auth") == "true":
    name = window.localStorage.getItem("mobby_user")
    email = window.localStorage.getItem("mobby_email") or ""
    mode = window.localStorage.getItem("mobby_mode") or "Adult"
    
    document['sideName'].text = name
    document['sidePFP'].src = window.localStorage.getItem("mobby_pfp") or f"https://ui-avatars.com/api/?name={name}"
    
    indicator = document['mode-indicator']
    indicator.text = f"{mode} Mode"
    if email.lower() in ["sicmailcenter1@gmail.com", "roystonslijkerman@gmail.com"]:
        indicator.text = "MASTER ADMIN"
        indicator.style.color = "#ef4444"

document['send-chat'].bind('click', send_message)

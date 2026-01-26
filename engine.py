from browser import document, window, html, timer
import json

def save_chat_history(role, name, text, pfp):
    history = window.localStorage.getItem("mobby_history")
    history = json.loads(history) if history else []
    history.append({"role": role, "name": name, "text": text, "pfp": pfp})
    window.localStorage.setItem("mobby_history", json.dumps(history))

def load_history():
    history = window.localStorage.getItem("mobby_history")
    if history:
        data = json.loads(history)
        for msg in data:
            create_bubble(msg['name'], msg['text'], msg['pfp'], msg['role']=="user", False)

def create_bubble(name, text, pfp, is_user=True, should_save=True):
    prefs = window.localStorage
    email = prefs.getItem("mobby_email") or ""
    admins = ["sicmailcenter1@gmail.com","roystonslijkerman@gmail.com"]
    is_admin = email.lower().strip() in admins
    
    alignment = "msg-user" if is_user else ""
    style = "bubble-user" if is_user else "bubble-bot"
    if is_admin and is_user: style += " admin-glow"

    container = html.DIV(className=f"msg-container {alignment}")
    img = html.IMG(src=pfp, className=f"w-10 h-10 rounded-full border {'border-red-500' if is_admin and is_user else 'border-white/10'}")
    
    msg_group = html.DIV(className="flex flex-col")
    name_tag = html.SPAN(name,className=f"text-[9px] uppercase mb-1 px-2 {'admin-text' if is_admin and is_user else 'opacity-40'}")
    text_bubble = html.DIV(text,className=f"bubble {style}")

    msg_group <= name_tag
    msg_group <= text_bubble
    container <= img
    container <= msg_group
    document['chat-box'] <= container
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight
    
    if should_save:
        save_chat_history("user" if is_user else "bot", name, text, pfp)

def send_message(ev=None):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    name = window.localStorage.getItem("mobby_user") or "Roy"
    pfp = window.localStorage.getItem("mobby_pfp") or f"https://ui-avatars.com/api/?name={name}"
    create_bubble(name,user_input,pfp,True)
    document['chat-input'].value=""
    # Bot response placeholder
    timer.set_timeout(lambda: create_bubble("MOBBY","System Command Received. Processing...", "https://i.imgur.com/r6oJp4O.png",False), 800)

window.send_message = send_message
load_history()

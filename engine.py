from browser import document, window, html, timer

def create_bubble(name, text, pfp, is_user=True):
    align = "msg-user ml-auto" if is_user else "msg-bot mr-auto"
    bubble = html.DIV(className=f"flex gap-3 max-w-[80%] p-4 rounded-3xl {align}")
    
    img = html.IMG(src=pfp, className="w-8 h-8 rounded-full border border-white/10")
    content = html.DIV()
    content <= html.P(name, className="text-[8px] font-black uppercase text-white/30 mb-1")
    content <= html.P(text, className="text-sm font-inter")
    
    if is_user:
        bubble <= content
        bubble <= img
    else:
        bubble <= img
        bubble <= content
        
    document['chat-box'] <= bubble
    document['chat-box'].scrollTop = document['chat-box'].scrollHeight

def send_to_mobby(ev):
    user_input = document['chat-input'].value.strip()
    if not user_input: return
    
    name = window.localStorage.getItem("mobby_user") or "Guest"
    pfp = window.localStorage.getItem("mobby_pfp") or "https://i.imgur.com/r6oJp4O.png"
    
    # User Message
    create_bubble(name, user_input, pfp, True)
    document['chat-input'].value = ""
    
    # Bot Response
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(user_input)
        if reply:
            timer.set_timeout(lambda: create_bubble("MOBBY", reply, "https://i.imgur.com/r6oJp4O.png", False), 600)

def update_profile(ev):
    name = document['set-username'].value
    pfp = document['set-pfp'].value
    window.localStorage.setItem("mobby_user", name)
    window.localStorage.setItem("mobby_pfp", pfp)
    document['sideName'].text = name
    document['sidePFP'].src = pfp
    alert("Profile Updated.")

document['send-chat'].bind('click', send_to_mobby)
document['save-profile'].bind('click', update_profile)

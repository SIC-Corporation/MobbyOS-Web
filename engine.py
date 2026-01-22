from browser import document, window, html, timer
import SICHelper

handshake = SICHelper.SICHandshake("SIC_CORP_2026")

def type_text(element, text):
    element.html = ""
    def _type(i):
        if i < len(text):
            element.html += text[i]
            timer.set_timeout(lambda: _type(i + 1), 30)
    _type(0)

def save_user_profile(ev):
    name = document['set-username'].value
    encrypted_name = handshake.secure_data(name)
    window.localStorage.setItem("mobby_user", encrypted_name)
    document['user-display-name'].text = name
    document['sideName'].text = name
    alert("Identity Confirmed, Operator.")

def send_to_mobby(ev):
    msg = document['chat-input'].value
    if not msg: return
    document['chat-box'] <= html.DIV(f"USER: {msg}", className="text-white/30 text-xs mb-2")
    document['chat-input'].value = ""
    
    # RESPONSE LOGIC
    res_div = html.DIV(className="text-sky-500 font-bold mb-4")
    document['chat-box'] <= res_div
    
    if hasattr(window, 'mobby_reflex'):
        reply = window.mobby_reflex(msg)
        type_text(res_div, f"MOBBY: {reply}")
    else:
        type_text(res_div, "MOBBY: UPLINK ERROR. CHECK BOTINITIALS.PY")

document['save-profile'].bind('click', save_user_profile)
document['send-chat'].bind('click', send_to_mobby)
document['btn-add'].bind('click', lambda e: document['chat-view'].classList.remove('hidden'))

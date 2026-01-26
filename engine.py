from browser import window, document, alert

def check_browser():
    ua = window.navigator.userAgent.lower()
    return any(b in ua for b in ["chrome", "firefox", "brave", "safari", "edg"])

def initSICAccountSystem():
    if not check_browser():
        alert("Unsafe browser blocked.")
        return

    if window.localStorage.getItem("mobby_auth") == "true":
        document["sic-setup-screen"].classList.add("hidden")
        document["main-ui"].classList.remove("hidden")
    else:
        document["sic-setup-screen"].classList.remove("hidden")
        document["main-ui"].classList.add("hidden")

// ==========================
// WatcherDog JS
// ==========================
const WatcherDog = (() => {
    const allowedBrowsers = ["chrome", "firefox", "brave", "safari", "edg"];
    let alerts = [];

    function checkBrowser() {
        let ua = navigator.userAgent.toLowerCase();
        return allowedBrowsers.some(name => ua.includes(name));
    }

    function checkSystem() {
        // Minimal fingerprint for privacy: OS + Browser
        let os = navigator.platform.toLowerCase();
        let browserSafe = checkBrowser();
        if (!browserSafe) alerts.push("Unsafe browser detected: " + navigator.userAgent);
        if (os.includes("win")) return true; // Example
        return true; // Basic check
    }

    function sendAlert(message) {
        alerts.push(message);
        const alertBox = document.getElementById("wd-alert");
        const msg = document.getElementById("wd-message");
        msg.textContent = message;
        alertBox.classList.remove("hidden");
    }

    function dismiss() {
        document.getElementById("wd-alert").classList.add("hidden");
        alerts = [];
    }

    function runChecks(msgFromPython) {
        if (!checkSystem()) sendAlert("System integrity check failed!");
        if (msgFromPython) sendAlert(msgFromPython);
    }

    return {
        initHTML: () => {
            if (!checkBrowser()) sendAlert("🚨 Browser not supported!");
        },
        runChecks,
        dismiss
    };
})();

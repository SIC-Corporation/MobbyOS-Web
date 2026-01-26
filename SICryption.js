// ==========================
// SICryption Browser Guard
// ==========================
const allowedBrowsers = ["chrome", "firefox", "brave", "safari", "edg"];
let userAgent = navigator.userAgent.toLowerCase();
let safe = allowedBrowsers.some(name => userAgent.includes(name));

if (!safe) {
    alert("🚨 Unrecognized or unsafe browser detected! MobbyOS blocked the session.");
    document.body.innerHTML = "<h1 class='text-center text-red-500 mt-20'>ACCESS DENIED</h1>";
    throw new Error("Unsafe browser. Access blocked.");
}

// ==========================
// JS Threat Protection
// ==========================
function runJSProtections(message) {
    // Basic regex checks
    const threatPatterns = [/script/i, /<.*>/, /eval/i, /fetch\(.*\)/i, /window.location/i];
    for (let pattern of threatPatterns) {
        if (pattern.test(message)) return false;
    }
    return true;
}

// ==========================
// WatcherDog Integration
// ==========================
function watcherDogCheck(message) {
    // Example: prevent sensitive info leaks for kids mode
    const mode = localStorage.getItem("mobby_mode") || "adult";
    if (mode === "kid" && /password|hack|kill|root/i.test(message)) {
        alert("⚠️ WatcherDog blocked unsafe message for Kid Mode!");
        return false;
    }
    return runJSProtections(message);
}

window.watcherDogCheck = watcherDogCheck;

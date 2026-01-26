// ==========================
// SICryption.js – Client Guard
// ==========================

(() => {
  const ALLOWED_BROWSERS = ["chrome", "firefox", "brave", "safari", "edg"];
  const ALLOWED_HOST = "sic-corporation.github.io";

  const ua = navigator.userAgent.toLowerCase();
  const safeBrowser = ALLOWED_BROWSERS.some(b => ua.includes(b));

  if (!safeBrowser) {
    alert("🚫 Unsupported browser blocked by SICryption.");
    document.body.innerHTML = "<h1 style='color:red;text-align:center;margin-top:20%'>ACCESS DENIED</h1>";
    throw new Error("Browser blocked");
  }

  if (location.hostname !== ALLOWED_HOST && location.hostname !== "localhost") {
    document.body.innerHTML = "🚨 Unauthorized fork detected.";
    throw new Error("Fork blocked");
  }

  console.log("🔐 SICryption JS active");
})();

// ==========================
// JS Threat Scan
// ==========================
function jsThreatScan(message) {
  const patterns = [
    /<script/i,
    /eval\s*\(/i,
    /document\.cookie/i,
    /fetch\s*\(/i,
    /window\.location/i
  ];
  return !patterns.some(p => p.test(message));
}

// ==========================
// WatcherDog JS
// ==========================
function watcherDogJS(message) {
  const mode = localStorage.getItem("mobby_mode") || "adult";

  if (!jsThreatScan(message)) {
    alert("⚠️ WatcherDog blocked suspicious input.");
    return false;
  }

  if (mode === "kid" && /hack|kill|password|root/i.test(message)) {
    alert("🧸 Kid Mode Safety: message blocked.");
    return false;
  }

  return true;
}

window.watcherDogJS = watcherDogJS;

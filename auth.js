// FIREBASE SETUP
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

function showUserUI(user) {
  document.getElementById("sic-setup-screen").classList.add("hidden");
  document.getElementById("main-ui").classList.remove("hidden");

  localStorage.setItem("mobby_user", user.displayName || "Guest");
  localStorage.setItem("mobby_email", user.email || "guest@guest.com");
  localStorage.setItem("mobby_pfp", user.photoURL || "https://ui-avatars.com/api/?name=Guest");

  document.getElementById("sideName").innerText = localStorage.getItem("mobby_user");
  document.getElementById("sidePFP").src = localStorage.getItem("mobby_pfp");
}

// GOOGLE LOGIN
document.getElementById("btn-firebase-login").onclick = () => {
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider).then(res => showUserUI(res.user)).catch(console.error);
};

// MICROSOFT LOGIN
document.getElementById("btn-microsoft-login").onclick = () => {
  const provider = new firebase.auth.OAuthProvider("microsoft.com");
  provider.setCustomParameters({ prompt: "select_account" });
  auth.signInWithPopup(provider).then(res => showUserUI(res.user)).catch(console.error);
};

// EMAIL LOGIN
document.getElementById("btn-email-login").onclick = () => {
  const email = prompt("Enter your email:");
  const password = prompt("Enter your password:");
  auth.signInWithEmailAndPassword(email, password).then(res => showUserUI(res.user)).catch(err => alert(err.message));
};

// GUEST LOGIN
document.getElementById("btn-guest-login").onclick = () => {
  showUserUI({ displayName: "Guest", email: "guest@guest.com", photoURL: "https://ui-avatars.com/api/?name=Guest" });
};

// AUTH STATE
auth.onAuthStateChanged(user => { if (user) showUserUI(user); });

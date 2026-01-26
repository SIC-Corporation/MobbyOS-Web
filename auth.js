// Wait until the DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  // FIREBASE CONFIG
  const firebaseConfig = {
    apiKey: "AIzaSyCcXBC24LdNbKnnS4TDPDRrPuee0amae-A",
    authDomain: "sicaccountsystem.firebaseapp.com",
    projectId: "sicaccountsystem",
    storageBucket: "sicaccountsystem.firebasestorage.app",
    messagingSenderId: "135479971246",
    appId: "1:135479971246:web:1bac73707f846965340c3f",
    measurementId: "G-RSV63GQ2EY"
  };

  // Initialize Firebase
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
  const btnGoogle = document.getElementById("btn-firebase-login");
  if (btnGoogle) btnGoogle.onclick = () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider).then(res => showUserUI(res.user)).catch(console.error);
  };

  // MICROSOFT LOGIN
  const btnMicrosoft = document.getElementById("btn-microsoft-login");
  if (btnMicrosoft) btnMicrosoft.onclick = () => {
    const provider = new firebase.auth.OAuthProvider("microsoft.com");
    provider.setCustomParameters({ prompt: "select_account" });
    auth.signInWithPopup(provider).then(res => showUserUI(res.user)).catch(console.error);
  };

  // EMAIL LOGIN
  const btnEmail = document.getElementById("btn-email-login");
  if (btnEmail) btnEmail.onclick = () => {
    const email = prompt("Enter your email:");
    const password = prompt("Enter your password:");
    auth.signInWithEmailAndPassword(email, password).then(res => showUserUI(res.user)).catch(err => alert(err.message));
  };

  // GUEST LOGIN
  const btnGuest = document.getElementById("btn-guest-login");
  if (btnGuest) btnGuest.onclick = () => {
    showUserUI({ displayName: "Guest", email: "guest@guest.com", photoURL: "https://ui-avatars.com/api/?name=Guest" });
  };

  // AUTH STATE
  auth.onAuthStateChanged(user => { if (user) showUserUI(user); });
});

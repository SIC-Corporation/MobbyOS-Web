<script>
  // --- Firebase Init ---
  const firebaseConfig = {
    apiKey: "AIzaSyCcXBC24LdNbKnnS4TDPDRrPuee0amae-A",
    authDomain: "sicaccountsystem.firebaseapp.com",
    projectId: "sicaccountsystem",
    storageBucket: "sicaccountsystem.firebasestorage.app",
    messagingSenderId: "135479971246",
    appId: "1:135479971246:web:1bac73707f846965340c3f",
    measurementId: "G-RSV63GQ2EY"
  };
  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();

  // --- Show UI after login ---
  function showUserUI(user){
    document.getElementById("sic-setup-screen").classList.add("hidden");
    document.getElementById("main-ui").classList.remove("hidden");

    localStorage.setItem("mobby_user", user.displayName || "Guest");
    localStorage.setItem("mobby_email", user.email || "guest@guest.com");
    localStorage.setItem("mobby_pfp", user.photoURL || "https://ui-avatars.com/api/?name=Guest");

    document.getElementById("sideName").innerText = localStorage.getItem("mobby_user");
    document.getElementById("sidePFP").src = localStorage.getItem("mobby_pfp");

    localStorage.setItem("mobby_auth", "true"); // mark as logged in
  }

  // --- Dummy functions to prevent errors ---
  function initSICAccountSystem(){ console.log("SIC Account System Initialized"); }
  function checkFork(){ console.log("checkFork called"); }

  // --- DOM ready ---
  document.addEventListener("DOMContentLoaded", ()=>{

    // Buttons
    const googleBtn = document.getElementById("btn-firebase-login");
    const msBtn = document.getElementById("btn-microsoft-login");
    const emailBtn = document.getElementById("btn-email-login");
    const guestBtn = document.getElementById("btn-guest-login");

    if(googleBtn) googleBtn.onclick = () => { 
      const provider = new firebase.auth.GoogleAuthProvider();
      auth.signInWithPopup(provider).then(res=>showUserUI(res.user)).catch(console.error);
    }

    if(msBtn) msBtn.onclick = () => {
      const provider = new firebase.auth.OAuthProvider("microsoft.com");
      provider.setCustomParameters({prompt:"select_account"});
      auth.signInWithPopup(provider).then(res=>showUserUI(res.user)).catch(console.error);
    }

    if(emailBtn) emailBtn.onclick = () => {
      const email = prompt("Enter your email:");
      const password = prompt("Enter your password:");
      if(!email || !password) return;
      auth.signInWithEmailAndPassword(email,password)
        .then(res=>showUserUI(res.user))
        .catch(err=>alert(err.message));
    }

    if(guestBtn) guestBtn.onclick = () => {
      showUserUI({displayName:"Guest",email:"guest@guest.com",photoURL:"https://ui-avatars.com/api/?name=Guest"});
    }

    // Auto-login if already authorized
    let mobbyAuth = localStorage.getItem("mobby_auth");
    if(mobbyAuth === "true"){
      document.getElementById("sic-setup-screen").classList.add("hidden");
      document.getElementById("main-ui").classList.remove("hidden");
    }

    // Firebase onAuthStateChanged
    auth.onAuthStateChanged(user => { if(user) showUserUI(user); });
  });
</script>

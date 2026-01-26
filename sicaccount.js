// Firebase Config
const firebaseConfig = {
    apiKey: "YOUR_FIREBASE_KEY",
    authDomain: "YOUR_FIREBASE_PROJECT.firebaseapp.com",
    projectId: "YOUR_FIREBASE_PROJECT",
    databaseURL: "https://YOUR_FIREBASE_PROJECT.firebaseio.com",
};
firebase.initializeApp(firebaseConfig);

function initSICAccountSystem() {
    const auth = firebase.auth();
    const db = firebase.database();

    // Buttons
    const btnGoogle = document.getElementById("btn-firebase-login");
    const btnGuest = document.getElementById("btn-guest-login");

    btnGoogle.onclick = () => {
        const provider = new firebase.auth.GoogleAuthProvider();
        auth.signInWithPopup(provider).then(res => {
            const user = res.user;
            saveUserPrefs(user.uid, user.displayName, user.email, user.photoURL);
        }).catch(console.error);
    };

    btnGuest.onclick = () => {
        showMainUI({name:"Guest", email:"guest@guest.com", photo:"https://ui-avatars.com/api/?name=Guest"});
    };

    auth.onAuthStateChanged(user => {
        if (user) loadUserPrefs(user.uid);
    });
}

// Save synced preferences
function saveUserPrefs(uid, name, email, photo) {
    firebase.database().ref('users/' + uid).set({name,email,photo});
    showMainUI({name,email,photo});
}

// Load synced preferences
function loadUserPrefs(uid) {
    firebase.database().ref('users/' + uid).once('value').then(snapshot => {
        const data = snapshot.val();
        showMainUI(data);
    });
}

// Show Main UI after login/setup
function showMainUI(userData){
    document.getElementById("sic-setup-screen").classList.add("hidden");
    const ui = document.getElementById("main-ui");
    ui.classList.remove("hidden");

    localStorage.setItem("mobby_user", userData.name);
    localStorage.setItem("mobby_email", userData.email);
    localStorage.setItem("mobby_pfp", userData.photo);

    // Update sidebar
    document.getElementById("sideName").innerText = userData.name;
    document.getElementById("sidePFP").src = userData.photo;
}

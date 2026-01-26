// import firebase modules
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, OAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCcXBC24LdNbKnnS4TDPDRrPuee0amae-A",
  authDomain: "sicaccountsystem.firebaseapp.com",
  projectId: "sicaccountsystem",
  storageBucket: "sicaccountsystem.firebasestorage.app",
  messagingSenderId: "135479971246",
  appId: "1:135479971246:web:1bac73707f846965340c3f",
  measurementId: "G-RSV63GQ2EY"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// example google login
document.getElementById("btn-firebase-login")?.addEventListener("click", async () => {
  const provider = new GoogleAuthProvider();
  try {
    const res = await signInWithPopup(auth, provider);
    console.log(res.user);
    // showUserUI(res.user) ...
  } catch (err) {
    console.error(err);
  }
});

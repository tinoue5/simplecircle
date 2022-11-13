import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js'
import { getAnalytics } from 'https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js'
import { getAuth, signInWithEmailAndPassword, signOut, signInWithRedirect,
  onAuthStateChanged, GoogleAuthProvider, getRedirectResult }
 from 'https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js'
import { getFirestore } from 'https://www.gstatic.com/firebasejs/9.10.0/firebase-firestore.js'

const firebaseConfig = {
  apiKey: "AIzaSyDn63P4LwWmB6udxvNXm_Ed10MJ26TjEaY",
  authDomain: "practice-b5aa4.firebaseapp.com",
  projectId: "practice-b5aa4",
  storageBucket: "practice-b5aa4.appspot.com",
  messagingSenderId: "405362124444",
  appId: "1:405362124444:web:069b2c7b80394f8e742f59",
  measurementId: "G-YVVSCENTP5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

window.logon = (email, password) => {
  // var email = $("email").val();
  // var password = $("password").val();
  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log("Login Successful.")
      // ...
      return true;
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log(error.code);
      console.log(error.message);

      return false;
    });
}

window.currentUser = () => {
  if(auth.currentUser==null){
    console.log("Not logged in.")
  }else{
    console.log(auth.currentUser.displayName);
    console.log(auth.currentUser.uid);
    console.log(auth.currentUser.email);
    console.log(auth.currentUser.emailVerified);
  }

  auth.currentUser.getIdToken(true).then((data) => {
    returnvalue = eval(JSON.stringify(data));
  });

  return returnvalue;
}

window.logon_check = () => {

  if(auth.currentUser==null){
    return false;
  }else{
    auth.currentUser.getIdToken(true).then((data) => {
      window.document.getElementById("token").value =
        eval(JSON.stringify(data));
    });
  }
}

window.logout = () => {
  signOut(auth).then(() => {
    // Sign-out successful.
    console.log("Logout Successful.")
    window.document.getElementById("token").value = "";
  }).catch((error) => {
    // An error happened.
  });
}

window.loginRedirectGoogle = () => {
  if(auth.currentUser==null){
    signInWithRedirect(auth, provider)
      .then((result) => {
        // This gives you a Google Access Token. You can use it to access the Google API.
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;
        // The signed-in user info.
        const user = result.user;
        // ...
      }).catch((error) => {
        // Handle Errors here.
        const errorCode = error.code;
        const errorMessage = error.message;
        // The email of the user's account used.
        const email = error.customData.email;
        // The AuthCredential type that was used.
        const credential = GoogleAuthProvider.credentialFromError(error);
        // ...
      });
  }
}

window.getRedirectResultGoogle = () => {
  getRedirectResult(auth)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access Google APIs.
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;

      // The signed-in user info.
      const user = result.user;
    }).catch((error) => {
      // Handle Errors here.
      const errorCode = error.code;
      const errorMessage = error.message;
      // The email of the user's account used.
      const email = error.customData.email;
      // The AuthCredential type that was used.
      const credential = GoogleAuthProvider.credentialFromError(error);
      // ...
    });
}

onAuthStateChanged(auth, (user) =>{
    if(user) {
      const uid = user.uid;
      console.log("changed:" + user.displayName);
      // console.log("changed:" + user.getIdToken());

      // user.getIdToken(true).then((data) => {
      //   const n = JSON.stringify(data);
      //   const t = JSON.stringify({"idtoken" : eval(n) });
      //   console.log(t);
      //   //データを送信
      //   const xhr = new XMLHttpRequest;       //インスタンス作成
      //   xhr.onload = function(){        //レスポンスを受け取った時の処理（非同期）
      //       var res = xhr.responseText;
      //       if (res.length>0) console.log(res);
      //   };
      //   xhr.onerror = function(){       //エラーが起きた時の処理（非同期）
      //       alert("error!");
      //   }
      //   xhr.open('post', "/app/tokentest", true);    //(1)
      //   xhr.setRequestHeader('Content-Type', 'application/json');
      //   xhr.send(t);    //送信実行
      // });

    }else{
      // User is signed out
    }
});

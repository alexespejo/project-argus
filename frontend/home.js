// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAK0toJ7D9_Jlt00PDemj16hi4g33-3Diw",
  authDomain: "fir-py-c779c.firebaseapp.com",
  databaseURL: "https://fir-py-c779c-default-rtdb.firebaseio.com",
  projectId: "fir-py-c779c",
  storageBucket: "fir-py-c779c.appspot.com",
  messagingSenderId: "450959185447",
  appId: "1:450959185447:web:f56bdb0d4b8d54642e2002",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

import {
  getFirestore,
  collection,
  onSnapshot,
  addDoc,
  deleteDoc,
  getDocs,
  doc,
  query,
  where,
  orderBy,
  serverTimestamp,
  getDoc,
  updateDoc,
} from "https://www.gstatic.com/firebasejs/9.6.8/firebase-firestore.js";

const db = getFirestore();

const colRef = collection(db, "members");
// const q = query(colRef, orderBy("createdAt"));
const deleteSelector = document.getElementById("deleteMember");
const updateSelector = document.getElementById("updateMember");
const data = document.getElementById("data");

onSnapshot(colRef, (snapshot) => {
  deleteSelector.innerHTML = "";
  updateSelector.innerHTML = "";
  data.innerHTML = "";
  const memberslist = [];
  snapshot.forEach((doc) => {
    const x = doc.data();
    x.id = doc.id;
    memberslist.push(x);
  });
  // for (let x = 0; x < memberslist.length(); x++) {}
  console.log(memberslist.sort((a, b) => (a.access > b.access ? 1 : -1)));
  for (let x = 0; x < memberslist.length; x++) {
    // console.log(JSON.stringify(memberslist[x].name));
    const displayItem = document.createElement("p");
    const deleteItem = document.createElement("option");
    const updateItem = document.createElement("option");

    displayItem.innerHTML = `${memberslist[x].name} Tier: ${memberslist[x].access}`;

    deleteItem.setAttribute("value", memberslist[x].id);
    updateItem.setAttribute("value", memberslist[x].id);

    deleteItem.innerHTML = `${memberslist[x].name} ${memberslist[x].access}`;
    updateItem.innerHTML = `${memberslist[x].name} ${memberslist[x].access}`;

    data.appendChild(displayItem);

    deleteSelector.appendChild(deleteItem);
    updateSelector.appendChild(updateItem);
  }
});
// const q = query(collection(db, "members"), where("access", "==", 1));

// const querySnapshot = await getDocs(q);
// querySnapshot.forEach((doc) => {
//   // doc.data() is never undefined for query doc snapshots
//   console.log(doc.id, " => ", doc.data());
// });

const deleteMembers = document.querySelector(".delete");
deleteMembers.addEventListener("submit", (e) => {
  e.preventDefault();
  const member = document.getElementById("deleteMember");
  const docRef = doc(db, "members", member.value);
  console.log(member.value);
  console.log(typeof docRef);
  deleteDoc(docRef).then(() => {
    deleteMembers.reset();
  });
});

const updateMember = document.querySelector(".update");

updateMember.addEventListener("submit", (e) => {
  e.preventDefault();
  const member = document.getElementById("updateMember");
  const changeName = document.getElementById("changeName");
  const changeAccess = document.getElementById("changeAccess");

  const docRef = doc(db, "members", member.value);

  if (changeName.value != "" && changeAccess.value != "") {
    updateDoc(docRef, {
      name: changeName.value,
      access: changeAccess.value,
    }).then(() => {
      updateMember.reset();
    });
  } else if (changeName.value != "") {
    updateDoc(docRef, {
      name: changeName.value,
    }).then(() => {
      updateMember.reset();
    });
  } else if (changeAccess.value != "") {
    updateDoc(docRef, {
      access: parseInt(changeAccess.value),
    }).then(() => {
      updateMember.reset();
    });
  } else {
    alert("nothing is here");
  }
});

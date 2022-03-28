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

function setAttributes() {
  const attributes = {
    disabled: "",
    selected: "",
    hidden: "",
  };
  let element = document.createElement("option");
  element.innerHTML = "Select One";
  Object.keys(attributes).forEach((attr) => {
    element.setAttribute(attr, attributes[attr]);
  });
  return element;
}
//Realtime updates UI for changes in the database
//NOTES**** split up update and delete functionality into seperate files later on

const deleteSelector = document.getElementById("deleteMember");
const updateSelector = document.getElementById("updateMember");
const data = document.getElementById("data");

onSnapshot(colRef, (snapshot) => {
  deleteSelector.innerHTML = "";
  updateSelector.innerHTML = "";
  deleteSelector.appendChild(setAttributes());
  updateSelector.appendChild(setAttributes());

  //
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

    displayItem.innerHTML = `${memberslist[x].name} Tier: ${memberslist[x].access} Last Access: ${memberslist[x].lastAccess}`;

    deleteItem.setAttribute("value", memberslist[x].id);
    updateItem.setAttribute("value", memberslist[x].id);

    deleteItem.innerHTML = `${memberslist[x].name} ${memberslist[x].access}`;
    updateItem.innerHTML = `${memberslist[x].name} ${memberslist[x].access}`;

    data.appendChild(displayItem);
    deleteSelector.appendChild(deleteItem);
    updateSelector.appendChild(updateItem);
  }
});

//DELETES Members based off a selection of user name
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

//Creates time interval between camera log
const settingRef = doc(db, "settings", "configurations");
const docSnap = await getDoc(settingRef);

const cameraDuration = document.getElementById("cameraDuration");
const cameraDuration_output = document.getElementById("cameraDuration-output");
cameraDuration_output.innerHTML = `${docSnap.data().cameraDuration} seconds`;

cameraDuration.setAttribute("value", docSnap.data().cameraDuration);
cameraDuration.oninput = () => {
  cameraDuration_output.innerHTML = `${cameraDuration.value} seconds`;
};

//Display Camera Logs
const cameraLogs = document.getElementById("camera-logs");
const historyRef = collection(db, "history");

const querySnapshot = await getDocs(historyRef);
querySnapshot.forEach((doc) => {
  // doc.data() is never undefined for query doc snapshots
  if (doc.id != "most_recent") {
    const logTime = document.createElement("p");
    const logPerson = document.createElement("h3");

    logTime.innerHTML = `${JSON.stringify(doc.data().history[0].name)} ${
      doc.data().date
    }`;

    cameraLogs.appendChild(logTime);
  }
});

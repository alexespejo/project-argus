# Project Argus

## What is it

Argus is a facial recognition camera and smart door lock accompanied by a dedicated web application. Combining my knowledge of IOT and web development. 

### Purpose 
It is not an uncommon mistake to forget or misplace a key whether it be your dorm, house or car. Forgetting such a small yet essential object can be an inconvenience and a hastle. Argus provides a multifacited security and convient solution to an issue that plagues millions. Forgetfullness...

### Use 
The camera itself would be a Raspberry PI and Camera Module mounted by the door. The camera will act as a running video stream till a person's face is presented in front of the camera. The camera will identify the person by their name or "unkown" and store that data to the database. If the person is not "unkown" they will be sent a phone notifcation on their app that will verify their access to the door and if they confirm the door will unlock. 

The web app would offer additional insight to Argus' view. A Ring inspired design will allow the user to view the live video stream from the camera(s). The app would present a collection of time series data of every instance a person is at the door and/or opens the door. The user will be able to customize aspects of the camera itself, such as time intervals in between scanning (in the instance there are multiple people approaching the door). 

The app will also allow admin users to grant people access to the smart door allocate app privelleges to specific users. As well as delete and update users as the admin sees fit.

## Technology overview

To build out the camera I used the Python OpenCV and face recognition libraries along side a Raspberry PI and the Raspberry PI Camera V2.

!currently
The web application is being built using vanilla HTML but I soon hope to implement React/React Native into the final project

The camera and web app backends are built with Flask and Firebase using the Firestore as the main database

### Technologies

IOT: Raspberry PI, Raspberry PI Camera V2, Python, Flask, OpenCV

APP: HTML, CSS, JavaScript, SCSS

BACKEND
Flask: 
  Used to build out a web server that stores the REST APIs for the camera and app to communicate with the database 

Firebase (Cloud Firestore) 
  Nonrelational real time databased that stores the user and camera data 


### Current State 
The baseline demo functionality is near completion in vanilla HTML, CSS, and JavaScript but will be soon migrated to React and Boostrap for a more concise and better development experience. 

The facial recognition software on a Raspberry PI and camera has been tested for proof of feasibility, but has yet to be properly implemented and tested. 

### Futures

-Plan to fully create the app in React.js

-Implement pyTorch or TensorFlow to the face recognition system

-Bring in D3 for processing analytics to the app

## Doc references 
Firebase: https://firebase.google.com/docs/firestore
face recogntion https://github.com/ageitgey/face_recognition 
OpenCV https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
Flask https://flask.palletsprojects.com/en/2.1.x/ 

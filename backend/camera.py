from flask import Flask, redirect, render_template, Response
import cv2
import face_recognition
import numpy as np
import firestore as db  # import from firestore.py
import datetime as dt
app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Initialize some variable
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def gen_frames():
    timeLimit = db.get_config_camera_interval()  # gettign time intrval
    recentTime = int(dt.datetime.now().strftime("%Y%m%d%H%M%S"))
    print(recentTime)
    # getting the most recent time
    recentPerson = db.history_log.get_most_recent_member()
    print(timeLimit)
    while True:
        known_face_encodings = db.encoding.get_encodings()  # getting the encodings
        known_face_names = db.encoding.get_names()  # getting the ids
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
                # if it's a different person
                if name != recentPerson and int(dt.datetime.now().strftime("%Y%m%d%H%M%S")) >= recentTime + 10 or int(dt.datetime.now().strftime("%Y%m%d%H%M%S")) >= recentTime + timeLimit:
                    try:
                        db.history_log.add_history(face_names)  # log history
                        timeLimit = db.get_config_camera_interval()  # gettign the time interval
                        recentTime = int(
                            dt.datetime.now().strftime("%Y%m%d%H%M%S"))
                        recentPerson = name
                        print(timeLimit)
                    except:
                        print('error')
                        continue
                print(face_names)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

import face_recognition
from flask import Flask, render_template, request, redirect, Response
import camera 
import main_db as db
import datetime as dt 
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_faces_in_image(name, access, file_stream):
    # Load the uploaded image filed
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)[0].tolist()

    db.add_member(name, access, unknown_face_encodings)
    return redirect('http://127.0.0.1:5500/frontend/home.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    db.encoding.update()
    name = request.form.get("name")
    access = request.form.get("access")
    access = int(access)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            return detect_faces_in_image(name, access, file)
    return ('', 204)

@app.route('/update', methods=['GET', 'POST'])
def update():
    db.encoding.update()
    member = request.form.get("updateMember")
    changeName = request.form.get("changeName")
    changeAccess = request.form.get("changeAccess")

    db.Members.update_member(member, changeName, changeAccess)

    return ('', 204)

@app.route('/configuration',  methods=['GET', 'POST'])
def config():
    db.config_camera_interval(int(request.form.get('cameraDuration')))
    return('', 204)
    
@app.route('/members')
def members():
    return db.encoding.get_members()

@app.route('/video')
def video():
    return render_template('stream.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


# Add settings configurations 
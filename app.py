from flask import Flask, render_template, Response,request,url_for,redirect,current_app,flash
import cv2
import face_recognition
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from air_frames_file import air_frames
from reading import reader_frames
from final_verify import verify_image
from snake_game import game_frames
from datetime import datetime

#from myapp import app, db
app=Flask(__name__)
#current_app.config['SERVER_NAME'] = ' 127.0.0.1:5000/'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#intializing the database
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(128))
    time = db.Column(db.String(128))
    def __init__(self,name,date,time):
        self.name = name
        self.date = date
        self.time = time

def gen_frames():
    global i
    i=0
    
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        success, frame = camera.read()
        photo_image = frame.copy()
        # read the camera frame
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
        # Loading the required haar-cascade xml classifier file
        haar_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')
        
        # Applying the face detection method on the grayscale image
        faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)
        
        # Iterating through rectangles of detected faces
        for (x, y, w, h) in faces_rect:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Face Detected", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (68, 42, 32), 2 )
        if not success:
            break
        else:
            i+=1
            if i<=20:
                file_name_path = "D:\Programming World\Another Testing Folder\Sample Testing - database\Photo/"+str("Photo")+str(i)+'.jpg'
                cv2.imwrite(file_name_path, photo_image)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            new = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            
            yield (new)
#main page
@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html',)

#entering home page
@app.route("/enter/<usr>",methods = ['GET','POST'])
def enter(usr):
    return render_template('enter.html',usr = usr)

@app.route("/database",methods = ['GET','POST'])
def database():
    return render_template('database.html',values = users.query.all())
@app.route("/aircanvas")
def aircanvas():
    return render_template('aircanvas.html')

@app.route('/air_canvas',methods = ['GET','POST'])
def air_canvas():
    return Response(air_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/reader")
def reader():
    return render_template('reader.html')

@app.route('/reader_canvas',methods = ['GET','POST'])
def reader_canvas():
    return Response(reader_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/game",methods = ['GET','POST'])
def game():
    if request.method == 'POST':
        return redirect(url_for('game'))
    return render_template('game.html')

@app.route('/game_canvas',methods = ['GET','POST'])
def game_canvas():
    return Response(game_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    verifying = verify_image()
    #found_user = users.query.filter_by(name = verifying).first()
    if verifying == None:
        #flash("Unkown Person")
        return redirect(url_for('index'))
    else:
        now = datetime.now()
        date = now.strftime("%d %b, %Y")
        time = now.strftime("%H:%M:%S")
        usr = users(verifying,date,time)
            
        db.session.add(usr)
            
        db.session.commit()
        return redirect(url_for('enter',usr = verifying ))

@app.route("/verification")
def verification():
    return render_template('facerecog.html')
    
@app.route("/face_recog",methods = ['GET','POST'])
def face_recog():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
            
    # return a 
if __name__=='__main__':
    db.create_all()
    app.run(debug=True)
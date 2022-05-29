from flask import Blueprint,Response, flash, redirect, render_template,url_for,jsonify,abort
from flask_login import login_required,current_user
import cv2
import time
from safety import db
import numpy as np
import os
from safety.admin.forms import DriverRegistrationForm
from safety.models import Driver
import uuid

secret_id=str(uuid.uuid4())

admin=Blueprint('admin',__name__)


dataset_path = 'safety/static/data/face_data/'
face_cascade = cv2.CascadeClassifier('safety/static/data/haarcascade/haarcascade_frontalface.xml')
class Camera():
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.start_time = time.time() 
        self.stop_time  = self.start_time + 15
        self.is_stored = False  # keep it to send it with AJAX
        self.skip = 0
        self.face_data = []
        
    def __del__(self):
        self.video.release()
        
    def get_feed(self):
        stat, frame = self.video.read()
        try:
            ret, jpeg = cv2.imencode('.jpg', frame)
        except:
            return b'','Fail'
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame,1.3,5)
        faces = sorted(faces,key=lambda f:f[2]*f[3])
        # print(type(faces))
        for face in faces:
            x,y,w,h = face

            #Get the face ROI
            offset = 10
            face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
            face_section = cv2.resize(face_section,(100,100))
            self.skip += 1
            if self.skip % 10 ==0 :
                self.face_data.append(face_section)            

        self.is_stored = (time.time() >= self.stop_time) # stop stream after 15 seconds
        return jpeg.tobytes(), self.is_stored
        
camera = Camera()

def get_camera():
    return camera

def generate(camera):
    global dataset_path,secret_id
    # start timer only when start streaming
    camera.start_time = time.time()
    camera.stop_time = camera.start_time + 15
    
    while True:
        frame, is_stored = camera.get_feed()
        if is_stored=='Fail' or is_stored:
            break
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
    if is_stored != 'Fail':
        camera.face_data = np.asarray(camera.face_data)
        camera.face_data = camera.face_data.reshape((camera.face_data.shape[0],-1))
        np.save(dataset_path+secret_id+'.npy',camera.face_data)
        print("Data Successfully save at "+dataset_path+secret_id+'.npy')


@admin.route('/admin/register')
@login_required
def driver_register_feed():
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403)
    return render_template('/admin/admin_register.html')

@admin.route('/admin/home')
@login_required
def ahome():
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403)
    return render_template('admin/admin_home.html')

 
@admin.route('/admin/register/form/<id>',methods=['GET','POST']) 
@login_required
def driver_register_form(id): 
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403)
    camera=get_camera()
    camera.video.release()
    del camera
    cv2.destroyAllWindows()
    form=DriverRegistrationForm()
    if form.validate_on_submit():
        print("Submitted")
        driver=Driver(driverid=id,name=form.name.data,phone=form.phone.data,aadhar=form.aadhar.data,vehicle=form.vehicle.data)
        db.session.add(driver)
        db.session.commit()
        flash('Driver added Successfully','success')
        return redirect(url_for('admin.ahome'))
    return render_template('admin/driver_register.html',form=form,id=id)

@admin.route('/admin/video')
@login_required
def admin_video_capture():
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403)
    return render_template('admin/admin_video.html')

@admin.route('/admin/video/is_stored',methods=['GET']) 
@login_required
def admin_is_stored(): 
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403)

    camera = get_camera() 
    print(camera.is_stored)
    return jsonify({'is_stored': camera.is_stored,'id':secret_id})

@admin.route('/admin/video/video_feed')
@login_required
def admin_video_feed():
    if current_user.email != os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
        abort(403) 
    camera = get_camera() 
    camera.is_stored = False
    return Response(generate(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

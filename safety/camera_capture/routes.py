from flask import Blueprint,Response, abort, render_template,jsonify
from flask_login import login_required,current_user
import cv2
import time
import numpy as np
from safety.camera_capture.utils import data_prep, send_info_email
from safety.models import Driver,User
import os

camera_capture=Blueprint('camera_capture',__name__)

face_cascade = cv2.CascadeClassifier('safety/static/data/haarcascade/haarcascade_frontalface.xml')
ids, trainset = data_prep()
number_of_guess=[]
unique_id=os.environ.get('SECRET_KEY','7f26ee67-50f5-4d5a-a72c-7582e0929906')
def distance(v1, v2):
    return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):
    dist = []
    
    for i in range(train.shape[0]):
        # Get the vector and label
        ix = train[i, :-1]
        iy = train[i, -1]
        # Compute the distance from test point
        d = distance(test, ix)
        # print(d)
        if d<11000:
            dist.append([d, iy])
    # Sort based on distance and get top k
    if len(dist)<k:
        return -1
    dk = sorted(dist, key=lambda x: x[0])[:k]
    # Retrieve only the labels
    labels = np.array(dk)[:, -1]
    
    # Get frequencies of each label
    output = np.unique(labels, return_counts=True)
    # Find max frequency and corresponding label
    index = np.argmax(output[1])
    return output[0][index]


class Camera():
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.start_time = time.time() 
        self.stop_time  = self.start_time + 10
        self.is_recognised = False  # keep it to send it with AJAX
        self.person_id = "Unknown"
        
    def __del__(self):
        self.video.release()
        
    def get_feed(self):
        stat, frame = self.video.read()
        print(stat,"camera status")
        try:
            ret, jpeg = cv2.imencode('.jpg', frame)
        except:
            return b'','Fail'
            
        faces = face_cascade.detectMultiScale(frame,1.3,5)
        for face in faces:
            x,y,w,h = face

            #Get the face ROI
            offset = 10
            face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
            face_section = cv2.resize(face_section,(100,100))

            #Predicted Label (out)
            out = knn(trainset,face_section.flatten())
            if out==-1:
                pred_id="Unknown"
            else:
                pred_id = ids[int(out)]
            number_of_guess.append(pred_id)
            print(pred_id)
        self.is_recognised = (time.time() >= self.stop_time) # stop stream after 10 seconds
        if len(number_of_guess)>0:
            self.person_id = max(number_of_guess,key=number_of_guess.count)
        return jpeg.tobytes(), self.is_recognised
        
camera = Camera()

def get_camera():
    return camera
def generate(camera):
    # start timer only when start streaming
    camera.start_time = time.time()
    camera.stop_time = camera.start_time + 10
    
    while True:
        frame, camera.is_recognised = camera.get_feed()
        if camera.is_recognised=='Fail' or camera.is_recognised:
            break
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
      
@camera_capture.route('/video')
@login_required
def video_capture():
    global unique_id
    unique_id=unique_id+'9'
    return render_template('video.html')

@camera_capture.route('/video/is_recognised')
@login_required
def is_recognised(): 
    global unique_id
    camera = get_camera() 
    if not unique_id==(os.environ.get('SECRET_KEY','7f26ee67-50f5-4d5a-a72c-7582e0929906')+'9'):
        camera.is_recognised=='Fail'
    # if camera.is_recognised=='Fail':
    #     abort(503)
    print("Here")
    print(camera.is_recognised)
    return jsonify({'is_recognised': camera.is_recognised,'person_id':camera.person_id})

@camera_capture.route('/video/video_feed')
@login_required
def video_feed():
    global unique_id
    if not unique_id==(os.environ.get('SECRET_KEY','7f26ee67-50f5-4d5a-a72c-7582e0929906')+'9'):
        abort(403)
    try:
        camera = get_camera() 
    except:
        abort(503)
    camera.is_recognised = False
    return Response(generate(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_capture.route('/result/<id>',methods=['GET'])
@login_required
def result(id):
    global unique_id
    if not unique_id==(os.environ.get('SECRET_KEY','7f26ee67-50f5-4d5a-a72c-7582e0929906')+'9'):
        abort(403)
    try:
        camera = get_camera() 
    except:
        abort(503)
    # if unique_id=="abcdefgh":
    #     return render_template('errors/403.html'),403
        
    # unique_id = 'abcdefgh'
    # print(unique_id, "res")
    try:
        camera=get_camera()
    except:
        abort(503)
    camera.video.release()
    del camera
    cv2.destroyAllWindows()
    if id=="Unknown":
        return render_template('result_unknown.html')
    driver=Driver.query.filter_by(driverid=id).first()
    print(driver) 
    if driver is None:
        abort(500)
    user = User.query.filter_by(email=current_user.email).first()
    if send_info_email(driver,user)!='Success':
        abort(500)
    
    return render_template('driver_profile.html',person=driver)



@camera_capture.route('/cam_error')
@login_required
def cam_error():
    return render_template('errors/cam_error.html')
 
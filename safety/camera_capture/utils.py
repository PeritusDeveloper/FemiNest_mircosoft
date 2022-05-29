import os
import numpy as np
from flask_mail import Message
from flask import url_for
from safety import mail
from safety.models import Driver, User

def data_prep():
    
    dataset_path = 'safety/static/data/face_data/'

    face_data = [] 
    labels = []

    class_id = 0 # Labels for the given file
    names = {} #Mapping btw id - name

    for fx in os.listdir(dataset_path):
        if fx.endswith('.npy'):
            #Create a mapping btw class_id and name
            names[class_id] = fx[:-4]
            print("Loaded "+fx)
            data_item = np.load(dataset_path+fx)
            face_data.append(data_item)

            #Create Labels for the class
            target = class_id*np.ones((data_item.shape[0],))
            class_id += 1
            labels.append(target)
        
    face_dataset = np.concatenate(face_data,axis=0)
    face_labels = np.concatenate(labels,axis=0).reshape((-1,1))

    print(face_dataset.shape)
    print(face_labels.shape)

    trainset = np.concatenate((face_dataset,face_labels),axis=1)
    print(trainset.shape)
    return names,trainset




def send_info_email(driver,user):
    msg = Message('Driver Information',
                  sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.html = f'''Hi {user.username},<br><br>
The information of the driver is:
Name: {driver.name} <br>
Phone No: {driver.phone} <br>
Aadhar No: {driver.aadhar} <br>
Vehicle No: {driver.vehicle} <br><br>

Thanks,<br>
The FemiNest Team
    '''
    try:
        mail.send(msg) 
        return "Success" 
    except:
        return "Failed"
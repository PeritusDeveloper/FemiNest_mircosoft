from flask import current_app
from safety import db, login_manager
from flask_login import UserMixin
import jwt
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(50), unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def get_reset_token(self, expires_sec=3600):
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        user_id=data.get('user_id')
        return User.query.get(user_id)

    def __repr__(self):
       return f"Username : {self.username}, id: {self.id}"

class Driver(db.Model):
    driverid = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(10),unique=True,nullable=False)
    aadhar = db.Column(db.String(12),unique=True,nullable=False)
    vehicle= db.Column(db.String(30),unique=True,nullable=False)

    def __repr__(self):
        return f"name : {self.name}, vehicle: {self.vehicle}" 

class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    msg= db.Column(db.String(1000))
    name=db.Column(db.String(100))
    email=db.Column(db.String(50))
    
    
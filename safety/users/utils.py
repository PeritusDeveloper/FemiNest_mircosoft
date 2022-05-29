from flask_mail import Message
from flask import url_for
from safety import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.html = f'''Hi {user.username},<br><br>
You recently requested to reset your password for your <b>FemiNest</b> account. Use the link below to reset your password:
{url_for('users.reset_token', token=token, _external=True)}<br>
The reset link is valid for the next <b>30 minutes</b>.
If you did not request a password reset,then simply ignore this email and no changes will be made.<br><br>
Thanks,<br>
The FemiNest Team
'''
    try:
        mail.send(msg) 
        return "Success" 
    except:
        return "Failed"
        
    
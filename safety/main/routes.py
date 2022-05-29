from flask import render_template,redirect,url_for
from flask import Blueprint
from flask_login import current_user, login_required
from safety.main.forms import ContactForm
from safety.models import Contact
from safety import db

main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def home():
    return render_template('home.html')

@main.route("/about")
@login_required
def about():
    return render_template('about.html')

@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html')

@main.route("/contactUs",methods=['POST','GET'])
def contact():
    form=ContactForm()
    if form.validate_on_submit():
        message=Contact(name=form.name.data,msg=form.msg.data,email=form.email.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('contactUs.html',form=form)

@main.route("/driver_profile")
@login_required
def driver_profile():
    return render_template('/driver_profile.html')

from flask import render_template, url_for, flash, redirect, request,abort
from flask import Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from safety import db,bcrypt
from safety.users.utils import send_reset_email
from safety.users.forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm
from safety.models import User
import os

users= Blueprint('users',__name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please log in')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/", methods=['GET','POST'])
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.email== os.environ.get('ADMIN_EMAIL','FemiNestAdmin@gmail.com'):
            print("Admin")
            return redirect(url_for('admin.ahome'))
        print("User")
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # print(form.remember.data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)  
            elif current_user.email== os.environ.get('ADMIN_EMAIL','FemiNestA dmin@gmail.com'):
                return redirect(url_for('admin.ahome'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if(send_reset_email(user)!='Success'):
            abort (500)

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
# def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # token=request.args.get('token','NULL')
    print(token)
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset! Sign In now!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
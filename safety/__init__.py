# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate

# from safety.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = "Log in to access the page"
login_manager.login_message_category = 'info'
mail = Mail()

def create_app():
    app =Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    Migrate(app,db)
    
    from safety.errors.error import errors
    app.register_blueprint(errors)
    
    from safety.users.routes import users
    app.register_blueprint(users)
    
    from safety.camera_capture.routes import camera_capture
    app.register_blueprint(camera_capture)
    
    from safety.main.routes import main
    app.register_blueprint(main)
    
    from safety.admin.routes import admin
    app.register_blueprint(admin)
    # from safety.driver.routes import
    
    return app
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError,Regexp
from safety.models import Driver



class ContactForm(FlaskForm):
    name = StringField('Name')
    msg = StringField('Message')
    email = StringField('Email')
    submit = SubmitField('Send')
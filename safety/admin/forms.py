from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError,Regexp
from safety.models import Driver



class DriverRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])
    aadhar = StringField('AadharNo',
                        validators=[DataRequired(),Length(min=12,max=12,message="Aadhar number has 12 digits"),Regexp('^[0-9]*$',message='Aadhar Number can contain only numbers')])
    phone = StringField('PhoneNo',
                        validators=[DataRequired(),Length(min=10,max=10,message="Mobile Number has 10 digits"),Regexp('^[0-9]*$',message='Mobile Number can contain only numbers')])
    vehicle = StringField('VehicleNo', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_aadhar(self, aadhar):
        aadhar_data = Driver.query.filter_by(aadhar=aadhar.data).first() 
        if aadhar_data:
            raise ValidationError('This Aadhar number is already registered.')
        
        
        
    def validate_phone(self, phone):
        phone_data = Driver.query.filter_by(phone=phone.data).first()
        if phone_data:
            raise ValidationError('This Mobile number is already registered.')

    def validate_vehicle(self, vehicle):
        vehicle_data = Driver.query.filter_by(vehicle=vehicle.data).first()
        if vehicle_data:
            raise ValidationError('This Vehicle number is already registered.')

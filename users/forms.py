from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6,max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    recaptcha = RecaptchaField()
    pin = StringField(validators=[DataRequired()])
    submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    current_password = PasswordField(id='password', validators=[DataRequired()])
    show_password = BooleanField('Show password', id='check')
    new_password = PasswordField(validators=[DataRequired(), Length(min=8, max=15, message="Must be between 8 and 15 characters in length")])
    confirm_new_password = PasswordField(validators=[DataRequired(), EqualTo('new_password', message='Both new password fields must be equal')])
    submit = SubmitField('Change Password')
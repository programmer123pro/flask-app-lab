from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import *
from wtforms.validators import *
from datetime import datetime as dt
from app import db
from .models import User

def emailUnique(form, field):
    count = db.session.query(User).filter(User.email == field.data).count()
    if count > 0:
        raise ValidationError('This email is already busy')

def confirmPassword(form, field):
    if(form.password.data != field.data):
        raise ValidationError("Passwords don't match")

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), emailUnique])
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[A-Za-z\d]{4,14}$')])
    password = PasswordField('Password', validators=[DataRequired(), Regexp(r'^[^\s]{7,}$')])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), confirmPassword])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
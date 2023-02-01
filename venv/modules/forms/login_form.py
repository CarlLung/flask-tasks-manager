from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

class RegisterForm(FlaskForm):
    username = StringField("New user's username")
    password = PasswordField('Password')
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Submit')
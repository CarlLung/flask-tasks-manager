from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Submit')
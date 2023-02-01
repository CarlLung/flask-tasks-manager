from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CmdForm(FlaskForm):
    command = StringField('Enter Command:')
    submit = SubmitField('Go')

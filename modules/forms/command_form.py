from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class CmdForm(FlaskForm):
    command = StringField('Enter Command:', validators=[InputRequired()])
    submit = SubmitField('Go')

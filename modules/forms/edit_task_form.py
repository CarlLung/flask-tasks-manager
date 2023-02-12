from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import InputRequired

class EditForm(FlaskForm):
    new_responsible = StringField('Reassign the Task to', validators=[InputRequired()])
    new_due = DateField('New Due Date:', validators=[InputRequired()])
    submit = SubmitField('Edit')
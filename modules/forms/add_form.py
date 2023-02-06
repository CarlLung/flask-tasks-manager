from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import InputRequired

class AddForm(FlaskForm):
    responsible = StringField('Assign the Task to', validators=[InputRequired()])
    title = StringField('Task Title', validators=[InputRequired()])
    description = TextAreaField('Task Description', validators=[InputRequired()])
    due = DateField('Due Date:', validators=[InputRequired()])
    submit = SubmitField('Submit')


            
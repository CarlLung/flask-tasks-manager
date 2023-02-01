from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField

class AddForm(FlaskForm):
    responsible = StringField('Assign the task to:')
    title = StringField('Task title:')
    description = TextAreaField('Task description:')
    due = DateField('Due date:')
    submit = SubmitField('Submit')
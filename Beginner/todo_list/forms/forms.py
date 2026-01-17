from models.models import TodoList
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    completed = BooleanField('Completed')
    submit = SubmitField('Add Todo')
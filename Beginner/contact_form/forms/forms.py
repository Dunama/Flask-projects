from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    fname = StringField('fname',
    validators= [DataRequired(), Length(min=2, max=60)])
    lname = StringField('lname',
    validators = [DataRequired(), Length(min=2, max=60)])
    email = StringField('email',
    validators = [DataRequired(), Email()])
    subject = StringField('subject',
    validators = [DataRequired(), Length(min=2, max=250)])
    message = TextAreaField('message',
    validators = [DataRequired()])
    submit = SubmitField('Send Message')
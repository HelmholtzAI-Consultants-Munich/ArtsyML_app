from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField

class EmailForm(FlaskForm):
    email = StringField(
        'Please enter your email address here:',
        validators=[
            DataRequired(message="Please enter your email address."), 
            Email(),
        ]
    )
    send = SubmitField('Send')
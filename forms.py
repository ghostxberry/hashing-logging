from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import TextAreaField
from wtforms.validators import InputRequired, Length

class registerUser(FlaskForm):
    username = StringField("Choose a username", validators=[InputRequired()])
    password = PasswordField("Create password", validators=[InputRequired()])
    email = StringField("Enter your email address", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    submit = SubmitField('Create User')


class loginForm(FlaskForm):
    username = StringField ("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class feedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Submit Feedback')

class deleteForm(FlaskForm):
    confirm_delete = SubmitField('Confirm Delete')
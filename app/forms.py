from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Diary

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    is_psychiatrist = BooleanField('Are you a psychiatrist?')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_psychiatrist = BooleanField('Are you a psychiatrist?')
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username has been taken already.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email has been taken already.')

class DiaryForm(FlaskForm):
    date = StringField('Date today', validators=[DataRequired()])
    mood = IntegerField('Mood today (1-10)', validators=[DataRequired()])
    post = TextAreaField('How was your day?', validators=[DataRequired()])
    submit = SubmitField('Add Post')

class AddPatientForm(FlaskForm):
    username = StringField('Username for Patient:', validators=[DataRequired()])
    submit = SubmitField('Add Patient')

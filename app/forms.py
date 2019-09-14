from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', Validators=[DataRequired()])
    password = PasswordField('Password', Validators=[DataRequired()])
    submit = SubmitField('Sign In')

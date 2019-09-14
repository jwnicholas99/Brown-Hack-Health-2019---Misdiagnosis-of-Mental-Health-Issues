from app import app, db
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, DiaryForm
from app.models import User, DiaryPost

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        return redirect('/index')

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Patient'}
    render_template('index.html', title="Get diagnosed", user=user)

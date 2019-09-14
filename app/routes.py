from app import app, db
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, DiaryForm
from app.models import Patient, Psychiatrist, Diary

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.is_psychiatrist:
            user = Psychiatrist.query.filter_by(username=form.username.data)
        else:
            user = Patient.query.filter_by(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("The username or password is not correct")
            return redirect(url_for('index'))
        login_user(user)
        next_url = request.args.get('next')
        return redirect(next_url)
    return render_template('login.html', title='Sign-In', form=form)

@app.route('/')
@app.route('/indexPatient')
@login_required
def index():
    diaryPosts = Diary.query.filter_by(patient_id = current_user.id)
    return render_template('indexPatient.html', title="Home", diaryPosts=diaryPosts)

from app import app, db
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, DiaryForm, AddPatientForm
from app.models import User, Diary
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return redirect(url_for('login'))
            urole = login.reload_user().get_urole()
            if ( (urole != role) and (role != "ANY")):
                return login.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_psychiatrist:
            return redirect(url_for('indexPsychiatrist'))
        else:
            return redirect(url_for('indexPatient'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("The username or password is not correct")
            return redirect(url_for('indexPatient'))
        login_user(user)
        next_url = request.args.get('next')
        return redirect(next_url)
    return render_template('login.html', title='Sign-In', form=form)

@app.route('/')
@app.route('/indexPatient')
@login_required(role="Patient")
def indexPatient():
    diaryPosts = Diary.query.filter_by(patient_id = current_user.id)
    return render_template('indexPatient.html', title="Home", diaryPosts=diaryPosts)

@app.route('/')
@app.route('/indexPsychiatrist')
@login_required(role="Psychiatrist")
def indexPsychiatrist():
    return render_template("indexPsychiatrist.html", title="Home | " + current_user.username, psychiatrist=current_user)

@app.route('/registration', methods=["GET","POST"])
def registration():
    if current_user.is_authenticated:
        if current_user.is_psychiatrist:
            return redirect(url_for('indexPsychiatrist'))
        else:
            return redirect(url_for('indexPatient'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)

@app.route('/IndexPsychiatrist/manage',  methods=["GET", "POST"])
@login_required(role="Psychiatrist")
def psychiatristManage():
    form = AddPatientForm()
    if form.validate_on_submit:
        user = User.query.filter_by(user=form.username.data, is_psychiatrist=False)
        if user is None:
            flash("The username is not found")
            return redirect(url_for('psychiatristManage'))
        current_user.patients.append(user)
        flash("Successfully added " + user.username + "!")
        return redirect(url_for('psychiatristManage'))
    return render_template("psychiatristManage", title='Manage Patients', psychiatrist=current_user) 

@app.route('/IndexPsychiatrist/manage/<username>')
@login_required(role="Psychiatrist")
def psychiatristDelete(username, patient, psychiatrist):
    psychiatrist.delete(patient)
    return redirect(url_for('psychiatristManage'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))





















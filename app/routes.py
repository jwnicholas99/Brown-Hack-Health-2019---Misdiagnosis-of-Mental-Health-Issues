from app import app, db
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, DiaryForm
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

@app.route('/registration', methods=["GET","POST"])
def registration():
    if current_user.is_authenticated:
        if current_user.is_psychiatrist:
            return redirect(url_for('indexPsychiatrist'))
        else:
            return redirect(url_for('indexPatient'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.is_psychiatrist = form.is_psychiatrist.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your accoutn has been registered!')
            return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)       

















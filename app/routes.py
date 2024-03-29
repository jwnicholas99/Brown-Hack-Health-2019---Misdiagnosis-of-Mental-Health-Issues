from app import app, db
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, DiaryForm, AddPatientForm
from app.models import User, Diary
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return redirect(url_for('login'))
            urole = current_user.get_urole()
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("The username or password is not correct")
            return redirect(url_for('login'))
        login_user(user)
        next_url = request.args.get('next')
        if not next_url or url_parse(next_url).netloc != '':
            if current_user.is_psychiatrist:
                return redirect(url_for('indexPsychiatrist'))
            else:
                return redirect(url_for('indexPatient'))
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
        user = User(username=form.username.data, email=form.email.data)
        user.is_psychiatrist = form.is_psychiatrist.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been registered!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form) 

@app.route('/indexPsychiatrist/manage',  methods=["GET", "POST"])
@login_required(role="Psychiatrist")
def psychiatristManage():
    form = AddPatientForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, is_psychiatrist=False).first()
        if user is None:
            flash("Username Not Found")
            return redirect(url_for('psychiatristManage'))
        current_user.patients_id.append(user)
        db.session.commit()
        print('b', current_user.patients_id)
        flash("Successfully added " + user.username + "!")
        return redirect(url_for('psychiatristManage'))
    print('a', current_user.patients_id) 
    return render_template("psychiatristManage.html", title='Manage Patients', psychiatrist=current_user, form=form) 

@app.route('/indexPsychiatrist/manage/<username>')
@login_required(role="Psychiatrist")
def psychiatristDelete(username):
    patient = User.query.filter_by(username=username).first()
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('psychiatristManage'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/addPost', methods=["GET","POST"])
@login_required(role="Patient")
def addPost():
    form = DiaryForm()
    if form.validate_on_submit():
        new_post = Diary(date=form.date.data, mood=form.mood.data, post=form.post.data, patient_id=current_user.id)
        current_user.diary.append(new_post)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('indexPatient'))
    return render_template('addPost.html', title='Add Post', form=form)

@app.route('/deletePost/<post_id>')
@login_required(role="Patient")
def deletePost(post_id):
    post = Diary.query.filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('indexPatient'))

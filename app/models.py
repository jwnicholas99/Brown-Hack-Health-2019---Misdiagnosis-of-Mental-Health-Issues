from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_patient, login_psychiatrist

class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    psychiatrist_id = db.Column(db.Integer, db.ForeignKey('psychiatrist.id'))
    dairy = db.relationship('Dairy', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_patient.user_loader
def load_user(id):
    return Patient.query.get(int(id))

class Psychiatrist(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    patient = db.relationship('Patient', backref='psychiatrist', lazy='dynamic')

    def __repr__(self):
        return '<Psychiatrist {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_psychiatrist.user_loader
def load_user(id):
    return Psychiatrist.query.get(int(id))

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    mood = db.Column(db.Integer)
    post = db.Column(db.String)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __repr__(self):
        return '<Diary {}>'.format(self.mood)


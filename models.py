from app_config import db
import datetime


class Doctor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    mobile = db.Column((db.Integer()), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    qualification = db.Column(db.String(50), nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    status = db.Column(db.String(10), nullable=False)
    available_date = db.Column(db.Date())
    available_time = db.Column(db.Time())
    lat_available = db.Column(db.Time())


class User(db.Model):
    reg_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(15), nullable=False)


class Appointment(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey('user.reg_id'))
    pat_name = db.Column(db.String(50), nullable=False)
    pat_age = db.Column(db.Integer(), nullable=False)
    pat_gender = db.Column(db.String(50), nullable=False)
    doctor = db.Column(db.Integer(), db.ForeignKey('doctor.id'))
    app_date = db.Column(db.Date())
    app_time = db.Column(db.Time())
    book_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    address = db.Column(db.String(100))

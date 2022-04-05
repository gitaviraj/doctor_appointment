import datetime
from app_config import app, db
from flask import request, jsonify, Blueprint, session, send_from_directory, send_file
from models import Doctor, User, Appointment
import json
from fpdf import FPDF

user = Blueprint('user', __name__, url_prefix='/user')


def validate_details(reqbody):
    error = {}
    if not reqbody.__contains__('NAME'):
        error["NAME"] = "User name required..."
    if not reqbody.__contains__('AGE'):
        error["Age"] = "User age required..."
    if not reqbody.__contains__('GENDER'):
        error["GENDER"] = "Gender required..."
    if not reqbody.__contains__('DOB'):
        error["DOB"] = "DOB  required..."
    if not reqbody.__contains__('MOBILE'):
        error["MOBILE"] = "Mobile number required..."
    if not reqbody.__contains__('EMAIL'):
        error["EMAIL"] = "Email required..."
    if not reqbody.__contains__('PASSWORD'):
        error["PASSWORD"] = "Password required..."
    return error


@user.route('/register', methods=['POST'])
def register_user():
    formdata = request.get_json()
    print(formdata)
    name = formdata.get("NAME")
    age = formdata.get("AGE")
    gender = formdata.get("GENDER")
    dob = formdata.get("DOB")
    mobile = formdata.get("MOBILE")
    email = formdata.get("EMAIL")
    password = formdata.get("PASSWORD")

    check = User.query.filter(email == User.email).first()
    if check:
        return jsonify({"ERROR": "Email already registered...."})

    error = validate_details(formdata)
    if error:
        return json.dumps(error)
    else:
        user = User(name=name, age=age, gender=gender, dob=dob, mobile=mobile, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"SUCCESS": "User successfully registered...."})


@user.route('/user/login', methods=['POST'])
def user_login():
    formdata = request.get_json()
    email = formdata.get("EMAIL")
    password = formdata.get("PASSWORD")
    user = User.query.filter(email == User.email).first()
    if user:
        if password == user.password:
            session['EMAIL'] = user.email
            return session['EMAIL']
        else:
           return jsonify({"ERROR": "Invalid password"})
    else:
        return jsonify({"ERROR": "User nor present"})


def creat_pdf(doctor, user, apoint):
    pdf = FPDF()
    pdf.add_page()
    pdf.line(5.0, 5.0, 205.0, 5.0) # top one
    pdf.line(5.0, 292.0, 205.0, 292.0) # bottom one
    pdf.line(5.0, 5.0, 5.0, 292.0) # left one
    pdf.line(205.0, 5.0, 205.0, 292.0) # right one
    pdf.set_font("Arial", 'B', size=17)
    pdf.cell(200, 10, "Appointment Confirmation Letter", ln=1, align='C')
    pdf.set_font("Arial", size=8)
    pdf.cell(350, 8, txt="Appointment-Number:- " + str(apoint.app_id),  ln=1, align='C')
    pdf.set_font("Arial", size=8)
    pdf.cell(350, 10, txt="Date:- " + str(apoint.book_time), ln=1, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, txt="Dear,"+str(user.name), ln=1, align='L')
    pdf.cell(200, 8, txt="          This is a reminder that your appointment is scheduled on date.", ln=1, align='L')
    pdf.cell(200, 10, "If you can not make this appointment, please call our office at 01224-789456 at least"
                      " 24 hours prior to this ", ln=5, align='L')
    pdf.cell(200, 10, "appointment. We would be happy to rescheduled your appointment for "
                      "a more convenient time.", ln=5, align='L')
    pdf.cell(200, 10, "Refer below details:-", ln=5, align='L')
    pdf.set_font("Arial", 'B', size=15)
    pdf.cell(190, 8, "Patient Details", 1, ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, txt="Patient Name" + '  =' + ' '*10 + str(apoint.pat_name), ln=1, align='L')
    pdf.cell(100, 10, txt="Patient Age" + '  =' + ' '*10 + str(apoint.pat_age), ln=1, align='L')
    pdf.cell(100, 10, txt="Patient Gender" + '  =' + ' '*10 + str(apoint.pat_gender), ln=1, align='L')
    pdf.set_font("Arial", 'B', size=15)
    pdf.cell(190, 8, "Doctor's Details", 1, ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, txt="Name" + '  =' + ' '*10 + str(doctor.first_name + '  ' + doctor.last_name), ln=1, align='L')
    pdf.cell(100, 10, txt="Speciality" + '  =' + ' '*10 + str(doctor.speciality), ln=1, align='L')
    pdf.cell(100, 10, txt="Address" + '  =' + ' '*10 + str(doctor.address), ln=1, align='L')
    pdf.cell(100, 10, txt="Date & Time" + '  =' + ' '*10 + str(apoint.app_time), ln=1, align='L')
    pdf.cell(300, 70, txt="Note:- Please be on time", ln=1, align='C')
    pdf.output("Appointment_{}.pdf".format(user.name))


@user.route('/user/appointment', methods=['POST'])
def book_appointment():
    if session.get('EMAIL'):
        formdata = request.get_json()
        pat_name = formdata.get("PATIENT NAME")
        pat_age = formdata.get("PATIENT AGE")
        pat_gender = formdata.get("PATIENT GENDER")
        doc_id = formdata.get("DOCTOR ID")
        time = formdata.get("APPOINTMENT TIME")

        doctor = Doctor.query.filter_by(id=doc_id).first()
        user = User.query.filter(session.get('EMAIL') == User.email).first()
        if doctor:
            from datetime import datetime
            available = datetime.strptime(str(doctor.available_time), '%Y-%d-%m %H:%M:%S')
            app_time = datetime.strptime(str(time), '%Y-%d-%m %H:%M:%S')
            last_available = datetime.strptime(str(doctor.lat_available), '%Y-%d-%m %H:%M:%S')
            d1 = available.time()
            d2 = app_time.time()
            d3 = last_available.time()
            print(d1, d2, d3)
            if d1 < d2 < d3:
                apoint = Appointment(user=user.reg_id, pat_name=pat_name, pat_age=pat_age, pat_gender=pat_gender,
                                     doctor=doc_id, app_time=time)
                db.session.add(apoint)
                db.session.commit()
                creat_pdf(doctor, user, apoint)
                app.config["CLIENT_PDF"] = 'F:\\postman\\Doctor'
                path = 'F:\\postman\\Doctor'
                pdf_filename = "Appointment_{}.pdf".format(user.name)
                try:
                    return send_from_directory(app.config["CLIENT_PDF"], filename=pdf_filename,
                                               path=path, as_attachment=True)
                except FileNotFoundError:
                    return 'abort(404)'
               # return jsonify({"SUCCESS": "Appointment successfully booked"})
            else:
                return jsonify({"ERROR": "Doctor is not available in this time"})
        else:
            return jsonify({"ERROR": "Invalid doctor id"})
    else:
        return jsonify({"ERROR": "You need to login first"})


@user.route('user/logout')
def logout():
    if session.get('EMAIL'):
        session.pop('EMAIL')
        return jsonify({"SUCCESS": "Successfully logout"})
    return jsonify({"ERROR": "Login first"})

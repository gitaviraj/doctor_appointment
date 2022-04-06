from app_config import app, db
from flask import request, jsonify, Blueprint, session
from models import Doctor
import json
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

auth = Blueprint('auth', __name__)


def validate_details(reqbody):
    error = {}
    if not reqbody.__contains__('FIRST_NAME'):
        error["First_NAME"] = "Doctor first name required..."
    if not reqbody.__contains__('LAST_NAME'):
        error["LAST_NAME"] = "Doctor last name required..."
    if not reqbody.__contains__('MOBILE'):
        error["MOBILE"] = "Mobile number required..."
    if not reqbody.__contains__('EMAIL'):
        error["EMAIL"] = "Email  required..."
    if not reqbody.__contains__('QUALIFICATION'):
        error["QUALIFICATION"] = "Qualification required..."
    if not reqbody.__contains__('SPECIALIZATION'):
        error["SPECIALIZATION"] = "Specialization required..."
    if not reqbody.__contains__('ADDRESS'):
        error["ADDRESS"] = "Address required..."
    if not reqbody.__contains__('STATUS'):
        error["STATUS"] = "Status required..."
    if not reqbody.__contains__('AVAILABLE_DATE'):
        error["AVAILABLE_DATE"] = "Available date required..."
    if not reqbody.__contains__('AVAILABLE_TIME'):
        error["AVAILABLE_TIME"] = "Available time required..."
    if not reqbody.__contains__('AVAILABLE_TILL'):
        error["AVAILABLE_TILL"] = "Last available time required..."
    return error


@auth.route('/doctor', methods=['POST'])
@jwt_required()
def add_doctor():
    formdata = request.get_json()
    print(formdata)
    fname = formdata.get("FIRST_NAME")
    lname = formdata.get("LAST_NAME")
    mobile = formdata.get("MOBILE")
    email = formdata.get("EMAIL")
    qual = formdata.get("QUALIFICATION")
    special = formdata.get("SPECIALIZATION")
    address = formdata.get("ADDRESS")
    status = formdata.get("STATUS")
    date = formdata.get("AVAILABLE_DATE")
    time1 = formdata.get("AVAILABLE_TIME")
    time2 = formdata.get("AVAILABLE_TILL")

    check = Doctor.query.filter(email == Doctor.email).first()
    if check:
        return jsonify({"ERROR": "EMAIL ALREADY PRESENT"})

    if not status == 'ACTIVE' or status == 'INACTIVE':
        return jsonify({"ERROR": "PLEASE INSERT VALID STATUS ACTIVE OR INACTIVE"})

    errors = validate_details(formdata)
    if errors:
        return json.dumps(errors)
    else:
        doctor = Doctor(first_name=fname.title(), last_name=lname.title(), mobile=mobile, email=email, qualification=qual,
                        speciality=special.title(), address=address.title(), status=status, available_date=date,
                        available_time=time1,
                        lat_available=time2)
        db.session.add(doctor)
        db.session.commit()
        return jsonify({"SUCCESS": "DOCTOR ADDED"})


@auth.route('/doctor/search/fname/<fname>')
def search_doctor_by_first_name(fname):
    if session.get('EMAIL'):
        doctors = Doctor.query.filter(fname.title() == Doctor.first_name).all()
        doctor_list = []
        if doctors:
            for doc in doctors:
                doctor = {
                            "NAME": doc.first_name + " " + doc.last_name,
                            "QUALIFICATION": doc.qualification,
                            "SPECIALIZATION": doc.speciality,
                            "ADDRESS": doc.address,
                            " AVAILABLE DATE": str(doc.available_date),
                            "AVAILABLE_TIME": str(doc.available_time) + '  to  ' + str(doc.lat_available)
                         }
                doctor_list.append(doctor)
                print(doctor_list)
            return json.dumps(doctor_list)
        else:
            return jsonify({"ERROR": "Doctor doesn't found"})
    else:
        return jsonify({"ERROR": "You need to login first"})


@auth.route('/doctor/search/lname/<lname>')
def search_doctor_by_last_name(lname):
    if session.get('EMAIL'):
        doctors = Doctor.query.filter(lname.title() == Doctor.first_name).all()
        doctor_list = []
        if doctors:
            for doc in doctors:
                doctor = {
                          "NAME": doc.first_name + " " + doc.last_name,
                          "QUALIFICATION": doc.qualification,
                          "SPECIALIZATION": doc.speciality,
                          "ADDRESS": doc.address,
                          " AVAILABLE DATE": str(doc.available_date),
                          "AVAILABLE TIME": str(doc.available_time) + '  to  ' + str(doc.lat_available)
                          }
                doctor_list.append(doctor)
            return json.dumps(doctor_list)
        else:
            return jsonify({"ERROR": "Doctor doesn't found"})
    else:
        return jsonify({"ERROR": "You need to login first"})


@auth.route('/doctor/search/speciality/<speciality>')
def search_doctor_by_speciality(speciality):
    if session.get('EMAIL'):
        Doctors = Doctor.query.all()
        doctor_list = []
        for doc in Doctors:
            if doc.speciality.__contains__(speciality.title()):
                doctor = {"NAME": doc.first_name + " " + doc.last_name,
                          "QUALIFICATION": doc.qualification,
                          "SPECIALIZATION": doc.speciality,
                          "ADDRESS": doc.address,
                          " AVAILABLE DATE": str(doc.available_date),
                          "AVAILABLE TIME": str(doc.available_time) + '  to  ' + str(doc.lat_available)}
                doctor_list.append(doctor)

        if doctor_list:
            return json.dumps(doctor_list)
        else:
            return jsonify({"ERROR": "No doctor found with this specialization"})
    else:
        return jsonify({"ERROR": "You need to login first"})


@auth.route('/doctor/search/area/<area>')
def search_doctor_by_area(area):
    if session.get('EMAIL'):
        Doctors = Doctor.query.all()
        doctor_list = []
        print(area.title())
        for doc in Doctors:
            if doc.address.__contains__(area.title()):
                doctor = {
                            "NAME": doc.first_name + " " + doc.last_name,
                            "QUALIFICATION": doc.qualification,
                            "SPECIALIZATION": doc.speciality,
                            "ADDRESS": doc.address,
                            " AVAILABLE DATE": str(doc.available_date),
                            "AVAILABLE TIME": str(doc.available_time) + '  to  ' + str(doc.lat_available)
                         }
                doctor_list.append(doctor)

        if doctor_list:
            return json.dumps(doctor_list)
        else:
            return jsonify({"ERROR": "No doctor found with this specialization"})
    else:
        return jsonify({"ERROR": "You need to login first"})


@auth.route('/doctor/update/<int:id>', methods=['POST'])
@jwt_required()
def update_doctor_details(id):
    formdata = request.get_json()
    print(formdata)
    doctor = Doctor.query.filter_by(id=id).first()
    if doctor:
        if formdata.get("FIRST_NAME"):
            doctor.first_name = formdata.get("FIRST_NAME")
        if formdata.get("LAST_NAME"):
            doctor.last_name = formdata.get("LAST_NAME")
        if formdata.get("MOBILE"):
            doctor.mobile = formdata.get("MOBILE")
        if formdata.get("EMAIL"):
            doctor.email = formdata.get("EMAIL")
        if formdata.get("QUALIFICATION"):
            doctor.qualification = formdata.get("QUALIFICATION")
        if formdata.get("SPECIALIZATION"):
            doctor.speciality = formdata.get("SPECIALIZATION")
        if formdata.get("ADDRESS"):
            doctor.address = formdata.get("ADDRESS")
        if formdata.get("STATUS"):
            doctor.status = formdata.get("STATUS")
        if formdata.get("AVAILABLE_DATE"):
            doctor.available_time = formdata.get("AVAILABLE_DATE")
        if formdata.get("AVAILABLE_TIME"):
            doctor.available_time = formdata.get("AVAILABLE_TIME")
        if formdata.get("AVAILABLE_TILL"):
            doctor.lat_available = formdata.get("AVAILABLE_TILL")
        db.session.commit()
        return jsonify({"SUCCESS": "Details successfully updated"})
    else:
        return jsonify({"ERROR": "Doctor doesn't found"})


@app.route('/api/token', methods=["POST"])
def create_token():
    username = request.json.get("USERNAME", None)
    password = request.json.get("PASSWORD", None)
    print(username, password)
    if username == 'admin' and password == '123456':
        identity = (username, password)
        accesstoken = create_access_token(identity=identity)
        refreshtoken = create_refresh_token(identity=identity)
        return jsonify({"ACCESS_TOKEN": accesstoken, "REFRESH_TOKEN": refreshtoken, "USERNAME": username})
    return jsonify({"ERROR": "Invalid Input"})


@app.route('/api/token/refresh')
@jwt_required(refresh=True)
def aceess_token_by_refresh():
    curent_user_id = get_jwt_identity()
    accestoken = create_access_token(identity=curent_user_id)
    return jsonify({"ACCESS_TOKEN": accestoken})


@auth.route('/api', methods=['GET'])
def test_sample_api():
    return "API is working.....Avinash"

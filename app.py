import os
from flask import Flask, request, abort, jsonify, render_template
from flask import url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
    setup_db,
    Doctor,
    Patient,
    Appointment,
    db_drop_and_create_all,
)
import datetime
from auth import requires_auth, AuthError
import json


def create_app(test_config=None):
    # And configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    # Controllers.

    """'
    Frontend homepage contoller
    """

    @app.route("/")
    def index():
        audience = os.getenv("0AUTH_API_AUDIENCE", "clinical_appointments")
        client_id = os.getenv(
            "0AUTH_CLIENT_ID", "8S3ud1J376cY6EsQ2AFLspCiVazKEjeg"
        )
        return render_template(
            "pages/home.html", audience=audience, client_id=client_id
        )

    """'
    Frontend callback contoller
    """

    @app.route("/login/token")
    def callback_url():
        return render_template("pages/login.html")

    """'
    An endpoint to handle GET requests
    for all available doctors.
    """

    @app.route("/doctors")
    @requires_auth("get:doctors")
    def fetch_all_doctors(jwt):
        doctors = Doctor.query.order_by(Doctor.id).all()
        formatted_doctors = [doctor.format() for doctor in doctors]

        if len(formatted_doctors) == 0:
            abort(404)

        return jsonify({"success": True, "doctors": formatted_doctors})

    """'
    An endpoint to handle GET requests
    by doctor id.
    """

    @app.route("/doctors/<int:id>")
    @requires_auth("get:doctors")
    def fetch_doctor_by_doctor_id(jwt, id):
        doctor = Doctor.query.filter(Doctor.id == id).one_or_none()

        if doctor is None:
            abort(404)

        formatted_doctor = [doctor.format()]

        return jsonify({"success": True, "doctor": formatted_doctor})

    """'
    An endpoint to handle GET requests
    for all available patients.
    """

    @app.route("/patients")
    @requires_auth("get:patients")
    def fetch_all_patients(jwt):
        patients = Patient.query.order_by(Patient.id).all()
        formatted_patients = [patient.format() for patient in patients]

        if len(formatted_patients) == 0:
            abort(404)

        return jsonify({"success": True, "patients": formatted_patients})

    """'
    An endpoint to handle GET requests
    by patient id.
    """

    @app.route("/patients/<int:id>")
    @requires_auth("get:patients")
    def fetch_patient_by_patient_id(jwt, id):
        patient = Patient.query.filter(Patient.id == id).one_or_none()

        if patient is None:
            abort(404)

        formatted_patient = [patient.format()]

        return jsonify({"success": True, "patient": formatted_patient})

    """'
    An endpoint to handle GET requests
    for all available appointments.
    """

    @app.route("/appointments")
    @requires_auth("get:appointments")
    def fetch_all_appointments(jwt):
        appointments = Appointment.query.order_by(Appointment.start_time).all()
        formatted_appointments = [
            appointment.format() for appointment in appointments
        ]

        if len(formatted_appointments) == 0:
            abort(404)

        return jsonify(
            {"success": True, "appointments": formatted_appointments}
        )

    """'
    An endpoint to handle GET requests
    by appointment id.
    """

    @app.route("/appointments/<int:id>")
    @requires_auth("get:appointments")
    def fetch_appointment_by_appointment_id(jwt, id):
        appointment = Appointment.query.filter(
            Appointment.id == id
        ).one_or_none()

        if appointment is None:
            abort(404)

        formatted_appointment = [appointment.format()]

        return jsonify({"success": True, "appointment": formatted_appointment})

    """
    Create a POST endpoint to create new doctors.
    """

    @app.route("/doctors", methods=["POST"])
    @requires_auth("post:doctors")
    def add_new_doctor(jwt):
        content = request.get_json()
        first_name = content.get("first_name")
        last_name = content.get("last_name")
        address = content.get("address")
        city = content.get("city")
        state = content.get("state")
        phone_no = content.get("phone_no")
        degree = content.get("degree")
        speciality = content.get("speciality")

        if len(phone_no) != 10:
            abort(400, "Phone number should be 10 digits")

        try:
            doctor = Doctor(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                state=state,
                phone_no=phone_no,
                degree=degree,
                speciality=speciality,
            )
            doctor.insert()
            formatted_doctor = [doctor.format()]

            return jsonify(
                {
                    "success": True,
                    "created": doctor.id,
                    "doctor": formatted_doctor,
                }
            )

        except:
            abort(422)

    """
    Create a POST endpoint to create new patients.
    """

    @app.route("/patients", methods=["POST"])
    @requires_auth("post:patients")
    def add_new_patient(jwt):
        content = request.get_json()
        first_name = content.get("first_name")
        last_name = content.get("last_name")
        address = content.get("address")
        city = content.get("city")
        state = content.get("state")
        phone_no = content.get("phone_no")
        date_of_birth = content.get("date_of_birth")

        if len(phone_no) != 10:
            abort(400, "Phone number should be 10 digits")

        try:
            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                state=state,
                phone_no=phone_no,
                date_of_birth=date_of_birth,
            )
            patient.insert()
            formatted_patient = [patient.format()]

            return jsonify(
                {
                    "success": True,
                    "created": patient.id,
                    "patient": formatted_patient,
                }
            )

        except:
            abort(422)

    """'
    An endpoint to handle POST requests
    for the appointment.
    """

    @app.route("/appointments", methods=["POST"])
    @requires_auth("post:appointments")
    def add_new_appointment(jwt):
        content = request.get_json()
        doctor_id = content.get("doctor_id")
        patient_id = content.get("patient_id")
        start_time = content.get("start_time")

        if (
            datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") <
            datetime.datetime.now()
        ):
            abort(400, "Incorrect date and time")

        try:
            appointment = Appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                start_time=start_time,
            )
            appointment.insert()
            formatted_appointment = [appointment.format()]

            return jsonify(
                {
                    "success": True,
                    "created": appointment.id,
                    "appointment": formatted_appointment,
                }
            )

        except Exception as e:
            abort(422)

    """'
    An endpoint to handle PATCH requests
    for the patient.
    """

    @app.route("/patients/<int:patient_id>", methods=["PATCH"])
    @requires_auth("patch:patients")
    def edit_patient(jwt, patient_id):
        patient = Patient.query.filter(Patient.id == patient_id).one_or_none()

        if patient is None:
            abort(404)

        content = request.get_json()
        if len(content.get("phone_no")) != 10:
            abort(400, "Phone number should be 10 digits")

        try:
            patient.first_name = content.get("first_name")
            patient.last_name = content.get("last_name")
            patient.address = content.get("address")
            patient.city = content.get("city")
            patient.state = content.get("state")
            patient.phone_no = content.get("phone_no")
            patient.date_of_birth = content.get("date_of_birth")
            patient.update()
            formatted_patient = [patient.format()]

            return jsonify({"success": True, "patient": formatted_patient})

        except:
            abort(422)

    """'
    An endpoint to handle PATCH requests
    for the appointment.
    """

    @app.route("/appointments/<int:appointment_id>", methods=["PATCH"])
    @requires_auth("patch:appointments")
    def edit_appointment(jwt, appointment_id):
        appointment = Appointment.query.filter(
            Appointment.id == appointment_id
        ).one_or_none()

        if appointment is None:
            abort(404)

        content = request.get_json()
        if (
            datetime.datetime.strptime(
                content.get("start_time"), "%Y-%m-%d %H:%M:%S"
            ) <
            datetime.datetime.now()
        ):
            abort(400, "Incorrect date and time")

        try:
            appointment.doctor_id = content.get("doctor_id")
            appointment.patient_id = content.get("patient_id")
            appointment.start_time = content.get("start_time")
            appointment.update()
            formatted_appointment = [appointment.format()]

            return jsonify(
                {"success": True, "appointment": formatted_appointment}
            )

        except:
            abort(422)

    """
    An endpoint to handle DELETE requests
    for the appointments.
    """

    @app.route("/patients/<int:id>", methods=["DELETE"])
    @requires_auth("delete:patients")
    def delete_patient(jwt, id):
        patient = Patient.query.filter(Patient.id == id).one_or_none()

        if patient is None:
            abort(404)

        try:
            patient.delete()
            return jsonify({"success": True, "deleted": patient.id})

        except:
            abort(422)

    """
    An endpoint to Truncate all tables
    """

    @app.route("/truncate", methods=["DELETE"])
    @requires_auth("delete:patients")
    def truncate_tables(jwt):
        try:
            db_drop_and_create_all()
            return jsonify({"success": True})

        except:
            abort(422)

    # Error Handling
    """
    Example error handling for unprocessable entity
    """

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "unprocessable"}
            ),
            422,
        )

    """
    Example error handling for 404 not found entity
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Not found"}),
            404,
        )

    """
    Example error handling for 400 invalid request
    """

    @app.errorhandler(400)
    def invalid_request(error):
        return (
            jsonify(
                {"success": False, "error": 400, "message": error.description}
            ),
            400,
        )

    """
    Example error handling for auth error
    """

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": error.status_code,
                    "message": error.error["description"],
                }
            ),
            error.status_code,
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run()

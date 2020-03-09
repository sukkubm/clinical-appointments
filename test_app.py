import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Doctor, Patient, Appointment
from unittest.mock import patch


class ClinicalAppointmentsTestCase(unittest.TestCase):
    """This class represents the clinical appointments test case"""

    decoded_jwt_mock = {
        "permissions": [
            "get:appointments",
            "get:doctors",
            "get:patients",
            "patch:appointments",
            "patch:patients",
            "post:doctors",
            "post:appointments",
            "post:patients",
            "delete:patients",
        ]
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "clinical_appointments1"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "postgres", "password", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            doctor1 = Doctor(
                first_name="Harry",
                last_name="Potter",
                address="41, hampstead road",
                city="Sydney",
                state="NSW",
                phone_no="0877177774",
                degree="MBBS MD",
                speciality="Dermatologist",
            )
            doctor1.insert()
            self.doctor1_id = doctor1.id
            doctor2 = Doctor(
                first_name="Tom",
                last_name="Jerry",
                address="41, merindah road",
                city="Sydney",
                state="NSW",
                phone_no="0987778432",
                degree="MBBS MD",
                speciality="Cardiologist",
            )
            doctor2.insert()
            self.doctor2_id = doctor2.id
            patient1 = Patient(
                first_name="Simi",
                last_name="Jain",
                address="41, ersnt road",
                city="Sydney",
                state="NSW",
                phone_no="0455536663",
                date_of_birth="2009-01-03",
            )
            patient1.insert()
            self.patient1_id = patient1.id
            patient2 = Patient(
                first_name="Roger",
                last_name="Federer",
                address="120, station road",
                city="Sydney",
                state="NSW",
                phone_no="0765636533",
                date_of_birth="1995-07-13",
            )
            patient2.insert()
            self.patient2_id = patient2.id
            appointment1 = Appointment(
                doctor_id=self.doctor1_id,
                patient_id=self.patient1_id,
                start_time="2020-03-10 19:15:48",
            )
            appointment1.insert()
            self.appointment1_id = appointment1.id
            appointment2 = Appointment(
                doctor_id=self.doctor2_id,
                patient_id=self.patient2_id,
                start_time="2020-04-12 12:45:35",
            )
            appointment2.insert()
            self.appointment2_id = appointment2.id

            self.doctor3 = {
                "first_name": "Will",
                "last_name": "Smith",
                "address": "113, Josh street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "0435627165",
                "degree": "BDS",
                "speciality": "Dentist",
            }

            self.wrong_add_doctor = {
                "first_name": "Test",
                "address": "113, Josh street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "0435627165",
                "degree": "BDS",
                "speciality": "Dentist",
            }

            self.patient3 = {
                "first_name": "Evelyn",
                "last_name": "Than",
                "address": "88, George street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "0887777777",
                "date_of_birth": "2010-06-19",
            }

            self.edit_patient = {
                "first_name": "Simi",
                "last_name": "Jain",
                "address": "98, arthur street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "0455536663",
                "date_of_birth": "2009-01-03",
            }

            self.wrong_add_patient = {
                "first_name": "Evelyn",
                "address": "88, George street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "0888888888",
                "date_of_birth": "2010-06-19",
            }

            self.wrong_edit_patient = {
                "first_name": "Simi",
                "last_name": "Jain",
                "address": "98, arthur street",
                "city": "Sydney",
                "state": "NSW",
                "phone_no": "04555363",
                "date_of_birth": "2009-01-03",
            }

            self.appointment3 = {
                "doctor_id": self.doctor1_id,
                "patient_id": self.patient2_id,
                "start_time": "2020-03-15 16:15:48",
            }

            self.edit_appointment = {
                "doctor_id": self.doctor1_id,
                "patient_id": self.patient1_id,
                "start_time": "2020-03-20 10:15:48",
            }

            self.wrong_add_appointment = {
                "doctor_id": 1,
                "patient_id": self.patient2_id,
                "start_time": "2020-03-15 16:15:48",
            }

            self.wrong_edit_appointment = {
                "doctor_id": self.doctor1_id,
                "patient_id": self.patient1_id,
                "start_time": "2020-02-01 10:15:48",
            }

    def tearDown(self):
        """Executed after reach test"""
        self._clear_appointments_data_from_db()
        self._clear_doctors_data_from_db()
        self._clear_patients_data_from_db()

    def _clear_doctors_data_from_db(self):
        self._clear_data_from_db(Doctor)

    def _clear_patients_data_from_db(self):
        self._clear_data_from_db(Patient)

    def _clear_appointments_data_from_db(self):
        self._clear_data_from_db(Appointment)

    def _clear_data_from_db(self, modelName):
        with self.app.app_context():
            self.db.session.query(modelName).delete()
            self.db.session.commit()

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_all_doctors(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for doctors"""
        res = self.client().get("/doctors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["doctors"]), 2)
        doctor = data["doctors"][0]
        self.assertEqual(doctor["first_name"], "Harry")
        self.assertEqual(doctor["last_name"], "Potter")
        self.assertEqual(doctor["address"], "41, hampstead road")
        self.assertEqual(doctor["city"], "Sydney")
        self.assertEqual(doctor["state"], "NSW")
        self.assertEqual(doctor["phone_no"], "0877177774")
        self.assertEqual(doctor["degree"], "MBBS MD")
        self.assertEqual(doctor["speciality"], "Dermatologist")
        doctor = data["doctors"][1]
        self.assertEqual(doctor["first_name"], "Tom")
        self.assertEqual(doctor["last_name"], "Jerry")
        self.assertEqual(doctor["address"], "41, merindah road")
        self.assertEqual(doctor["city"], "Sydney")
        self.assertEqual(doctor["state"], "NSW")
        self.assertEqual(doctor["phone_no"], "0987778432")
        self.assertEqual(doctor["degree"], "MBBS MD")
        self.assertEqual(doctor["speciality"], "Cardiologist")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_doctors_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if doctor does not exist"""
        self._clear_appointments_data_from_db()
        self._clear_doctors_data_from_db()
        res = self.client().get("/doctors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_data_by_doctor_id(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for doctor by doctor id"""
        doctor = Doctor.query.first()
        res = self.client().get(f"/doctors/{doctor.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["doctor"]), 1)
        doctor = data["doctor"][0]
        self.assertEqual(doctor["first_name"], "Harry")
        self.assertEqual(doctor["last_name"], "Potter")
        self.assertEqual(doctor["address"], "41, hampstead road")
        self.assertEqual(doctor["city"], "Sydney")
        self.assertEqual(doctor["state"], "NSW")
        self.assertEqual(doctor["phone_no"], "0877177774")
        self.assertEqual(doctor["degree"], "MBBS MD")
        self.assertEqual(doctor["speciality"], "Dermatologist")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_doctor_id_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if doctor does not exist"""
        res = self.client().get("/doctors/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_all_patients(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for patients"""
        res = self.client().get("/patients")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["patients"]), 2)
        patient = data["patients"][0]
        self.assertEqual(patient["first_name"], "Simi")
        self.assertEqual(patient["last_name"], "Jain")
        self.assertEqual(patient["address"], "41, ersnt road")
        self.assertEqual(patient["city"], "Sydney")
        self.assertEqual(patient["state"], "NSW")
        self.assertEqual(patient["phone_no"], "0455536663")
        self.assertEqual(
            patient["date_of_birth"], "Sat, 03 Jan 2009 00:00:00 GMT"
        )
        patient = data["patients"][1]
        self.assertEqual(patient["first_name"], "Roger")
        self.assertEqual(patient["last_name"], "Federer")
        self.assertEqual(patient["address"], "120, station road")
        self.assertEqual(patient["city"], "Sydney")
        self.assertEqual(patient["state"], "NSW")
        self.assertEqual(patient["phone_no"], "0765636533")
        self.assertEqual(
            patient["date_of_birth"], "Thu, 13 Jul 1995 00:00:00 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_patients_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if patients not found"""
        self._clear_appointments_data_from_db()
        self._clear_patients_data_from_db()
        res = self.client().get("/patients")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_data_by_patient_id(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for patient by patient id"""
        patient = Patient.query.first()
        res = self.client().get(f"/patients/{patient.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["patient"]), 1)
        patient = data["patient"][0]
        self.assertEqual(patient["first_name"], "Simi")
        self.assertEqual(patient["last_name"], "Jain")
        self.assertEqual(patient["address"], "41, ersnt road")
        self.assertEqual(patient["city"], "Sydney")
        self.assertEqual(patient["state"], "NSW")
        self.assertEqual(patient["phone_no"], "0455536663")
        self.assertEqual(
            patient["date_of_birth"], "Sat, 03 Jan 2009 00:00:00 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_patient_id_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if patient does not exist"""
        res = self.client().get("/patients/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_all_appointments(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for appointments"""
        res = self.client().get("/appointments")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["appointments"]), 2)
        appointment = data["appointments"][0]
        self.assertEqual(appointment["doctor_id"], self.doctor1_id)
        self.assertEqual(appointment["patient_id"], self.patient1_id)
        self.assertEqual(
            appointment["start_time"], "Tue, 10 Mar 2020 19:15:48 GMT"
        )
        appointment = data["appointments"][1]
        self.assertEqual(appointment["doctor_id"], self.doctor2_id)
        self.assertEqual(appointment["patient_id"], self.patient2_id)
        self.assertEqual(
            appointment["start_time"], "Sun, 12 Apr 2020 12:45:35 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_appointments_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if appointments not found"""
        self._clear_appointments_data_from_db()
        res = self.client().get("/appointments")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_get_data_by_appointment_id(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to fetch the data for appointment by appointment  id"""
        appointment = Appointment.query.first()
        res = self.client().get(f"/appointments/{appointment.id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["appointment"]), 1)
        appointment = data["appointment"][0]
        self.assertEqual(appointment["doctor_id"], self.doctor1_id)
        self.assertEqual(appointment["patient_id"], self.patient1_id)
        self.assertEqual(
            appointment["start_time"], "Tue, 10 Mar 2020 19:15:48 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_if_appointment_id_not_found(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to see if appointment does not exist"""
        res = self.client().get("/appointments/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_add_new_doctor(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test for adding new doctor"""
        res = self.client().post("/doctors", json=self.doctor3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["doctor"]), 1)
        doctor = data["doctor"][0]
        self.assertEqual(doctor["first_name"], "Will")
        self.assertEqual(doctor["last_name"], "Smith")
        self.assertEqual(doctor["address"], "113, Josh street")
        self.assertEqual(doctor["city"], "Sydney")
        self.assertEqual(doctor["state"], "NSW")
        self.assertEqual(doctor["phone_no"], "0435627165")
        self.assertEqual(doctor["degree"], "BDS")
        self.assertEqual(doctor["speciality"], "Dentist")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_422_if_doctor_creation_fails(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        res = self.client().post("/doctors", json=self.wrong_add_doctor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_add_new_patient(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test for adding new patient"""
        res = self.client().post("/patients", json=self.patient3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["patient"]), 1)
        patient = data["patient"][0]
        self.assertEqual(patient["first_name"], "Evelyn")
        self.assertEqual(patient["last_name"], "Than")
        self.assertEqual(patient["address"], "88, George street")
        self.assertEqual(patient["city"], "Sydney")
        self.assertEqual(patient["state"], "NSW")
        self.assertEqual(patient["phone_no"], "0887777777")
        self.assertEqual(
            patient["date_of_birth"], "Sat, 19 Jun 2010 00:00:00 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_422_if_patient_creation_fails(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        res = self.client().post("/patients", json=self.wrong_add_patient)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_add_new_appointment(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test for adding new appointment"""
        res = self.client().post("/appointments", json=self.appointment3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["appointment"]), 1)
        appointment = data["appointment"][0]
        self.assertEqual(appointment["doctor_id"], self.doctor1_id)
        self.assertEqual(appointment["patient_id"], self.patient2_id)
        self.assertEqual(
            appointment["start_time"], "Sun, 15 Mar 2020 16:15:48 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_422_if_appointment_creation_fails(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        res = self.client().post(
            "/appointments", json=self.wrong_add_appointment
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_edit_patient(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test for editing patient"""
        patient = Patient.query.first()
        res = self.client().patch(
            f"/patients/{patient.id}", json=self.edit_patient
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["patient"]), 1)
        patient = data["patient"][0]
        self.assertEqual(patient["first_name"], "Simi")
        self.assertEqual(patient["last_name"], "Jain")
        self.assertEqual(patient["address"], "98, arthur street")
        self.assertEqual(patient["city"], "Sydney")
        self.assertEqual(patient["state"], "NSW")
        self.assertEqual(patient["phone_no"], "0455536663")
        self.assertEqual(
            patient["date_of_birth"], "Sat, 03 Jan 2009 00:00:00 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_400_if_patient_edit_fails(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to check if patient edit fails"""
        patient = Patient.query.first()
        res = self.client().patch(
            f"/patients/{patient.id}", json=self.wrong_edit_patient
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Phone number should be 10 digits")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_edit_appointment(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test for editing appointment"""
        appointment = Appointment.query.first()
        res = self.client().patch(
            f"/appointments/{appointment.id}", json=self.edit_appointment
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["appointment"]), 1)
        appointment = data["appointment"][0]
        self.assertEqual(appointment["doctor_id"], self.doctor1_id)
        self.assertEqual(appointment["patient_id"], self.patient1_id)
        self.assertEqual(
            appointment["start_time"], "Fri, 20 Mar 2020 10:15:48 GMT"
        )

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_400_if_appointment_edit_fails(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to check if appointment edit fails"""
        appointment = Appointment.query.first()
        res = self.client().patch(
            f"/appointments/{appointment.id}", json=self.wrong_edit_appointment
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Incorrect date and time")

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_delete_patient(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to check for deleting patient"""
        res = self.client().delete(f"/patients/{self.patient1_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], self.patient1_id)

    @patch("auth.get_token_auth_header", return_value="mock_token")
    @patch("auth.verify_decode_jwt", return_value=decoded_jwt_mock)
    def test_404_delete_patient(
        self, mock_get_token_auth_header, mock_verify_decode_jwt
    ):
        """Test to check if patient cant be deleted"""
        res = self.client().delete("/patients/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

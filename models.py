import os
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

local_db_path = "postgres://{}:{}@{}/{}".format(
    "postgres", "password", "localhost:5432", "clinical_appointments"
)
database_path = os.getenv("DATABASE_URL", local_db_path)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(32)
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(db.Model):
    __abstract__ = True

    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    phone_no = Column(String, nullable=False)
    UniqueConstraint("phone")


"""
Doctor
a persistent doctor entity, extends the User SQLAlchemy Model
"""


class Doctor(User):
    __tablename__ = "doctors"

    degree = Column(String)
    speciality = Column(String)
    appointments = relationship("Appointment", back_populates="doctor")

    """
    insert()
        inserts a new model into a database
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone_no": self.phone_no,
            "degree": self.degree,
            "speciality": self.speciality,
        }


"""
Patient
a persistent patient entity, extends the User SQLAlchemy Model
"""


class Patient(User):
    __tablename__ = "patients"

    date_of_birth = Column(Date)
    appointments = relationship("Appointment", back_populates="patient")

    """
    insert()
        inserts a new model into a database
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
    """

    def update(self):
        db.session.commit()

    """
    delete()
        deletes a new model into a database
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone_no": self.phone_no,
            "date_of_birth": self.date_of_birth,
        }


"""
Appointment bookings
"""


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column("doctor_id", Integer, ForeignKey("doctors.id"))
    patient_id = Column("patient_id", Integer, ForeignKey("patients.id"))
    start_time = Column("start_time", DateTime)
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    """
    insert()
        inserts a new model into a database
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
    """

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "start_time": self.start_time,
        }

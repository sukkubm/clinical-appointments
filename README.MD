#Capstone Project - Clinical Appointments

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

source env/bin/activate

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./heroku_capestone` directory first ensure you are working using your created virtual environment.
run ``` pip install -r requirements ```
Update the `setup.sh`. 
To run the server, execute:

```bash
   ./setup.sh
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Endpoint documentation
 Please find below the documentation link forAPI endpoints.
 https://documenter.getpostman.com/view/10361626/SzRw2Bea?version=latest

## Auth0 Roles
 -Patient
    - Can view doctors, patients and appointments
    - Can post patients and appointments
    - Can edit patients and appointments

 -Doctor
    - Has all the permissions of patients and...
    - Can post doctors
    - Can delete patients

## Steps to create JWT token

 Please find below credentials for creating JWT token

    Doctor Role:
     Username - yelofi5655@kamismail.com
     password - Junk111!!

    Patient Role:
     Username - wetomi7239@link3mail.com
     Password - Junk111!!

 Please follow below steps to create JWT token
    - Go to website base url (https://udacitycapestonesukku.herokuapp.com)
    - Click login button and use the above credentials to login as doctor or patient
    - Once logged in, JWT token is printed on the login page and this can be used in postman
    - In order to logout, click the logout button

## Testing the API

 ## To run the tests, run
 dropdb clinical_appointments_test
 createdb clinical_appointments_test
 python test_app.py

 ## To test the endpoints with Postman
    - Import the postman collection './starter/postman_collection.json'
    - Generate new JWT token if expired using above credentials 
    - send a `DELETE` request to https://udacitycapestonesukku.herokuapp.com/truncate using the JWT token (This step clears the database for the tests)
    - Right-clicking the collection folder for Doctor and Patient, navigate to the authorization tab, and include the JWT in the token field
    - Run the postman collection

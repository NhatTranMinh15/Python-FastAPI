# Python FastAPI Assignment
A FastAPI sample application to learn how to use FastAPI with SQLAlchemy and PostgreSQL.

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- ...

## Default Account
To login with admin account, use:
```bash
username: admin
password: admin
```
To login with user account, use:
```bash
username: user
password: password
```

## Installation 
- Create a virtual environment using `virtualenv` module in python.
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
# on Linux
source venv/bin/activate
# or on Window
.\venv\Scripts\activate

# Install depdendency packages
pip install -r requirements.txt
```
## Configuration

Set up the database: Update the DATABASE_URL in your environment variables or in the alembic.ini file.

Run Alembic migrations:
```bash
alembic upgrade head
```
The  migration will populate the database with random data for each table.
To view all datas, use corresponded GET endpoints

## Running the Application
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
cd app #if you are not in `app` directory
uvicorn main:app --reload
```
This will start the server on http://127.0.0.1:8000

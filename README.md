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

## Import Postman API Collection
### Prerequisites
- Postman installed on your machine. You can download it from Postman's official website.
### Steps to Import a Collection
1. **Open Postman**:
   Launch the Postman application on your computer.
2. **Click on the Import Button**:
   In the top left corner of the Postman interface, click on the `Import` button.
3. **Choose Import Method**:
- **Drop File**
  Drag and drop the API collection `.json` file to the import window.
- **Select File**
  Click on `Select Files`, browse to the location of the collection file, select it, and click `Open`.  
4. **Verify the Import**:
   Once the import is complete, you should see the imported collection in the `Collections` tab on the left sidebar of Postman.
### Additional Resources
- [Postman Documentation](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/)


'''
Initialize our database, application and its configurations.
'''
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_PATH, 'url.db')}")

app = Flask(__name__)
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQL_ALCHEMY_DATABSE_URI'] = DATABASE
app.secret_key = "super secret key"

db_api = SQLAlchemy(app)

from src import routes # Import after setting up db to prevent cyclic import.


'''
Initialize our database, application and its configurations.
'''
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_PATH, 'url.db')}")
# DB_USERS = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_PATH, 'users.db')}")

app_api = Flask(__name__)
app_api.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app_api.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_api.config['SQL_ALCHEMY_DATABSE_URI'] = DATABASE
app_api.secret_key = "super secret key"

app_users = Flask(__name__)
app_users.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app_users.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_users.config['SQL_ALCHEMY_DATABSE_URI'] = DATABASE
app_users.secret_key = "super secret key"

db_api = SQLAlchemy(app_api)
db_users = SQLAlchemy(app_users)

from core import routes # Import after setting up db to prevent cyclic import.


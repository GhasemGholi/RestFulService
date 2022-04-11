from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQL_ALCHEMY_DATABSE_URI'] = 'sqlite:////tmp/urls.db'
app.secret_key = "super secret key"

db = SQLAlchemy(app)

from core import routes


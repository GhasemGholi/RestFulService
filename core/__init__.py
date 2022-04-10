from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQL_ALCHEMY_DATABSE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)

from core import routes


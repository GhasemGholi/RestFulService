from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import routes

app = Flask(__name__)
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQL_ALCHEMY_DATABSE_URI'] = 'sqlite:///urls.db'


db = SQLAlchemy(app)


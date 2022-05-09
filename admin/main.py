import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_PATH, 'url.db')}")

app_api = Flask(__name__)
app_api.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app_api.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app_api.config['SQL_ALCHEMY_DATABSE_URI'] = DATABASE
app_api.secret_key = "super secret key"

db_api = SQLAlchemy(app_api)


from users import * # Import after setting up db to prevent cyclic import.

if __name__ == '__main__':
    # db_api.create_all()
    port = int(os.environ.get('PORT', 5001))
    app_api.run(host='0.0.0.0', port=port, debug=True)
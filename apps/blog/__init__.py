from config import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME, SECRET_KEY, CSRF_ENABLED
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
app.config["SECRET_KEY"] = SECRET_KEY
db = SQLAlchemy(app)
app.config['CSRF_ENABLED'] = CSRF_ENABLED

app.config['TEMPLATES_FOLDER'] = 'templates'

from blog import routes
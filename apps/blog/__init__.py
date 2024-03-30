from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

app.config.from_pyfile('../config.py')
app.config['TEMPLATES_FOLDER'] = 'templates'

from blog import routes
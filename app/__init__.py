from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'    
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'test.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
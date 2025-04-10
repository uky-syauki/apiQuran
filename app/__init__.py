from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
jwt = JWTManager(app)

from app import routes, models
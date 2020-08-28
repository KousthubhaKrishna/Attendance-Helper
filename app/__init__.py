from flask import Flask
from config import Config
from .database.databaseConfig import db,initialize_db
import os

app = Flask(__name__)
print(__name__)
app.config.from_object(Config)
initialize_db(app)

from app import routes



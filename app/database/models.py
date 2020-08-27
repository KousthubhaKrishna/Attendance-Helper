from .databaseConfig import db

class Student(db.Document):
    roll = db.StringField(required=True,unique=True)
    name = db.StringField(required=True)
    section = db.StringField(required=True)
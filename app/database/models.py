from .databaseConfig import db

class Student(db.Document):
    roll = db.IntField(required=True,unique=True)
    name = db.StringField(required=True)
    section = db.StringField(required=True)
    year = db.IntField(required=True)
from .databaseConfig import db

class Student(db.Document):
    roll = db.StringField(required=True,unique=True)
    name = db.StringField(required=True)
    branch = db.StringField(required=True)
    section = db.IntField(required=True)
    year = db.IntField(required=True)

class Elective_students(db.Document):
    eid = db.StringField(required=True, unique=True)
    students_list = db.ListField()

class Elective(db.Document):
    branch = db.StringField(required=True)
    year = db.IntField(required=True) 
    eid = db.StringField(required=True, unique=True)
    ename = db.StringField(required=True)

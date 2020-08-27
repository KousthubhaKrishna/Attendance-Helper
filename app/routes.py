from app import app                                     
from flask import render_template
from .database.models import Student

@app.route("/")
def home():
    students = Student.objects.all()
    print(students[0].name)
    return render_template("index.html")
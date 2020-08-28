from app import app                                     
from flask import render_template,request,request,redirect
from .database.models import Student
import codecs
import pandas as pd
import os
import time

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:

            # Obtain the year and section selected and query for list of students
            section, year = request.form['section'], request.form['year']
            students_info = Student.objects(section=section,year=year)

            #Load the uploaded file, save, read and delete after work 
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                file_url = app.config["UPLOAD_FOLDER"]+str(time.time())+uploaded_file.filename
                uploaded_file.save(file_url)
                att_data = pd.read_csv(codecs.open(file_url, 'rU', 'utf-16'),delimiter='\t')
                os.remove(file_url)
            else:
                return redirect("/", error="Please upload a file")

            # Make a report by comparing data
            report = prepare_report(students_info,att_data)
            return render_template("home.html", report=report)

        # Any errors caused due to invalid data formats
        except:
            print("Invalid Files")
            return render_template("home.html", report=report, error="Invalid file format")
    else:
        return render_template("home.html")


def prepare_report(students_info,att_data):
    present_set = set(att_data["Full Name"])
    present_data,absent_data,unknown_data = [],[],[]

    for index, student in enumerate(students_info):
        if( student.name in present_set ):
            present_data.append({ "sno":index+1, "roll":student.roll,"name":student.name})
            present_set.remove(student.name)
        else:
            absent_data.append({ "sno":index+1, "roll":student.roll,"name":student.name})

    unknown_data = list(present_set)
    return {"present_data":present_data,"absent_data":absent_data,"unknown_data":unknown_data}

    
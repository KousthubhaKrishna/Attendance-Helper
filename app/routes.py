from app import app                                     
from flask import render_template,request,request,redirect,send_file
from .database.models import Student, Elective, Elective_students
import codecs
import pandas as pd
import os
import time
import traceback

@app.route("/", methods=['GET', 'POST'])
def home():

    list_of_subjects = Elective.objects().all()

    if request.method == 'POST':
        try:

            branch, section_list, year = request.form['branch'], request.form.getlist('section') , request.form['year']
            section_list = [int(x) for x in section_list]
            subject = request.form['subject']
            print(section_list)

            students_info = Student.objects(branch=branch,year=year,section__in = section_list).order_by('roll')
            elective_students_list = []
            if(subject != "-1"):
                elective_students_list = Elective_students.objects.get(eid=subject).students_list

            #Load the uploaded file, save, read and delete after work 
            uploaded_file = request.files['file']
            filename = ""
            if uploaded_file.filename != '':
                filename = str(time.time())+uploaded_file.filename
                file_url = app.config["UPLOAD_FOLDER"]+filename
                uploaded_file.save(file_url)
                att_data = pd.read_csv(codecs.open(file_url, 'rU', 'utf-16'),delimiter='\t')
                os.remove(file_url)
            else:
                return render_template("home.html", report=None, error="Please upload a file !",list_of_subjects=list_of_subjects)

            # Make a report by comparing data
            report = None
            if(not elective_students_list):
                report = prepare_report(students_info,att_data)
            else:
                report = prepare_report_for_electives(students_info,elective_students_list,att_data)

            # Save to downloads Folder
            file_download_url = app.config["DOWNLOADS_FOLDER"]+filename
            total_sheet = report["total_sheet"]
            total_sheet.to_csv(file_download_url, index = False, header=True)

            return render_template("home.html", report=report,error="",file_download_url=filename,list_of_subjects=list_of_subjects)

        # Any errors caused due to invalid data formats
        except Exception as error:
            print("Invalid Files",error)
            traceback.print_exc()
            return render_template("home.html", report=None, error="Invalid file format !",list_of_subjects=list_of_subjects)
    else:
        return render_template("home.html",report=None,error="",list_of_subjects=list_of_subjects)


def prepare_report(students_info,att_data):
    present_set = set([x[:] for x in att_data["Full Name"]])
    present_data,absent_data,unknown_data = [],[],[]

    total_time = get_total_present_time(att_data)

    pc,ac = 1,1
    total_sheet = []

    i = 1
    for index, student in enumerate(students_info):
        roll, name = student.roll, student.name[:20]
        display_name = student.name[:]

        for j in present_set:
            if( name == j[:20] ):
                present_data.append({ "sno":pc, "roll":roll,"name":display_name,"time":total_time[j]}) 
                present_set.remove(j)
                pc += 1                                                                                 
                total_sheet.append([i,roll,display_name,1])                                                                                                                                      
                break                                                                                   
                                                                                                        
        else:
            absent_data.append({ "sno":ac, "roll":roll,"name":display_name})
            ac += 1
            total_sheet.append([i,roll,display_name,0])
        i += 1
        
    total_sheet = pd.DataFrame(total_sheet,columns=['Sno','Roll','Name','Status'])
    unknown_data = list(present_set)
    unknown_data = [{"sno":i+1,"name":unknown_data[i],"time":total_time[unknown_data[i]]} for i in range(len(unknown_data))]
    report = {
        "present_data":present_data,
        "absent_data":absent_data,
        "unknown_data":unknown_data,
        "total_sheet":total_sheet,
    }
    return report


def prepare_report_for_electives(students_info,elective_students_list,att_data):
    elective_students_set = set([x[:15] for x in elective_students_list])
    present_set = set([x[:] for x in att_data["Full Name"]])
    present_data,absent_data,unknown_data = [],[],[]

    total_time = get_total_present_time(att_data)
    pc,ac = 1,1
    total_sheet = []

    i = 1
    for index, student in enumerate(students_info):
        roll, name = student.roll[:15], student.name[:20]
        display_name = student.name[:]

        if(roll in elective_students_set):
            for j in present_set:
                if( name == j[:20] ):
                    present_data.append({ "sno":pc, "roll":roll,"name":display_name,"time":total_time[j]}) 
                    present_set.remove(j)
                    pc += 1                                                                                 
                    total_sheet.append([i,roll,display_name,1])                                                                                                                                      
                    break                                                                                   
                                                                                                        
            else:
                absent_data.append({ "sno":ac, "roll":roll,"name":display_name})
                ac += 1
                total_sheet.append([i,roll,display_name,0])
            i += 1
        
    total_sheet = pd.DataFrame(total_sheet,columns=['Sno','Roll','Name','Status'])
    unknown_data = list(present_set)
    unknown_data = [{"sno":i+1,"name":unknown_data[i],"time":total_time[unknown_data[i]]} for i in range(len(unknown_data))]
    report = {
        "present_data":present_data,
        "absent_data":absent_data,
        "unknown_data":unknown_data,
        "total_sheet":total_sheet,
    }
    return report


def get_total_present_time(att_data):
    cur_status = dict()
    total_time = dict()
    check = att_data.values.tolist()
    fmt = '%m/%d/%Y, %H:%M:%S'
    end_time = datetime.strptime(check[0][2][:-3], fmt)
    end_time = end_time + timedelta(hours=1)
    for i in range(len(check)):
        name,status,timestamp = check[i][0],check[i][1],check[i][2]
        status = status[:6]
        if status=="Joined":
            if cur_status.get(name)==None:
                total_time[name]= 0
            cur_status[name]=timestamp[:-3]
        else:
            val = datetime.strptime(timestamp[:-3], fmt) - datetime.strptime(cur_status[name], fmt)
            val = int(round(val.total_seconds()/60))
            total_time[name] += val
            cur_status[name]='0'
    for i in cur_status:
        if cur_status[i]!='0':
            val = end_time - datetime.strptime(cur_status[i], fmt)
            total_time[i] += int(round(val.total_seconds()/60)) 
            cur_status[i] = '0'
    print(total_time)
    return total_time

@app.route('/downloads/<filename>')
def return_files_tut(filename):
    file_download_url = os.path.join(app.config['DOWNLOADS_FOLDER'],filename)
    return send_file(file_download_url, as_attachment=True, attachment_filename='')



#Code to delete cached files regularly
from datetime import datetime, timedelta
from threading import Timer

x=datetime.today()
y = x.replace(day=x.day, hour=3, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x
secs=delta_t.total_seconds()

def deleteChachedFiles():
    for file in os.listdir(app.config["DOWNLOADS_FOLDER"]):
        if(str(file).endswith('.csv')):
            fname = app.config["DOWNLOADS_FOLDER"]+str(file)
            os.remove(fname)
        
deleteChachedFiles()
timer = Timer(secs, deleteChachedFiles)
timer.start()

#threading.Timer(86400.0, deleteChachedFiles).start()
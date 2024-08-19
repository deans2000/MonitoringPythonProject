from Poarta1 import *
from flask import Flask, request, render_template, redirect, url_for, flash
from MySqlConn import *
from werkzeug.utils import secure_filename
from datetime import datetime
from Passwords import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import threading
import csv
import copy
import requests
import smtplib, ssl
import json

app = Flask(__name__)
secret_key = os.urandom(24).hex()
print(secret_key)
app.secret_key = secret_key
mysqlConn = MySqlConn()

def partea1():
    while True:
        if len(os.listdir('intrari')) > 0:
            if os.listdir('intrari')[0] == 'Poarta1.txt':
                angajat = Poarta1()
                angajat.valideazaCard()
                angajat.salveazaDateBackup()
                angajat.stergeFisier()
        
        time.sleep(2)
        def send_email(manager_email, email_content):
            subject = "Employees Who Worked Less Than 8 Hours"
            body = f"Dear manager,\n\nThe following employees worked less than 8 hours today:\n\n{email_content}\nPlease take necessary actions.\n\nBest regards,\nYour Monitoring System"

            sender_email = "xenox0123@gmail.com"
            password = emailPassword

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = manager_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, manager_email, msg.as_string())

            print(f'Email sent to {manager_email}!')

        if "20:00:00" <= datetime.now().strftime("%H:%M:%S") <= "20:00:05":
            query = """
                    SELECT a.Nume, a.Prenume, acc.data, acc.sens, acc.idPoarta, a.IdManager
                    FROM angajati a
                    JOIN access acc ON a.ID = acc.idAngajat
                    WHERE a.IdManager IS NOT NULL
                    ORDER BY a.ID, acc.data LIMIT 100;
                    """
            result=mysqlConn.select(query)

            employee_data = {}

            for record in result:
                name = f"{record[0]} {record[1]}"
                date_str = record[2].split("T")[0]
                timestamp = datetime.strptime(record[2], "%Y-%m-%dT%H:%M:%S.%fZ")
                sens = record[3]
                manager_id = record[5]

                if manager_id not in employee_data:
                    employee_data[manager_id] = {}

                if name not in employee_data[manager_id]:
                    employee_data[manager_id][name] = {}

                if date_str not in employee_data[manager_id][name]:
                    employee_data[manager_id][name][date_str] = []

                employee_data[manager_id][name][date_str].append((timestamp, sens))

            manager_emails = {
                1: "deanslatinat@yahoo.com",
            }
            for manager_id, employees in employee_data.items():
                email_content = ""
                results = []
                for employee, dates in employees.items():
                    for date_str, times in dates.items():
                        total_seconds = 0
                        in_time = None

                        for timestamp, sens in times:
                            if sens == "in":
                                in_time = timestamp
                            elif sens == "out" and in_time:
                                total_seconds += (timestamp - in_time).total_seconds()
                                in_time = None

                        hours_worked = total_seconds / 3600

                        if hours_worked < 8:
                            results.append((employee, date_str, hours_worked))

                if results:
                        csv_filename = f'backup_intrari/{datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")}_idManager_{manager_id}_chiulangii.csv'
                        txt_filename = f'backup_intrari/{datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")}_idManager_{manager_id}_chiulangii.txt'

                        with open(csv_filename, 'w', newline='') as csvfile, open(txt_filename, 'w') as txtfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerow(['Nume', 'Data', 'OreLucrate'])

                            for employee, date_str, hours_worked in results:
                                csvwriter.writerow([employee, date_str, hours_worked])
                                txtfile.write(f"{employee},{date_str},{hours_worked}\n")
                                email_content += f"{employee} on {date_str}: {hours_worked:.2f} hours\n"

                        if email_content and manager_id in manager_emails:
                            send_email(manager_emails[manager_id], email_content)
            query="DELETE FROM access"
            mysqlConn.delete(query)
UPLOAD_FOLDER = 'intrari'
BACKUP_FOLDER = 'backup_intrari'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addEmployee')
def insert():
    return render_template('insert.html')

@app.route('/uploadFile')
def upload():
    return render_template('upload.html')

@app.route('/stats')
def stats():
    return render_template('enter_manager_id.html')

@app.route('/employee', methods=['POST'])
def addPerson():
    inputs = request.form
    if inputs['IdManager'] == '':
        query = f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',null)"
    else:
        query = f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',{inputs['IdManager']})"
    mysqlConn.insert(query)
    return 'Angajat adaugat!'

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        process_file(file_path)
        flash('Data collected successfully')
        return redirect(url_for('home'))
    
def process_file(file_path):
    dictionar = {
        "data": "",
        "sens": "",
        "idPersoana": 0,
        "idPoarta": 2
    }

    with open(file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            idAngajat_str = row[0]
            dataOra_str = row[1]
            sens = row[2]
            dictionarNou = copy.copy(dictionar)
            dictionarNou["data"] = dataOra_str
            dictionarNou["sens"] = sens
            dictionarNou["idPersoana"] = idAngajat_str

            # Send the JSON data to the Flask route
            response = requests.post('http://localhost:5000/poarta2', json=dictionarNou)
            
            if response.status_code != 200:
                print(f"Failed to add entry for {idAngajat_str}. Server responded with: {response.status_code}")

    # Backup the CSV file
    backup_file(file_path)

def backup_file(file_path):
    timeStamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")
    filename = os.path.basename(file_path)
    backup_file_path = os.path.join(BACKUP_FOLDER, f'{filename}_{timeStamp}.csv')

    with open(file_path, 'r') as original_file:
        with open(backup_file_path, 'w') as backup_file:
            backup_file.write(original_file.read())

    print(f"File backed up as {backup_file_path}")

    # Delete the original file after backup
    os.remove(file_path)

@app.route('/poarta2', methods=['POST'])
def poarta2():
    data = request.json
    if not data:
        return "No data provided", 400

    # Construct the SQL query
    query = f"""
    INSERT INTO access 
    VALUES ('{data['data']}', '{data['sens']}', {data['idPersoana']}, {data['idPoarta']}, 'Poarta 2')
    """

    # Execute the query
    mysqlConn.insert(query)
    
    return "Entry added successfully", 200

@app.route('/view_stats', methods=['POST'])
def view_stats():
    # Re-initialize MySqlConn to ensure a fresh connection
    mysqlConn = MySqlConn()

    manager_id = request.form['ManagerID']

    query = f"""
            SELECT a.Nume, a.Prenume, acc.data, acc.sens, acc.idPoarta
            FROM angajati a
            JOIN access acc ON a.ID = acc.idAngajat
            WHERE a.IdManager = {manager_id}
            ORDER BY a.ID, acc.data;
            """
    result = mysqlConn.select(query)

    if not result:
        return render_template('view_stats.html', error="No data available.")

    employee_data = {}

    for record in result:
        name = f"{record[0]} {record[1]}"
        date_str = record[2].split("T")[0]
        timestamp = datetime.strptime(record[2], "%Y-%m-%dT%H:%M:%S.%fZ")
        sens = record[3]

        if name not in employee_data:
            employee_data[name] = {}

        if date_str not in employee_data[name]:
            employee_data[name][date_str] = []

        employee_data[name][date_str].append((timestamp, sens))

    chart_data = {
        'labels': [],
        'datasets': [{
            'label': 'Hours Worked',
            'data': [],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }

    for employee, dates in employee_data.items():
        for date_str, times in dates.items():
            total_seconds = 0
            in_time = None

            for timestamp, sens in times:
                if sens == "in":
                    in_time = timestamp
                elif sens == "out" and in_time:
                    total_seconds += (timestamp - in_time).total_seconds()
                    in_time = None

            hours_worked = total_seconds / 3600
            chart_data['labels'].append(f"{employee} on {date_str}")
            chart_data['datasets'][0]['data'].append(hours_worked)

    # Convert the chart_data dictionary to a JSON string
    chart_data_json = json.dumps(chart_data)

    # Pass the JSON string to the template
    return render_template('view_stats.html', chart_data=chart_data_json)

def partea2():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    t1 = threading.Thread(target=partea1)
    t2 = threading.Thread(target=partea2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

from Poarta1 import *
import os
import time
from flask import Flask, request, render_template, redirect, url_for, flash
from MySqlConn import *
from werkzeug.utils import secure_filename
import threading
import csv
import copy
import requests

app = Flask(__name__)
secret_key = os.urandom(24).hex()
print(secret_key)
app.secret_key = secret_key
mysqlConn = MySqlConn()

def partea1():
    while True:
        if len(os.listdir('Tema/MonitoringPythonProject/intrari')) > 0:
            if os.listdir('Tema/MonitoringPythonProject/intrari')[0] == 'Poarta1.txt':
                angajat = Poarta1()
                angajat.valideazaCard()
                angajat.salveazaDateBackup()
                angajat.stergeFisier()
        
        time.sleep(2)

UPLOAD_FOLDER = 'Tema/MonitoringPythonProject/intrari'
BACKUP_FOLDER = 'Tema/MonitoringPythonProject/backup_intrari'
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
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")
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

def partea2():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    t1 = threading.Thread(target=partea1)
    t2 = threading.Thread(target=partea2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

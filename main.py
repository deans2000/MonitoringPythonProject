from Poarta1 import *
import os
import time
from flask import Flask, request, render_template
from MySqlConn import *
import threading

app = Flask(__name__)
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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addEmployee')
def insert():
    return render_template('insert.html')

@app.route('/employee', methods=['POST'])
def addPerson():
    inputs = request.form
    if inputs['IdManager'] == '':
        query = f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',null)"
    else:
        query = f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',{inputs['IdManager']})"
    mysqlConn.insert(query)
    return 'Angajat adaugat!'

def partea2():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    t1 = threading.Thread(target=partea1)
    t2 = threading.Thread(target=partea2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

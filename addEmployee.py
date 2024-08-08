from flask import Flask,request,render_template
from MySqlConn import *
app=Flask(__name__)
mysqlConn=MySqlConn()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addEmployee')
def insert():
    return render_template('insert.html')

@app.route('/employee',methods=['POST'])
def addPerson():
    inputs=request.form
    if inputs['IdManager']=='':
        query=f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',null)"
    else:
        query=f"INSERT INTO angajati VALUES (null,'{inputs['Nume']}','{inputs['Prenume']}','{inputs['Companie']}',{inputs['IdManager']})"
    mysqlConn.insert(query)
    return 'Angajat adaugat!'

if __name__=='__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)


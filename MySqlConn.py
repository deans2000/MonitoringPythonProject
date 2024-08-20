import mysql.connector
from Passwords import *
class MySqlConn():
    def __init__(self):
        self.mydb=mysql.connector.connect(host='localhost',
                                          user='root',
                                          password=mySQLServerPassword,
                                          database='monitoringpythonproject')
        self.cursor=self.mydb.cursor()

    def select(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self,query):
        self.cursor.execute(query)
        self.mydb.commit()

    def delete(self,query):
        self.cursor.execute(query)
        self.mydb.commit()



        
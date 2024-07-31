import mysql.connector
class MySqlConn():
    def __init__(self):
        self.mydb=mysql.connector.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          database='monitoringpythonproject')
        self.cursor=self.mydb.cursor()

    def insert(self,query):
        self.cursor.execute(query)
        self.mydb.commit()



        
import datetime
from Poarta import *
from MySqlConn import *
import os
class Poarta1(Poarta):
    def salvareDate(self):
        dataOra=datetime.datetime.now()
        folder='Tema/MonitoringPythonProject/intrari'
        dimensiuneInitiala=len(os.listdir(folder))

        with open('Tema/MonitoringPythonProject/intrari/Poarta1.txt','w') as file:
            idAngajat_str = str(self.idAngajat)
            dataOra_str = dataOra.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            dataOra_str2=dataOra.strftime("%Y-%m-%dT%H-%M-%S-%fZ")
            file.write(idAngajat_str+","+self.sens+","+dataOra_str+";\n")

        dimensiuneDupa=len(os.listdir(folder))

        if dimensiuneDupa>dimensiuneInitiala:
            mysqlConn=MySqlConn()
            query=f"INSERT INTO access VALUES ('{dataOra}','{self.sens}',{self.idAngajat},1,null)"
            mysqlConn.insert(query)

        with open('Tema/MonitoringPythonProject/intrari/Poarta1.txt','r') as file2:
            content=file2.read()
            with open(f'Tema/MonitoringPythonProject/backup_intrari/Poarta1_backup_{dataOra_str2}.txt','w') as file3:
                file3.write(content)
        




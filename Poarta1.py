import datetime
from Poarta import *
from MySqlConn import *
import os

class Poarta1(Poarta):
    entries = []

    def salvareDate(self):
        dataOra = datetime.datetime.now()
        idAngajat_str = str(self.idAngajat)
        dataOra_str = dataOra.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        entry = f"{idAngajat_str},{dataOra_str},{self.sens}"
        Poarta1.entries.append(entry)

    @classmethod
    def save_all_entries(cls):
        folder = 'Tema/MonitoringPythonProject/intrari'
        dimensiuneInitiala=len(os.listdir(folder))
        backup_folder = 'Tema/MonitoringPythonProject/backup_intrari'

        file_path = os.path.join(folder, 'Poarta1.txt')
        backup_file_path = os.path.join(backup_folder, 'Poarta1_backup.txt')

        # Write all entries to the main file
        with open(file_path, 'w') as file:
            for entry in cls.entries:
                file.write(entry + ";\n")

        dimensiuneDupa=len(os.listdir(folder))

        if dimensiuneDupa>dimensiuneInitiala:
            mysqlConn = MySqlConn()
            for entry in cls.entries:
                idAngajat_str, dataOra_str, sens = entry.split(',')
                query = f"INSERT INTO access VALUES ('{dataOra_str}','{sens}',{idAngajat_str},1,null)"
                mysqlConn.insert(query)

        # Write all entries to the backup file
        with open(backup_file_path, 'w') as backup_file:
            for entry in cls.entries:
                backup_file.write(entry + ";\n")

       
        

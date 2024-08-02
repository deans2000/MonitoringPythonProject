import datetime
from Poarta import *
from MySqlConn import *
import os

class Poarta1(Poarta):
    entries = []

    def valideazaCard(self):
        idAngajat_str = str(self.idAngajat)
        dataOra_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        entry = f"{idAngajat_str},{dataOra_str},{self.sens}"
        Poarta1.entries.append(entry)

        mysqlConn = MySqlConn()
        query = f"INSERT INTO access VALUES ('{dataOra_str}','{self.sens}',{idAngajat_str},1,'Poarta 1')"
        mysqlConn.insert(query)

        # Save data to the main file
        self.salveazaDate()

        # If 5 entries are reached, save to backup and delete the main file
        if len(self.entries) >= 5:
            self.salveazaDateBackup()
            self.stergeFisier()
            # Clear entries after backup
            Poarta1.entries.clear()

    def salveazaDate(self):
        # Write all entries to the main file
        folder = 'Tema/MonitoringPythonProject/intrari'
        file_path = os.path.join(folder, 'Poarta1.txt')
        with open(file_path, 'w') as file:
            for entry in self.entries:
                file.write(entry + ";\n")

    def salveazaDateBackup(self):
        # Write all entries to the backup file
        timeStamp=datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")
        backup_folder = 'Tema/MonitoringPythonProject/backup_intrari'
        backup_file_path = os.path.join(backup_folder, f'Poarta1_backup_{timeStamp}.txt')
        with open(backup_file_path, 'w') as backup_file:
            for entry in self.entries:
                backup_file.write(entry + ";\n")

    def stergeFisier(self):
        folder = 'Tema/MonitoringPythonProject/intrari'
        file_path = os.path.join(folder, 'Poarta1.txt')
        os.remove(file_path)

       
        

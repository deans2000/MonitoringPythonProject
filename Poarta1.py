import datetime
from Poarta import *
from MySqlConn import *
import os

class Poarta1(Poarta):

    def valideazaCard(self):
        filePath='intrari/Poarta1.txt'
        mysqlConn = MySqlConn()
        with open(filePath,'r') as file:
            for line in file:
                line = line.strip().strip(';')
                if line:
                    idAngajat_str, dataOra_str, sens = line.split(',')
                    query = f"INSERT INTO access VALUES ('{dataOra_str}','{sens}',{idAngajat_str},1,'Poarta 1')"
                    mysqlConn.insert(query)
        print('Card validat!')

    def salveazaDateBackup(self):
        # Writing all entries to the backup file
        filePath='intrari/Poarta1.txt'
        timeStamp=datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")
        backup_folder = 'backup_intrari'
        backup_file_path = os.path.join(backup_folder, f'Poarta1_backup_{timeStamp}.txt')
        with open(filePath, 'r') as original_file:
            with open(backup_file_path, 'w') as backup_file:
                backup_file.write(original_file.read())
        print('Date salvate in backup!')

    def stergeFisier(self):
        folder = 'intrari'
        file_path = os.path.join(folder, 'Poarta1.txt')
        os.remove(file_path)
        print('Fisier sters!')

       
        

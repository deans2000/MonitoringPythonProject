from Poarta1 import *
import os
import time

while True:
    if len(os.listdir('Tema/MonitoringPythonProject/intrari'))>0:
        if os.listdir('Tema/MonitoringPythonProject/intrari')[0]=='Poarta1.txt':
            angajat=Poarta1()
            angajat.valideazaCard()
            angajat.salveazaDateBackup()
            angajat.stergeFisier()
    
    time.sleep(2)

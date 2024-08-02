from Poarta1 import *
i=0
while i<5:
    id=int(input('Introduceti id-ul: '))
    sens=input('Introcueti sensul: ')
    nrPoarta=int(input('Introduceti numarul portii: '))

    if nrPoarta==1:
        angajat=Poarta1(id,sens)
        angajat.valideazaCard()
        print('Cardul a fost validat!')
    else:
        print('Poarta introdusa nu exista!')

    i+=1
    


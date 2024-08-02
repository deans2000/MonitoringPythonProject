from abc import ABC,abstractmethod

class Poarta(ABC):
    def __init__(self,idAngajat,sens):
        self.idAngajat=idAngajat
        self.sens=sens

    @abstractmethod
    def valideazaCard(self):
        pass
    
from MDUS.Class.DataClass import Data

class IonNTPClass(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'Ion_NTP'
    def Info(self):
        super().Info()
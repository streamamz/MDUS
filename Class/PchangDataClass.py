from MDUS.Class.DataClass import Data

class PchangData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'PCHANG'
    def Info(self):
        super().Info()
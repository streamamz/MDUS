from MDUS.Class.DataClass import Data

class Datas(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'Integrated Data'
    def Info(self):
        super().Info()
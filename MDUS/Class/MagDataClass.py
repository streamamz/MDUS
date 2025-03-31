from MDUS.Class.DataClass import Data

class MagData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = "MAG"
    def Info(self):
        super().Info()
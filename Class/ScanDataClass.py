from MDUS.Class.DataClass import Data
from MDUS.Setting.setting import setting

class ScanData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'SCAN'
    def Info(self):
        super().Info()
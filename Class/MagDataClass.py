from MDUS.Class.DataClass import Data
from MDUS.Input.InputMag import *

# ==== class for Mag data ====
class MagData(Data):
    # ===== constructor ====
    # add type field
    def __init__(self):
        super().__init__()
        self.type = 'MAG'
    def Info(self):
        print('Data Type\t:',self.type)
        super().Info()
    # == input ==
    def Input(self,start,end,sec=1):
        ofile, pfile, result = maginput(start,end,sec)
        # = value =
        self.value = result
        # = update Information =
        self.info['Start Date'] = start
        self.info['End Date'] = end
        self.info['Time Resolution'] = sec
        self.info['Input Files'] = ', '.join(pfile)
        self.info['Original Files'] = ', '.join(ofile)
    # == plot ==
    def Plot(self):
        pass
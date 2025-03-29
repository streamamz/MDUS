from MDUS.Class.DataClass import Data
from MDUS.Class.MagDataClass import MagData
from MDUS.Class.ScanDataClass import ScanData

class Datas(Data):
    def __init__(self,datatype=['MAG']):
        super().__init__()
        self.info["Data Type"] = 'Integrated Data'
        self.data = {}
        supdata = ["MAG","FIPS_CDR_SCAN"]
        dtmp = []
        for d in datatype:
            if d in supdata:
                if d == "MAG":
                    self.data[d] = MagData()
                    self.data[d].Setting()
                elif d == "FIPS_CDR_SCAN":
                    self.data[d] = ScanData()
                    self.data[d].Setting()
                dtmp.append(d)
            else:
                print("Warning : non supportd data type : ",d)
        self.info["Input Data"] = dtmp
    def Info(self):
        super().Info()
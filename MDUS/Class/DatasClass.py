from MDUS.Class.DataClass import Data
from MDUS.Class.MagDataClass import MagData
from MDUS.Class.ScanDataClass import ScanData

class Datas(Data):
    def __init__(self,datatype=['MAG']):
        super().__init__()
        self.info["Data Type"] = 'Integrated Data'
        self.value = {}
        supdata = ["MAG","FIPS_CDR_SCAN"]
        dtmp = []
        for d in datatype:
            if d in supdata:
                if d == "MAG":
                    self.value[d] = MagData()
                    self.value[d].LoadSetting()
                elif d == "FIPS_CDR_SCAN":
                    self.value[d] = ScanData()
                    self.value[d].LoadSetting()
                dtmp.append(d)
            else:
                print("Warning : non supportd data type : ",d)
        self.info["Input Data"] = dtmp
    def Info(self):
        super().Info()
from MDUS.Input.InputMag import maginput
# from MDUS.Input.InputScan import scaninput
# from MDUS.Input.InputPchang import pchanginput

from MDUS.Class.DatasClass import Datas
from MDUS.Class.MagDataClass import MagData
# from MDUS.Class.ScanDataClass import ScanData
# from MDUS.Class.PchangDataClass import PchangData

# from MDUS.Analysis.Analysis.DataShaping import DataIntegration

# def loadsetting(self)

# def datasinput(self,start=None,end=None,orbit=None,inputdata=["mag"],
#                sec=1, Rm=True, # mag関連
#                scantype = "proton", integrate=True, # scan関連
#                pchangtype='H_PA'): # pchang関連
#     # 例外処理
#     if start is None and end is None and orbit is None:
#         raise ValueError("Error: start, end, and orbit cannot be None at the same time")
#     # magの例外処理
#     if sec not in [1,5,10,60]:
#         raise ValueError("Error: sec must be 1, 5, 10, or 60")
#     # pchangの例外処理
#     pchangdatatypes = ['H_PA', 'HE2_PA', 'HE_PA', 'NAGROUP_PA', 'OGROUP_PA']
#     if pchangtype not in pchangdatatypes:
#         raise ValueError("Error: datatype must be 'H_PA', 'HE2_PA', 'HE_PA', 'NAGROUP_PA', or 'OGROUP_PA'")
#     # scanの例外処理

#     for data in inputdata:
#         if data == "mag":
#             data_mag = MagData()
#             data_mag.Input(start,end,orbit,sec,Rm)
#             self.mag = data_mag
#         elif data == "scan":
#             data_scan = ScanData()
#             data_scan.Input(start,end,orbit,scantype)
#             self.scan = data_scan
#             # if integrate:
#             #     self.scan.Integrate()
#         elif data == "pchang":
#             data_pchang = PchangData()
#             data_pchang.Input(start,end,orbit,pchangtype)
#             self.pchang = data_pchang
#         else:
#             raise ValueError("Error: inputdata must be 'mag', 'scan', or 'pchang'")
#     self.info["Input Data"] = inputdata

# Datas.Input = datasinput
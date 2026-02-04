__version__ = "0.2.2"

# Spice setup
from MDUS.Spice.SpiceSetup import *
# check spk files
chech_spkfile()

# datapath setting
from MDUS.Setting.setting import reload_setting as ReloadDatapath

# import data
from MDUS.Data.data import *

# import constant
from MDUS.Constant.constant import *

# import Classes
from MDUS.Class.MagDataClass import MagData
from MDUS.Class.ScanDataClass import ScanData
from MDUS.Class.EspecDataClass import EspecData
from MDUS.Class.DatasClass import Datas

# import LoadData
from MDUS.LoadData import LoadMag
from MDUS.LoadData import LoadScan
from MDUS.LoadData import LoadDatas

# import Plot
import sys
if "ipykernel" in sys.modules:
    print("Jupyter")
    import matplotlib_inline.backend_inline
    matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
import MDUS.Plot.PlotMag
import MDUS.Plot.PlotOrbit
import MDUS.Plot.PlotScan
# import MDUS.Plot.PlotPchang
import MDUS.Plot.PlotDatas

# Analysis関連
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model
# from MDUS.Analysis import CalcPhysics

# import Convert
# from MDUS.Convert import ConvertMag
# classディレクトリに入っているDataClass.pyをimportする
from MDUS.Class.DataClass import Data
from MDUS.Class.MagDataClass import MagData
from MDUS.Class.ScanDataClass import ScanData
# data関連はここに追記していく
from MDUS.Data.data import orbit, dip
# 定数はここに追記していく
from MDUS.Data.constant import *
# input
import MDUS.Input.InputScan
# plot
import MDUS.Plot.PlotMag
import MDUS.Plot.PlotOrbit
import MDUS.Plot.PlotScan
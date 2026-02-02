from MDUS.Class.DataClass import Data

from MDUS.LoadData import LoadEspec
from MDUS.Plot import PlotEspec
from MDUS.Plot import PlotOrbit
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model

class EspecData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'FIPS_DDR_ESPEC'
    def Info(self):
        super().Info()    
    # LoadData
    def LoadSetting(self,target=["H+"]) -> None:
        LoadEspec.especsetting(self,target)
    def Load(self,start=None,end=None,orbit=None) -> None:
        LoadEspec.especload(self,start,end,orbit)
    # Plot
    def Plot(self, target="all", start=None, end=None, fig = None, ax = None, fsize=None,vmin=1e5,vmax=1e9, printxticks=True, printother=True):
        fig, ax = PlotEspec.Plot(self, target, start, end, fig, ax, fsize, vmin, vmax, printxticks, printother)
        return fig, ax
    # Analysis
    def GetPos(self,unit='Rm') -> None:
        DataShaping.GetPos(self,unit)
    # def CTransform(self,coordinate='MSM',mag=True,replace=False) -> None:
    #     DataShaping.CTransform(self,coordinate,mag,replace)
from MDUS.Class.DataClass import Data

from MDUS.LoadData import LoadScan
from MDUS.Plot import PlotScan
from MDUS.Plot import PlotOrbit
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model
# from MDUS.Analysis import CalcPhysics

class ScanData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'FIPS_CDR_SCAN'
    def Info(self):
        super().Info()
    # LoadData
    def LoadSetting(self,target='Proton',quality=0) -> None:
        LoadScan.scansetting(self,target,quality)
    def Load(self,start=None,end=None,orbit=None) -> None:
        LoadScan.scanload(self,start,end,orbit)
    # Plot
    def PlotOld(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),vmin=1e5,vmax=1e9,pxlabel=True,ptitle=True):
        fig, ax = PlotScan.Plot(self,start,end,fig,ax,fsize,vmin,vmax,pxlabel=pxlabel,ptitle=ptitle)
        return fig, ax
    def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),vmin=1e5,vmax=1e9,coordinate='MSO',skip_labels=False):
        fig, ax = PlotScan.PlotAdvanced(self,start,end,fig,ax,fsize,vmin,vmax,coordinate,skip_labels)
        return fig, ax
    def PlotNew(self, start=None, end=None, fig = None, ax = None, fsize=(9,3.5),vmin=1e5,vmax=1e9, printxticks=True, printother=True):
        fig, ax = PlotScan.PlotNew(self, start, end, fig, ax, fsize, vmin, vmax, printxticks, printother)
        return fig, ax
    def PlotOrbit(self,fig=None,ax=None,plane='XY',coordinate='MSO'):
        fig, ax = PlotOrbit.PlotOrbit(self,fig,ax,plane,coordinate)
        return fig, ax
    # DataShaping
    def GetPos(self,unit='Rm') -> None:
        DataShaping.GetPos(self,unit)
    def CTransform(self,coordinate='MSM',mag=True,replace=False) -> None:
        DataShaping.CTransform(self,coordinate,mag,replace)
    # def CalcNTP(self):
    #     CalcPhysics.CalcNTP(self)
    # Model
    def CalcModel(self, model="KT17",
                   Rsun=0.4, DI=50):
        Model.CalcModel(self, model, Rsun, DI)
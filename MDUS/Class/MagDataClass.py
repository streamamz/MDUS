from MDUS.Class.DataClass import Data

from MDUS.LoadData import LoadMag
from MDUS.Plot import PlotMag
from MDUS.Plot import PlotOrbit
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model

class MagData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = "MAG"
    def Info(self):
        super().Info()
    def Value(self,start=None,end=None,dropna=False,inplace=False):
        return super().Value(start,end,dropna,inplace)
    # LoadData
    def LoadSetting(self,sec=1,unit="Rm") -> None:
        LoadMag.magsetting(self,sec,unit)
    def Load(self,start=None,end=None,orbit=None) -> None:
        LoadMag.magload(self,start,end,orbit)
    # Plot
    def PlotSetting(self,component={'Bx':'red','By':'blue','Bz':'green','Btot':'black'},
                    ylabel='Magnetic Field [nT]',
                    coordinate='MSO',
                    title = None) -> None:
        PlotMag.PlotSetting(self,component,ylabel,coordinate,title)
    def PlotOld(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),pxlabel=True,ptitle=True):
        fig, ax = PlotMag.Plot(self,start,end,fig,ax,fsize,pxlabel=pxlabel,ptitle=ptitle)
        return fig, ax
    def Plot(self, start=None,end=None,fig=None,ax=None,fsize=(9,3.5),coordinate='MSO',skip_labels=False):
        fig, ax = PlotMag.PlotAdvanced(self,start,end,fig,ax,fsize,coordinate,skip_labels)
        return fig, ax
    def PlotNew(self, start=None, end=None, fig = None, ax = None, fsize=(9,3.5), printxticks=True, printother=True):
        fig, ax = PlotMag.PlotNew(self, start, end, fig, ax, fsize, printxticks, printother)
        return fig, ax
    def PlotOrbit(self,fig=None,ax=None,
                  plane='XY',coordinate='MSO'):
        fig, ax = PlotOrbit.PlotOrbit(self,fig,ax,plane,coordinate)
        return fig, ax
    # DataShaping
    def GetPos(self,unit='Rm') -> None:
        DataShaping.GetPos(self,unit)
    def CTransform(self,coordinate='MSM',mag=True,replace=False) -> None:
        DataShaping.CTransform(self,coordinate,mag,replace)
    def MoveAverage(self,window=3,replace=False,component=['Bx', 'By', 'Bz', 'DBx', 'DBy', 'DBz', 'Btot']) -> None:
        DataShaping.MoveAverage(self,window,replace,component)
    # Model
    def CalcModel(self, model="KT17",
                   Rsun=0.4, DI=50):
        Model.CalcModel(self, model, Rsun, DI)

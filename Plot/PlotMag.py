import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd

from MDUS.Class import MagDataClass
from MDUS.Class import ScanDataClass

def Plot(self,component={'Bx':'red','By':'blue','Bz':'green','|B|':'black'},legend=None,ds=None,de=None,filename=None,fsize=(9,3),fig=None,ax=None):
    if not all([i in self.value.columns for i in component.keys()]):
        raise ValueError("Error: did not find the component in the data")
    if ds is not None and de is not None:
        ds = pd.to_datetime(ds)
        de = pd.to_datetime(de)
    else:
        ds = self.value.index[0]
        de = self.value.index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)
    
    if legend is None or len(legend) != len(component):
        legend = component.keys()
    for comp,color,leg in zip(component.keys(),component.values(),legend):
        ax.plot(self.value.query('@ds <= index <= @de').index,self.value.query('@ds <= index <= @de')[comp],color=color,label=leg,linewidth=1)
    # ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("UTC")
    ax.set_ylabel("Magnetic Field [nT]")
    ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
    ax.set_zorder(2)
    ax.patch.set_visible(False)
    if filename is not None:
        fig.tight_layout()
        fig.savefig(filename)
    return fig, ax
MagDataClass.MagData.Plot = Plot
ScanDataClass.ScanData.PlotMag = Plot
import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
import pandas as pd

from MDUS.Constant.constant import EQTAB
from MDUS.Class import ScanDataClass

def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),vmin=1e5,vmax=1e9):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize
                              ,constrained_layout=True # 消すかも 
                               ) 
    if len(self.value.values) == 0:
        print("Warning: No plot data")
        return fig, ax
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)
    else:
        ds = self.value.dropna().index[0]
        de = self.value.dropna().index[-1]   

    # dataの準備
    pdata = self.value[EQTAB].replace(0,1e-38).query('@ds <= index <= @de').values
    date = self.value.query('@ds <= index <= @de').index.values

    # plot
    if not pdata.size == 0:
        cmap = plt.cm.jet
        cmap.set_under('white')
        hm = ax.pcolormesh(date,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
        hm.set_clim(vmin,vmax)
        ax.set_xlabel("UTC")
        ax.set_ylabel("Energy [keV/q]")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
        ax.set_yscale('log')
        ax.set_ylim(0.2,20)
        ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
        cbar = plt.colorbar(hm)
        cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
    else:
        print("Warning: No plot data")
    return fig, ax
ScanDataClass.ScanData.Plot = Plot
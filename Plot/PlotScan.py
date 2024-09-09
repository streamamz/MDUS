import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
from matplotlib.colors import LogNorm
import pandas as pd

from MDUS.Data.constant import EQTAB
from MDUS.Class import ScanDataClass

def Plot(self,ds=None,de=None,filename=None,fsize=(9,3),fig=None,ax=None,vmin=1e5,vmax=1e9):
    if ds is not None and de is not None:
        ds = pd.to_datetime(ds)
        de = pd.to_datetime(de)
    else:
        ds = self.value.index[0]
        de = self.value.index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)
    
    pdata = self.value[EQTAB].query('@ds <= index <= @de').values.astype(float)
    energy = self.value[EQTAB].columns.to_numpy().astype(float)
    date = self.value.query('@ds <= index <= @de').index.to_numpy()

    if not pdata.size == 0:
        hm = ax.pcolormesh(date,energy,pdata.T,norm=LogNorm(),cmap='jet')
        hm.set_clim(vmin,vmax)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.set_xlabel("UTC")
        ax.set_ylabel("Energy [keV/q]")
        ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
        ax.set_zorder(1)
        ax.patch.set_visible(False)
        _, y_max = ax.get_ylim()
        ax.set_ylim(0.2,y_max)
        cbar = plt.colorbar(hm,pad=0.08)
    if filename is not None:
        fig.tight_layout()
        fig.savefig(filename)
    return fig, ax
ScanDataClass.ScanData.Plot = Plot
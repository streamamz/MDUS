import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
from matplotlib.colors import LogNorm
import pandas as pd
import numpy as np

from MDUS.Class import PchangDataClass

def Plot(self,ds=None,de=None,filename=None,fsize=(9,3),fig=None,ax=None,vmin=1e7,vmax=1e11,title=None):
    if ds is not None and de is not None:
        ds = pd.to_datetime(ds)
        de = pd.to_datetime(de)
    else:
        ds = self.value.index[0]
        de = self.value.index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)

    pdata = self.value.query('@ds <= index <= @de').values.astype(float)
    angles = self.value.columns.to_numpy().astype(float)
    date = self.value.query('@ds <= index <= @de').index.to_numpy()

    cmap = plt.cm.jet  # カラーマップをjetに設定
    cmap.set_bad(color='gray')  # NaN（欠損値）の色をグレーに設定
    cmap.set_under(color='white')

    if not pdata.size == 0:
        ax.set_ylim(0,180)
        ax.set_yticks([0,90,180])
        hm = ax.pcolormesh(date,angles,np.ma.masked_less_equal(pdata.T,0),norm=LogNorm(),cmap=cmap)
        hm.set_clim(vmin,vmax)
        cbar = plt.colorbar(hm,pad=0.08)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.set_xlabel("UTC")
        ax.set_ylabel("Pitch Angle [deg]")
        if title is None:
            ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
        else:
            ax.set_title(title)
    if filename is not None:
        fig.tight_layout()
        fig.savefig(filename)
    return fig, ax        
PchangDataClass.PchangData.Plot = Plot

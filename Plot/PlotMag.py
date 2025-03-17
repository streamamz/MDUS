import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd
import matplotlib.ticker as ticker

from MDUS.Class import MagDataClass

def Plot(self,ds=None,de=None,fig=None,ax=None,fsize=(9,3)):
    if ds is not None and de is not None:
        ds = pd.to_datetime(ds)
        de = pd.to_datetime(de)
    else:
        ds = self.value.dropna().index[0]
        de = self.value.dropna().index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)
    # Plot
    colors = ['black','red','blue','green']
    comp = ['|B|','Bx','By','Bz']
    for i,j in zip(colors,comp):
        ax.plot(
            self.value.query('@ds <= index <= @de').index.values,
            self.value.query('@ds <= index <= @de')[j].values,
            color=i,label=j,linewidth=1
        )
    ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel('UTC')
    ax.set_ylabel('Magnetic Field [nT]')
    ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    ax.set_zorder(2)
    return fig, ax 

MagDataClass.MagData.Plot = Plot
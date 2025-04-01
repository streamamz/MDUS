import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd
import matplotlib.ticker as ticker

from MDUS.Class import MagDataClass

def PlotSetting(self,component={'Bx':'red','By':'blue','Bz':'green','|B|':'black'},
                ylabel='Magnetic Field [nT]',
                title = None):
    self.plotinfo = {}
    self.plotinfo['component'] = component
    self.plotinfo['ylabel'] = ylabel
    if title is not None:
        self.plotinfo['title'] = title
MagDataClass.MagData.PlotSetting = PlotSetting

def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3)):
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)
    else:
        ds = self.value.dropna().index[0]
        de = self.value.dropna().index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)

    # default setting
    colors = ['black','red','blue','green']
    comp = ['|B|','Bx','By','Bz']
    ylabel = 'Magnetic Field [nT]'
    title = ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S")

    # load setting
    if hasattr(self,'plotinfo'):
        if 'component' in self.plotinfo.keys():
            colors = self.plotinfo['component'].values()
            comp = self.plotinfo['component'].keys()
        if 'ylabel' in self.plotinfo.keys():
            ylabel = self.plotinfo['ylabel']
        if 'title' in self.plotinfo.keys():
            title = self.plotinfo['title']

    for i,j in zip(colors,comp):
        ax.plot(
            self.value.query('@ds <= index <= @de').index.values,
            self.value.query('@ds <= index <= @de')[j].values,
            color=i,label=j,linewidth=1
        )
    ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel('UTC')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    ax.set_zorder(2)
    return fig, ax 

MagDataClass.MagData.Plot = Plot
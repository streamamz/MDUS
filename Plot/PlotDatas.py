import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd

from MDUS.Class import DatasClass

def Plot(self, legend=None,ds=None,de=None,filename=None, 
         magcomp={'Bx':'red','By':'blue','Bz':'green','|B|':'black'}, 
         ):
    # fig, ax があるか否か
    if (not hasattr(self, "fig")) or (not hasattr(self, "axes")):
        fig, ax = plt.subplots(len(self.info["Input Data"]),1,figsize=(9,len(self.info["Input Data"])*3))
        self.fig = fig
        self.axes = {}
        for i in range(len(self.info["Input Data"])):
            self.axes[self.info["Input Data"][i]] = ax[i]
    plotdatas = self.info["Input Data"]
    for plotdata in plotdatas:
        if plotdata == "mag":
            self.fig, self.axes[plotdata] = self.mag.Plot(
                component=magcomp, legend=legend, ds=ds, de=de, fig=self.fig, ax=self.axes[plotdata], title="Magnetic Field"
            )
        elif plotdata == "scan":
            self.fig, self.axes[plotdata] = self.scan.Plot(
                ds = ds, de = de, fig=self.fig, ax=self.axes[plotdata], title="Scan"
            )
        elif plotdata == "pchang":
            self.fig, self.axes[plotdata] = self.pchang.Plot(
                ds = ds, de = de, fig=self.fig, ax=self.axes[plotdata], title="Pchang"
            )
    if ds is not None and de is not None:
        plt.suptitle(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
    else:
        ds = self.mag.value.index[0]
        de = self.mag.value.index[-1]
        plt.suptitle(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
    self.fig.tight_layout()
    if filename is not None:
        self.fig.savefig(filename,dpi=300)
DatasClass.Datas.Plot = Plot
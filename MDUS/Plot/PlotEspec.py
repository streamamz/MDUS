import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

from MDUS.Spice.SpiceSetup import spice_exist
from MDUS.Constant.constant import *
import spiceypy as sp

def Plot(self, target = "all", start=None, end=None, fig = None, ax = None, fsize=None,vmin=1e5,vmax=1e9, printxticks=True, printother=True):
    # initial setting
    keys = list(self.value.keys())
    plotkeys = []
    if target == "all":
        plotkeys = keys
    else:
        plotkeys = [target]
    if fsize is None:
        nplots = len(plotkeys)
        fsize = (9,3*nplots)
    if fig is None or ax is None:
        if target == "all":
            nplots = len(keys)
            fig, ax = plt.subplots(nplots,1,figsize=fsize
                                ,constrained_layout=True, # 消すかも 
                                sharex=True
                                )
        else:
            fig, ax = plt.subplots(figsize=fsize
                                ,constrained_layout=True # 消すかも 
                                ) 
            ax = np.array([ax])
    else:
        if not isinstance(ax, np.ndarray):
            ax = np.array([ax])
    if len(self.value[keys[0]].values) == 0:
        print("Warning: No plot data")
        return fig, ax
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)
    else:
        ds = self.value[plotkeys[0]].dropna().index[0]
        de = self.value[plotkeys[0]].dropna().index[-1]       
    # plot
    cmap = plt.cm.jet
    cmap.set_under('white')
    cmap.set_bad('grey')    
    
    for i in range(len(plotkeys)):
        data_copy = self.value[plotkeys[i]].copy()
        data_copy[EQTAB] = data_copy[EQTAB].replace(0,1e-38)
        pdata = data_copy[EQTAB].query('@ds <= index <= @de').values
        date = data_copy.query('@ds <= index <= @de').index.values
        if not pdata.size == 0:
            hm = ax[i].pcolormesh(date,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
            hm.set_clim(vmin,vmax)
            ax[i].set_ylabel(plotkeys[i]+" [keV/q]")    
            ax[i].set_yscale('log')
            ax[i].set_ylim(0.2,20)
            cbar = plt.colorbar(hm, ax=ax[i])
            cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
        else:
            print("Warning: No plot data")
            return fig, ax
    
    # ticks
    ax[-1].xaxis.set_major_locator(ticker.LinearLocator(5))
    ax[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d %H:%M:%S"))
    xlabels = [tick.get_text() for tick in ax[-1].get_xticklabels()]
    xticks_location = ax[-1].get_xticks()
    new_labels = []
    xlabel_name = "UTC"
    # other settings
    if printother:
        if "Orbit" in self.info.keys():
            orbit_num = "Orbit: " + str(self.info["Orbit"])
            ax[0].text(0, 1.0, orbit_num, ha='left', va='bottom', transform=ax[0].transAxes)
        dt = pd.to_datetime(self.value[plotkeys[0]].query("@ds <= index <= @de").index.values[0]).strftime('%Y-%m-%d')
        ax[0].text(1.0, 1.0, dt, ha='right', va='bottom', transform=ax[0].transAxes)
    if printxticks:
        if spice_exist:
            time = sp.str2et(np.array(xlabels))
            ptarg = sp.spkpos('MESSENGER',time,'J2000','NONE','MERCURY BARYCENTER')[0]
            positions = np.array([sp.mxv(sp.pxform("J2000", "MSGR_MSO", t), pos) for t, pos in zip(time, ptarg)])
            xmso = positions[:,0] / Rm
            ymso = positions[:,1] / Rm
            zmso = positions[:,2] / Rm
            for xlabel, x, y, z in zip(xlabels, xmso, ymso, zmso):
                tmp = pd.to_datetime(xlabel).strftime('%H:%M:%S')
                new_label = f"{tmp}\n{x:.2f}\n{y:.2f}\n{z:.2f}"
                new_labels.append(new_label)
            xlabel_name += "/X_MSO/Y_MSO/Z_MSO"
        else:
            new_labels = xlabels
        ax[-1].set_xticks(xticks_location)  
        ax[-1].set_xticklabels(new_labels, rotation=0, ha='center', va="top")
        ax[-1].set_xlabel(xlabel_name)
    return fig, ax    
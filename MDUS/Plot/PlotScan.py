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
# from MDUS.Class import ScanDataClass

def PlotNew(self, start=None, end=None, fig = None, ax = None, fsize=(9,3.5),vmin=1e5,vmax=1e9, printxticks=True, printother=True):
    # initial setting
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
    # plot
    data_copy = self.value.copy()
    data_copy[EQTAB] = data_copy[EQTAB].replace(0,1e-38)
    pdata = data_copy[EQTAB].query('@ds <= index <= @de').values
    date = data_copy.query('@ds <= index <= @de').index.values
    # plot
    if not pdata.size == 0:
        cmap = plt.cm.jet
        cmap.set_under('white')
        cmap.set_bad('grey')
        hm = ax.pcolormesh(date,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
        hm.set_clim(vmin,vmax)
        ax.set_ylabel("Energy [keV/q]")    
        ax.set_yscale('log')
        ax.set_ylim(0.2,20)
        cbar = plt.colorbar(hm)
        cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
    else:
        print("Warning: No plot data")
        return fig, ax
    # ticks
    ax.xaxis.set_major_locator(ticker.LinearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d %H:%M:%S"))
    xlabels = [tick.get_text() for tick in ax.get_xticklabels()]
    xticks_location = ax.get_xticks()
    new_labels = []
    xlabel_name = "UTC"
    # other settings
    if printother:
        if "Orbit" in self.info.keys():
            orbit_num = "Orbit: " + str(self.info["Orbit"])
            ax.text(0, 1.0, orbit_num, ha='left', va='bottom', transform=ax.transAxes)
        dt = pd.to_datetime(self.value.query("@ds <= index <= @de").index.values[0]).strftime('%Y-%m-%d')
        ax.text(1.0, 1.0, dt, ha='right', va='bottom', transform=ax.transAxes)
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
        ax.set_xticks(xticks_location)  
        ax.set_xticklabels(new_labels, rotation=0, ha='center', va="top")
        ax.set_xlabel(xlabel_name)
    return fig, ax

def PlotAdvanced(self, start=None,end=None,fig=None,ax=None,fsize=(9,2.5),vmin=1e5,vmax=1e9,coordinate='MSO',skip_labels=False):
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
    data_copy = self.value.copy()
    data_copy[EQTAB] = data_copy[EQTAB].replace(0,1e-38)
    pdata = data_copy[EQTAB].query('@ds <= index <= @de').values
    date = data_copy.query('@ds <= index <= @de').index.values
    x_tmp = np.arange(len(date))
    # plot
    if not pdata.size == 0:
        cmap = plt.cm.jet
        cmap.set_under('white')
        cmap.set_bad('grey')
        hm = ax.pcolormesh(x_tmp,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
        hm.set_clim(vmin,vmax)
        ax.set_ylabel("Energy [keV/q]")    
        ax.set_yscale('log')
        ax.set_ylim(0.2,20)
        cbar = plt.colorbar(hm)
        cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
    else:
        print("Warning: No plot data")
        return fig, ax
    # xlabel
    # X軸の描画範囲
    xmin, xmax = ax.get_xlim()
    # Y軸の描画範囲
    ymin, ymax = ax.get_ylim()
    if not skip_labels:
        columns = self.value.columns.values
        columns = [str(col) for col in columns]
        date_str = pd.to_datetime(date).strftime("%H:%M").tolist()
        # coordinate
        if any("X_" + coordinate in s for s in columns):
            # 座標データがある場合
            if any(coordinate in s for s in columns):
                # 指定した座標系のデータがある場合
                X = data_copy["X_" + coordinate].values
                Y = data_copy["Y_" + coordinate].values
                Z = data_copy["Z_" + coordinate].values
                labels = "UT\n" + rf"$X_{{{coordinate}}}$" + "\n" + rf"$Y_{{{coordinate}}}$" + "\n" + rf"$Z_{{{coordinate}}}$" 
            else:
                # 指定した座標系のデータがない場合、MSOで代用
                X = data_copy["X_MSO"].values
                Y = data_copy["Y_MSO"].values
                Z = data_copy["Z_MSO"].values
                labels = "UT\n" + rf"$X_{{MSO}}$" + "\n" + rf"$Y_{{MSO}}$" + "\n" + rf"$Z_{{MSO}}$"
            x_str = np.char.mod('%.2f', X)
            y_str = np.char.mod('%.2f', Y)
            z_str = np.char.mod('%.2f', Z)
            x_ticks = [f'{d}\n{x}\n{y}\n{z:}' for d, x, y, z in zip(date_str, x_str, y_str, z_str)]
        else:
            x_ticks = date_str
            labels = "UTC"
        # ---
        n_labels = len(date)
        max_labels = 5
        step = max(1, n_labels // max_labels)
        tick_positions = list(range(0, n_labels, step))
        tick_labels = [x_ticks[i] for i in tick_positions]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=0, ha='center')
        renderer = fig.canvas.get_renderer()
        pos = tick_positions[0]
        label = ax.get_xticklabels()[0]
        label_fontsize = label.get_fontsize()
        bbox = label.get_window_extent(renderer=renderer)
        center_x = bbox.x0 + bbox.width / 2
        center_y = bbox.y0 + bbox.height / 2
        inv = ax.transData.inverted()
        data_x, data_y = inv.transform((center_x, center_y))
        if any("X_" + coordinate in s for s in columns):
            ax.text(data_x-40, ymin-0.112, labels, fontsize=label_fontsize, ha='center', va='center', zorder=20)
        else:
            ax.text(data_x-40, ymin-0.047, labels, fontsize=label_fontsize, ha='center', va='center', zorder=20)
        # Y label
        # ax.set_ylabel(ylabel)
        # =============== #
        title_fontsize = 10
        # title
        # X軸の描画範囲
        xmin, xmax = ax.get_xlim()
        # Y軸の描画範囲
        ymin, ymax = ax.get_ylim()
        # タイトルの位置（Y軸の最大値から少し上にオフセット）
        title_y = ymax + 1
        # 軌道番号（左端に左寄せ）
        if "Orbit" in self.info.keys():
            orbit_num = "Orbit: " + str(self.info["Orbit"])
            ax.text(xmin, title_y, orbit_num, ha='left', va='bottom', fontsize=title_fontsize)
        day = pd.to_datetime(date).strftime('%Y-%m-%d').tolist()[0]
        # 日付（右端に右寄せ）
        ax.text(xmax, title_y, day, ha='right', va='bottom', fontsize=title_fontsize)
    return fig, ax

# ----
def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),vmin=1e5,vmax=1e9,pxlabel=True,ptitle=True):
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
    data_copy = self.value.copy()
    data_copy[EQTAB] = data_copy[EQTAB].replace(0,1e-38)
    pdata = data_copy[EQTAB].query('@ds <= index <= @de').values
    date = data_copy.query('@ds <= index <= @de').index.values

    # plot
    if not pdata.size == 0:
        cmap = plt.cm.jet
        cmap.set_under('white')
        cmap.set_bad('grey')
        hm = ax.pcolormesh(date,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
        hm.set_clim(vmin,vmax)
        ax.set_ylabel("Energy [keV/q]")
        # xlabel
        if 'X_MSO' in self.value.columns.values:
            ticks_labels = []
            for time in data_copy.query('@ds <= index <= @de').index:
                x = data_copy.loc[time, 'X_MSO']
                y = data_copy.loc[time, 'Y_MSO']
                z = data_copy.loc[time, 'Z_MSO']
                label = f"{time.strftime('%H:%M')}\n{x:.2f}\n {y:.2f}\n {z:.2f}"
                ticks_labels.append(label)
            ticks_labels = np.array(ticks_labels)
            ticks_num = np.linspace(0,len(ticks_labels)-1,6).astype(int)
            ax.set_xticks(data_copy.query('@ds <= index <= @de').index.values[ticks_num])
            ax.set_xticklabels(ticks_labels[ticks_num])
            # ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
            if pxlabel:
                ax.set_xlabel("UTC and Coordinate")
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
            if pxlabel:
                ax.set_xlabel("UTC")
        # settings
        ax.set_yscale('log')
        ax.set_ylim(0.2,20)
        if ptitle:
            ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
        cbar = plt.colorbar(hm)
        cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
    else:
        print("Warning: No plot data")
    return fig, ax
# ScanDataClass.ScanData.Plot = Plot
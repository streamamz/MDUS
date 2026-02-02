import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

from MDUS.Spice.SpiceSetup import spice_exist
from MDUS.Constant.constant import *
import spiceypy as sp

# from MDUS.Class import MagDataClass

def PlotSetting(self,component={'Bx':'red','By':'blue','Bz':'green','Btot':'black'},
                ylabel='Magnetic Field [nT]',
                coordinate='MSO',
                title = None):
    self.plotinfo = {}
    self.plotinfo['component'] = component
    self.plotinfo['ylabel'] = ylabel
    if title is not None:
        self.plotinfo['title'] = title
    self.plotinfo['coordinate'] = coordinate

def Plot(self, start=None, end=None, fig = None, ax = None, fsize=(9,3.5), printxticks=True, printother=True):
    # initial setting
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)
    else:
        ds = self.value.dropna().index[0]
        de = self.value.dropna().index[-1]
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)   
    colors = ['black','red','blue','green']
    comp = ['Btot','Bx','By','Bz']
    ylabel = 'Magnetic Field [nT]'
    # load setting
    coordinate = "MSO"
    if hasattr(self,'plotinfo'):
        if 'component' in self.plotinfo.keys():
            colors = self.plotinfo['component'].values()
            comp = self.plotinfo['component'].keys()
        if 'ylabel' in self.plotinfo.keys():
            ylabel = self.plotinfo['ylabel']
        if 'coordinate' in self.plotinfo.keys():
            coordinate = self.plotinfo['coordinate']

    # plot
    for i, j in zip(comp, colors):
        ax.plot(
            self.value.query("@ds <= index <= @de").index.values,
            self.value.query("@ds <= index <= @de")[i].values,
            color=j,
            label=i,
            linewidth=1
        )    
    # ticks
    ax.xaxis.set_major_locator(ticker.LinearLocator(5))
    # ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=7))
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
    ax.legend(bbox_to_anchor=(1, 1), loc='upper left')
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
    ax.set_ylabel(ylabel)
    return fig, ax


# MagDataClass.MagData.PlotSetting = PlotSetting
def PlotAdvanced(self, start=None,end=None,fig=None,ax=None,fsize=(9,3.5),coordinate='MSO',skip_labels=False):
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
    comp = ['Btot','Bx','By','Bz']
    ylabel = 'Magnetic Field [nT]'
    # load setting
    coordinate = "MSO"
    if hasattr(self,'plotinfo'):
        if 'component' in self.plotinfo.keys():
            colors = self.plotinfo['component'].values()
            comp = self.plotinfo['component'].keys()
        if 'ylabel' in self.plotinfo.keys():
            ylabel = self.plotinfo['ylabel']
        if 'coordinate' in self.plotinfo.keys():
            coordinate = self.plotinfo['coordinate']
    # coordinate
    columns = self.value.columns.values
    exists = any(coordinate in s for s in columns)
    if exists:
        X = self.value["X_" + coordinate].values
        Y = self.value["Y_" + coordinate].values
        Z = self.value["Z_" + coordinate].values
    else:
        X = self.value["X_MSO"].values
        Y = self.value["Y_MSO"].values
        Z = self.value["Z_MSO"].values        
    time = self.value.index.values

    # plot
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize)
    
    for i, j in zip(comp, colors):
        ax.plot(
            self.value[i].values,
            color=j,
            label=i,
            linewidth=1
        )
    # xlabel
    if not skip_labels:
        x_str = np.char.mod('%.2f', X)
        y_str = np.char.mod('%.2f', Y)
        z_str = np.char.mod('%.2f', Z)
        date_str = pd.to_datetime(time).strftime('%H:%M').tolist()
        x_ticks = [f'{d}\n{x}\n{y}\n{z:}' for d, x, y, z in zip(date_str, x_str, y_str, z_str)]
        n_labels = len(time)
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
        labels = "UT\n" + rf"$X_{{{coordinate}}}$" + "\n" + rf"$Y_{{{coordinate}}}$" + "\n" + rf"$Z_{{{coordinate}}}$" 
        ax.text(data_x-600, data_y+10, labels, fontsize=label_fontsize, ha='center', va='center', zorder=20)
        title_fontsize = 10
        # title
        # X軸の描画範囲
        xmin, xmax = ax.get_xlim()
        # Y軸の描画範囲
        ymin, ymax = ax.get_ylim()
        # タイトルの位置（Y軸の最大値から少し上にオフセット）
        title_y = ymax + 10
        # 軌道番号（左端に左寄せ）
        if "Orbit" in self.info.keys():
            orbit_num = "Orbit: " + str(self.info["Orbit"])
            ax.text(xmin, title_y, orbit_num, ha='left', va='bottom', fontsize=title_fontsize)
        day = pd.to_datetime(time).strftime('%Y-%m-%d').tolist()[0]
        # 日付（右端に右寄せ）
        ax.text(xmax, title_y, day, ha='right', va='bottom', fontsize=title_fontsize)
    # Y label
    ax.set_ylabel(ylabel)
    # legend
    ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=10)
    # =============== #
    return fig, ax
# ----
def PlotOld(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),pxlabel=True,ptitle=True):
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
    comp = ['Btot','Bx','By','Bz']
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

    # 軌道データ (x, y, z) を x 軸の tick ラベルに表示
    ticks_labels = []
    for time in self.value.query('@ds <= index <= @de').index:
        x = self.value.loc[time, 'X_MSO']
        y = self.value.loc[time, 'Y_MSO']
        z = self.value.loc[time, 'Z_MSO']
        label = f"{time.strftime('%H:%M')}\n{x:.2f}\n {y:.2f}\n {z:.2f}"
        ticks_labels.append(label)
        

    ax.set_xticks(self.value.query('@ds <= index <= @de').index)
    ax.set_xticklabels(ticks_labels)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    
    if pxlabel:
        ax.set_xlabel('UTC')
    ax.set_ylabel(ylabel)
    if ptitle:
        ax.set_title(title)
    ax.set_zorder(2)
    return fig, ax 

# MagDataClass.MagData.Plot = Plot
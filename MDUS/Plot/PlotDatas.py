import matplotlib.pyplot as plt
import pandas as pd

# 現在はPlotNewのみ使用
def PlotNew(self,start=None,end=None,fig=None,ax=None,fsize=None,background=False):
    dtype = self.info["Load Success"]
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)    
    else:
        dss = []
        des = []
        for d in dtype:
            if d == "FIPS_DDR_ESPEC":
                keys = list(self.value[d].value.keys())
                dss.append(self.value[d].value[keys[0]].dropna().index.values[0])
                des.append(self.value[d].value[keys[0]].dropna().index.values[-1])
            else:
                dss.append(self.value[d].value.dropna().index.values[0])
                des.append(self.value[d].value.dropna().index.values[-1])
        ds = min(dss)
        de = max(des) 
    # fig, ax
    nplots = len(dtype)
    if "FIPS_DDR_ESPEC" in dtype:
        nplots = nplots + len(list(self.value["FIPS_DDR_ESPEC"].value.keys())) - 1
    if fsize is None:
        fsize = (12,3*nplots)
    if fig is None or ax is None:
        fig, ax = plt.subplots(nrows=nplots,figsize=fsize,sharex=True,constrained_layout=True)
    plotscounter = 0
    if len(dtype) == 1:
        if background:
            if dtype[i] == "FIPS_CDR_SCAN":
                ax[i].set_facecolor('grey') 
        self.value[dtype[0]].Plot(fig=fig,ax=ax,start=ds,end=de)       
    else:
        for i in range(len(dtype)):
            if background:
                if dtype[i] == "FIPS_CDR_SCAN":
                    ax[i].set_facecolor('grey')
            if dtype[i] == "FIPS_DDR_ESPEC":
                for k in range(len(list(self.value[dtype[i]].value.keys()))):
                    plotscounter += 1
                    self.value[dtype[i]].Plot(target=list(self.value[dtype[i]].value.keys())[k],fig=fig,ax=ax[plotscounter-1],start=ds,end=de,
                                              printxticks=True if plotscounter == nplots else False,printother=True if plotscounter == 1 else False)
            else:
                plotscounter += 1
                self.value[dtype[i]].Plot(fig=fig,ax=ax[plotscounter-1],start=ds,end=de,
                                          printxticks=True if plotscounter == nplots else False,printother=True if plotscounter == 1 else False)
    return fig, ax  

def PlotOld(self,start=None,end=None,fig=None,ax=None,fsize=None,background=False):
    dtype = self.info["Load Success"]
    # ds, de
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)    
    else:
        dss = []
        des = []
        for d in dtype:
            dss.append(self.value[d].value.dropna().index.values[0])
            des.append(self.value[d].value.dropna().index.values[-1])
        ds = min(dss)
        de = max(des)
    # fig, ax
    if fsize is None:
        fsize = (12,3*len(dtype))
    if fig is None or ax is None:
        fig, ax = plt.subplots(nrows=len(dtype),figsize=fsize,sharex=True,constrained_layout=True)
    if len(dtype) == 1:
        if background:
            if dtype[i] == "FIPS_CDR_SCAN":
                ax[i].set_facecolor('grey') 
        self.value[dtype[0]].Plot(fig=fig,ax=ax,start=ds,end=de)       
    else:
        for i in range(len(dtype)):
            if background:
                if dtype[i] == "FIPS_CDR_SCAN":
                    ax[i].set_facecolor('grey')
            if i == 0:
                self.value[dtype[i]].PlotOld(fig=fig,ax=ax[i],start=ds,end=de,pxlabel=False,ptitle=True)
            elif i == len(dtype)-1:
                self.value[dtype[i]].PlotOld(fig=fig,ax=ax[i],start=ds,end=de,ptitle=False,pxlabel=True)
            else:
                self.value[dtype[i]].PlotOld(fig=fig,ax=ax[i],start=ds,end=de,pxlabel=False,ptitle=False)
        plt.grid(False)
    return fig, ax

# DatasClass.Datas.Plot = Plot
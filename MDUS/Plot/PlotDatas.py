import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
import pandas as pd

# # from MDUS.Class import DatasClass
# def PlotAdvanced(self, start=None,end=None,fig=None,ax=None,fsize=None,coordinate='MSO'):
#     # plotするデータタイプの取得
#     dtype = self.info["Load Success"]
#     # ds, de
#     dss = []
#     des = []
#     for d in dtype:
#         dss.append(self.value[d].value.dropna().index.values[0])
#         des.append(self.value[d].value.dropna().index.values[-1])
#     ds_tmp = min(dss)
#     de_tmp = max(des)
#     if start is not None:
#         ds = pd.to_datetime(start)
#     else:
#         ds = ds_tmp
#     if end is not None:
#         de = pd.to_datetime(end)
#     else:
#         de = de_tmp
#     # fig, ax
#     if fsize is None:
#         fsize = (12,3*len(dtype))
#     if fig is None or ax is None:
#         fig, ax = plt.subplots(nrows=len(dtype),figsize=fsize,sharex=True,constrained_layout=True)
#     # plot
#     for i in range(len(dtype)):
#         self[dtype[i]].Plot(start=ds,end=de,fig=fig,ax=ax[i],
#                                     fsize=(12,3),
#                                     coordinate=coordinate)
#     return fig, ax

def Plot(self,start=None,end=None,fig=None,ax=None,fsize=None,background=False):
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
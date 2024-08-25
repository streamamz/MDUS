import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
import pandas as pd

def plot_mag(data,component,colors,ds=None,de=None):
    if ds != None and de != None:
        ds = pd.to_datetime(ds)
        de = pd.to_datetime(de)
    else:
        ds = data.index[0]
        de = data.index[-1]
    fig, ax = plt.subplots(figsize=(9,3))
    for comp,color in zip(component,colors):
        ax.plot(data.query('@ds <= index <= @de').index,data.query('@ds <= index <= @de')[comp],color=color,label=comp,linewidth=1)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("UTC")
    ax.set_ylabel("Magnetic Field [nT]")
    ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
    return fig, ax
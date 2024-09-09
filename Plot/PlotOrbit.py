import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from MDUS.Class import MagDataClass

theta = np.arange(0,2*np.pi+0.01,0.01)

def PlotOrbit(self,fig=None,ax=None,coordinate='XY',label='',color='red',filename='None'):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(6,6))
        ax.invert_xaxis()
        ax.set_xlim(2,-2)
        ax.set_ylim(-2,2)
        ax.set_aspect('equal')
        if 'X' in coordinate:
            w = patches.Wedge((0,0),1,theta1=90,theta2=270,color='black')
            ax.add_patch(w)
        ax.plot(np.cos(theta),np.sin(theta),color='black',zorder=-1)
    coor1 = coordinate[0] + '_MSO'
    coor2 = coordinate[1] + '_MSO'
    ax.plot(self.value[coor1].values,self.value[coor2].values,label=label,color=color)
    if label != '':
        ax.legend()
    ax.set_xlabel(coor1 + ' [Rm]')
    ax.set_ylabel(coor2 + ' [Rm]')
    if filename != 'None':
        fig.tight_layout()
        fig.savefig(filename)
    return fig, ax

MagDataClass.MagData.PlotOrbit = PlotOrbit
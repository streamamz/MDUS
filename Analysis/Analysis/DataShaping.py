import numpy as np
import pandas as pd
from MDUS.Class import MagDataClass

# MLATの計算
def MLAT(self):
    x = self.value['X_MSO'].values.copy()
    y = self.value['Y_MSO'].values.copy()
    z = self.value['Z_MSO'].values.copy() - 0.2
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z/r)
    self.value['MLAT'] = -np.rad2deg(theta) + 90

MagDataClass.MagData.MLAT = MLAT

# 移動平均
def MoveAverage(self,window=3,component=['Bx','By','Bz','|B|'],replace=True):
    if window % 2 == 0:
        window += 1
    result = pd.DataFrame()
    result['date'] = self.value.index.values.copy()[window//2:-window//2]
    for cname in self.value:
        if cname in component:
            tmp = np.convolve(self.value[cname], np.ones(window)/window, mode='same').copy()[window//2:-window//2]
        else:
            tmp = self.value[cname].values.copy()[window//2:-window//2]
        result[cname] = tmp
    result = result.set_index('date')
    if replace:
        self.value = result
        self.info['Move Average'] = window 
    else:
        return result
MagDataClass.MagData.MoveAverage = MoveAverage
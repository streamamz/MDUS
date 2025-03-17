import numpy as np
import pandas as pd

from astroquery.jplhorizons import Horizons
from astropy.time import Time

from MDUS.Data.constant import * 

from MDUS.Class import MagDataClass

# 座標変換用メソッド
def CTransform(self,coordinate='MSM',replace=False):
    # Error
    if not coordinate in ['MSM','aMSM','MCOOR']:
        raise ValueError("Error: coordinate must be MSM, aMSM or MCOOR")
    # --- #
    x = self.value['X_MSO'].values.copy()
    y = self.value['Y_MSO'].values.copy()
    z = self.value['Z_MSO'].values.copy() - 0.2
    if replace:
        self.value = self.value.drop(['X_MSO','Y_MSO','Z_MSO'],axis=1)
        tmp = self.value.columns.values
    # MSM coordinate
    if coordinate == 'MSM':
        self.value['X_MSM'] = x
        self.value['Y_MSM'] = y
        self.value['Z_MSM'] = z
        coordinate_name = np.array(['X_MSM','Y_MSM','Z_MSM'])
    # aberatted-MSM coordinate
    if coordinate == 'aMSM':
        dt = Time(self.value.dropna().index.values[0]).jd1
        r_hel = Horizons(id='199',location='@sun',epochs=dt).vectors()['range'].value[0]
        beta = np.arctan(-np.sqrt(G*M*(2/(r_hel*au*1e3) - 1/(smaxis*1e3))) * 1e-3/vsw)
        rotvector = np.array([
            [np.cos(beta), -np.sin(beta), 0],
            [np.sin(beta), np.cos(beta), 0],
            [0, 0, 1]
        ])
        points = np.vstack([x,y,z])
        rotated_points = rotvector @ points
        self.value['X_aMSM'] = rotated_points[0]
        self.value['Y_aMSM'] = rotated_points[1]
        self.value['Z_aMSM'] = rotated_points[2]
        coordinate_name = np.array(['X_aMSM','Y_aMSM','Z_aMSM'])
    # Magnetic coordinate
    if coordinate == 'MCOOR':
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = 90 - np.rad2deg(np.arccos(z/r))
        phi = np.rad2deg(np.arctan2(y,x))
        phi = np.where(phi < 0, phi+360, phi)
        self.value['R_MSM'] = r
        self.value['MLAT'] = theta
        self.value['MLON'] = phi
        self.value["MLT"] = (phi/15 + 12) % 24
        coordinate_name = np.array(['R_MSM','MLAT','MLON','MLT'])
    
    if replace:
        self.value = self.value.reindex(columns=np.concatenate([coordinate_name,tmp]))
MagDataClass.MagData.CTransform = CTransform

# 移動平均
def MoveAverage(self,window=3,component=None):
    if component is None:
        self.value = self.value.rolling(window=window,center=True).mean()
    else:
        self.value[component] = self.value[component].rolling(window=window,center=True).mean()
    self.info['Move Average'] = window
MagDataClass.MagData.MoveAverage = MoveAverage
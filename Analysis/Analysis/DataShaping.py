import numpy as np
import pandas as pd
from MDUS.Class import MagDataClass
from MDUS.Class import ScanDataClass
from MDUS.Data import constant as cst
from scipy import interpolate

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

# 座標データをscanデータに入れる
# 時間分解能ゆえに，scanデータに補間する
def DataIntegration(self,magdata=None):
    if magdata is None:
        ds = self.info['Start Date']
        de = self.info['End Date']
        magdata = MagDataClass.MagData()
        magdata.Input(start=ds,end=de)
    data_scan_unix = [x.timestamp() for x in pd.to_datetime(self.value.index.values)]
    data_mag_unix = [x.timestamp() for x in pd.to_datetime(magdata.value.index.values)]

    fbx = interpolate.interp1d(data_mag_unix,magdata.value['Bx'].values)
    fby = interpolate.interp1d(data_mag_unix,magdata.value['By'].values)
    fbz = interpolate.interp1d(data_mag_unix,magdata.value['Bz'].values)
    fbabs = interpolate.interp1d(data_mag_unix,magdata.value['|B|'].values)
    fx = interpolate.interp1d(data_mag_unix,magdata.value['X_MSO'].values)
    fy = interpolate.interp1d(data_mag_unix,magdata.value['Y_MSO'].values)
    fz = interpolate.interp1d(data_mag_unix,magdata.value['Z_MSO'].values)
    
    self.value['Bx'] = fbx(data_scan_unix)
    self.value['By'] = fby(data_scan_unix)
    self.value['Bz'] = fbz(data_scan_unix)
    self.value['|B|'] = fbabs(data_scan_unix)
    self.value['X_MSO'] = fx(data_scan_unix)
    self.value['Y_MSO'] = fy(data_scan_unix)
    self.value['Z_MSO'] = fz(data_scan_unix)

    self.info['Data Integration'] = True
    self.info['Second'] = magdata.info['Second']
    self.info['unit'] = magdata.info['unit']
ScanDataClass.ScanData.DataIntegration = DataIntegration

# 圧力等を計算
energy = np.array(list(reversed(cst.EQTAB.copy())))
velocity = energy * 1000
velocity *= cst.ev
velocity *= 2/cst.mass
velocity = np.array(list(map(np.sqrt,velocity)))
def NTP(self):
    psd = pd.DataFrame()
    psd['date'] = self.value.index.copy()
    for i in range(len(velocity)):
        psd[energy[i]] = self.value[energy[i]].values * cst.mass /velocity[i]**2 / cst.C
    psd = psd.set_index('date')
    # 物理量計算
    # N
    tmp = []
    for i in psd.itertuples():
        tmp1 = 0
        for j in range(len(velocity)-1):
            if float(energy[j]) < 0.1:
                continue
            tmp1 += (i[j+1]*velocity[j]**2 + i[j+2]*velocity[j+1]**2) * (velocity[j] - velocity[j+1]) * 0.5
        tmp1 *= cst.omega
        tmp.append(tmp1)
    tmp = np.array(tmp)
    self.value['N'] = tmp*1e-6
    # P
    tmp = []
    for i in psd.itertuples():
        tmp1 = 0
        for j in range(len(velocity)-1):
            if float(energy[j]) < 0.1:
                continue
            tmp1 += cst.mass * (i[j+1]*velocity[j]**4 + i[j+2]*velocity[j+1]**4) * (velocity[j] - velocity[j+1]) * 0.5
        tmp1 *= cst.omega
        tmp.append(tmp1)
    tmp = np.array(tmp)
    self.value['P'] = tmp*1e9 * cst.magicnumber_p * cst.magicnumber_t
    # T
    self.value['T'] = self.value['P']*1e-9 / (self.value['N'] * 1e5 * cst.kb) * 1e-6
ScanDataClass.ScanData.NTP = NTP

# # 反磁性電流の計算
# def DCurrent(self,ds=None,de=None):
#     if 'Data Integration' not in self.info.keys():
#         self.DataIntegration()
#     if ds is None or de is None:
#         ds = self.value.index[0].copy()
#         de = self.value.index[-1].copy()
#     x = self.value['X_MSO'].values.copy() * 1e3
#     y = self.value['Y_MSO'].values.copy() * 1e3
#     z = self.value['Z_MSO'].values.copy() * 1e3
#     if self.info['unit'] == 'Rm':
#         x *= cst.Rm
#         y *= cst.Rm
#         z *= cst.Rm
#     Bx = self.value['Bx'].values * 1e-9
#     By = self.value['By'].values * 1e-9
#     Bz = self.value['Bz'].values * 1e-9
#     Babs = self.value['|B|'].values * 1e-9


# ScanDataClass.ScanData.DCurrent = DCurrent
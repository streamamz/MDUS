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
ScanDataClass.ScanData.MLAT = MLAT

# 移動平均
# <- 古いコードは正しく動いていないことが確認
# 代わりに, pandasのrollingを使う
# <- 動いていた可能性あり（componentの指定忘れていた...）
# def MoveAverage(self,window=3,component=['Bx','By','Bz','|B|'],replace=True):
#     if window % 2 == 0:
#         window += 1
#     result = pd.DataFrame()
#     result['date'] = self.value.index.values.copy()[window//2:-window//2]
#     for cname in self.value:
#         if cname in component:
#             tmp = np.convolve(self.value[cname], np.ones(window)/window, mode='same').copy()[window//2:-window//2]
#         else:
#             tmp = self.value[cname].values.copy()[window//2:-window//2]
#         result[cname] = tmp
#     result = result.set_index('date')
#     if replace:
#         self.value = result
#         self.info['Move Average'] = window 
#     else:
#         return result
def MoveAverage(self,window=3,component=None):
    if component is None:
        self.value = self.value.rolling(window=window,center=True).mean()
    else:
        self.value[component] = self.value[component].rolling(window=window,center=True).mean()
    self.info['Move Average'] = window
MagDataClass.MagData.MoveAverage = MoveAverage
ScanDataClass.ScanData.MoveAverage = MoveAverage

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

    # データ点が外側のものは外挿
    fbx = interpolate.interp1d(data_mag_unix,magdata.value['Bx'].values,fill_value="extrapolate")
    fby = interpolate.interp1d(data_mag_unix,magdata.value['By'].values,fill_value="extrapolate")
    fbz = interpolate.interp1d(data_mag_unix,magdata.value['Bz'].values,fill_value="extrapolate")
    fbabs = interpolate.interp1d(data_mag_unix,magdata.value['|B|'].values,fill_value="extrapolate")
    fx = interpolate.interp1d(data_mag_unix,magdata.value['X_MSO'].values,fill_value="extrapolate")
    fy = interpolate.interp1d(data_mag_unix,magdata.value['Y_MSO'].values,fill_value="extrapolate")
    fz = interpolate.interp1d(data_mag_unix,magdata.value['Z_MSO'].values,fill_value="extrapolate")
    
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
    self.value['T'] = self.value['P']*1e-9 / (self.value['N'] * 1e6 * cst.kb) * 1e-6
ScanDataClass.ScanData.NTP = NTP

# ∇ｘB電流の計算
def rotBCurrent(self,ds=None,de=None,model=True):
    if self.info['Data Type'] == 'SCAN' and 'Data Integration' not in self.info.keys():
        self.DataIntegration()
    if ds is None or de is None:
        ds = self.value.index[0]
        de = self.value.index[-1]

    result = self.value.query('@ds <= index <= @de').copy()

    x = result['X_MSO'].values.copy() * 1e3
    y = result['Y_MSO'].values.copy() * 1e3
    z = result['Z_MSO'].values.copy() * 1e3
    if self.info['unit'] == 'Rm':
        x *= cst.Rm
        y *= cst.Rm
        z *= cst.Rm

    if model:
        Bx = result['Bx'].values.copy() * 1e-9 - result['Bx_KTH22'].values.copy() * 1e-9
        By = result['By'].values.copy() * 1e-9 - result['By_KTH22'].values.copy() * 1e-9
        Bz = result['Bz'].values.copy() * 1e-9 - result['Bz_KTH22'].values.copy() * 1e-9
    else:
        Bx = result['Bx'].values.copy() * 1e-9
        By = result['By'].values.copy() * 1e-9
        Bz = result['Bz'].values.copy() * 1e-9

    Jx_l = np.gradient(Bz, y) / cst.mu0
    Jx_r = -np.gradient(By, z) / cst.mu0
    Jx = Jx_l + Jx_r

    Jy_l = np.gradient(Bx, z) / cst.mu0
    Jy_r = -np.gradient(Bz, x) / cst.mu0
    Jy = Jy_l + Jy_r

    Jz_l = np.gradient(By, x) / cst.mu0
    Jz_r = -np.gradient(Bx, y) / cst.mu0
    Jz = Jz_l + Jz_r

    result['Jx_rot'] = Jx
    result['Jx_rot_first'] = Jx_l
    result['Jx_rot_second'] = Jx_r
    result['Jy_rot'] = Jy
    result['Jy_rot_first'] = Jy_l
    result['Jy_rot_second'] = Jy_r
    result['Jz_rot'] = Jz
    result['Jz_rot_first'] = Jz_l
    result['Jz_rot_second'] = Jz_r

    self.value = pd.merge(self.value,result,how='left',left_index=True,right_index=True,suffixes=('', '_new'))
    self.value = self.value.drop(columns=[i for i in self.value.columns if '_new' in i])
ScanDataClass.ScanData.rotBCurrent = rotBCurrent
MagDataClass.MagData.rotBCurrent = rotBCurrent

# 反磁性電流の計算
def DiamagCurrent(self,ds=None,de=None):
    if 'Data Integration' not in self.info.keys():
        self.DataIntegration()
    if ds is None or de is None:
        ds = self.value.index[0]
        de = self.value.index[-1]
    
    result = self.value.query('@ds <= index <= @de').copy()
    
    x = result['X_MSO'].values.copy() * 1e3
    y = result['Y_MSO'].values.copy() * 1e3
    z = result['Z_MSO'].values.copy() * 1e3
    if self.info['unit'] == 'Rm':
        x *= cst.Rm
        y *= cst.Rm
        z *= cst.Rm
    Bx = result['Bx'].values.copy() * 1e-9
    By = result['By'].values.copy() * 1e-9
    Bz = result['Bz'].values.copy() * 1e-9
    Babs = result['|B|'].values.copy() * 1e-9
    pressure = result['P'].values.copy() * 1e-9

    # 正しいのか要確認
    Jx = []
    Jy = []
    Jz = []

    dpxs = []
    dpys = []
    dpzs = []

    for i in range(len(x)):
        if i == 0 or i == len(x)-1:
            Jx.append(np.nan)
            Jy.append(np.nan)
            Jz.append(np.nan)

            dpxs.append(np.nan)
            dpys.append(np.nan)
            dpzs.append(np.nan)
        else:
            dx = x[i+1] - x[i-1]
            dy = y[i+1] - y[i-1]
            dz = z[i+1] - z[i-1]

            dpx = (pressure[i+1] - pressure[i-1])/dx
            dpy = (pressure[i+1] - pressure[i-1])/dy
            dpz = (pressure[i+1] - pressure[i-1])/dz

            Jx.append((By[i]*dpz - Bz[i]*dpy) / Babs[i]**2)
            Jy.append((Bz[i]*dpx - Bx[i]*dpz) / Babs[i]**2)
            Jz.append((Bx[i]*dpy - By[i]*dpx) / Babs[i]**2)

            dpxs.append(dpx)
            dpys.append(dpy)
            dpzs.append(dpz)

    # gradpx = np.gradient(pressure, x)
    # gradpy = np.gradient(pressure, y)
    # gradpz = np.gradient(pressure, z)

    # Jx = (By*gradpz - Bz*gradpy) / Babs**2
    # Jy = (Bz*gradpx - Bx*gradpz) / Babs**2
    # Jz = (Bx*gradpy - By*gradpx) / Babs**2

    result['Jx_diamag'] = Jx
    result['Jy_diamag'] = Jy
    result['Jz_diamag'] = Jz

    result['gradPx'] = dpxs
    result['gradPy'] = dpys
    result['gradPz'] = dpzs

    self.value = pd.merge(self.value,result,how='left',left_index=True,right_index=True,suffixes=('', '_new'))
    self.value = self.value.drop(columns=[i for i in self.value.columns if '_new' in i])
ScanDataClass.ScanData.DiamagCurrent = DiamagCurrent
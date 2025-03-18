from MDUS.Input import  InputFunction as ipf
from MDUS.Setting.setting import setting
import MDUS.Data.constant as cst
from MDUS.Data.data import orbit as orbits
from MDUS.Convert.ConvertMag import magconvert

import pandas as pd
import numpy as np
import os 
from pathlib import Path

from MDUS.Class import MagDataClass

def magsetting(self,sec=1,Rm=True):
    if sec not in [1,5,10,60]:
        raise ValueError("Error: sec must be 1, 5, 10, or 60")
    else:
        self.info["Second"] = sec
        self.setting = True
    if Rm:
        self.info["unit"] = "Rm"
    else:
        self.info["unit"] = "km"
MagDataClass.MagData.Setting = magsetting

def magload(self,start=None,end=None,orbit=None):
    # 対応付ファイルの作成・読み込み
    files = os.listdir("./MDUS/Data")
    if 'MagOPMap.pkl' in files:
        mapfile = pd.read_pickle('./MDUS/Data/MagOPMap.pkl')
    else:
        mapfile = pd.DataFrame()
        mapfile['pfile'] = []
        mapfile['ofile'] = []
        mapfile.to_pickle('./MDUS/Data/MagOPMap.pkl')
    # 例外処理
    if start is None and end is None and orbit is None:
        raise ValueError("Error: start, end, and orbit cannot be None at the same time")
    # 時刻計算
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['MP1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['MP4'].values[0])
    else:
        startdate,enddate = ipf.convert_to_datetime(start,end)
    # データ読み込み
    ofile = []
    pfile = []
    result = pd.DataFrame()
    if self.setting:
        sec = self.info["Second"] 
    else:
        sec = 1
        self.info["unit"] = "Rm"

    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        pfile.append(setting["MAG"]["pfile_path"] + "/" + str(year)+"_"+str(day).zfill(3)+"_"+str(sec).zfill(2)+".pkl")
    for file in pfile:
        try:
            df = pd.read_pickle(file)
            result = pd.concat([result,df])
            ofile.append(mapfile.query('pfile == @file')['ofile'].values[0])
        # ofileがあるときにはloadしたうえでpfileに変換
        except FileNotFoundError:
        # pikle fileがないときにはoriginal fileを探してくる
            print("Error: " + file + " is not found")
            ofile_tmp = setting["MAG"]["format"] + str(year-2000)+str(day).zfill(3)+"_"+str(sec).zfill(2)
            ofile_dir = Path(setting["MAG"]["ofile_path"])
            ofile_path = [file for file in ofile_dir.rglob("*") if file.is_file() and ofile_tmp in file.name and 'TAB' in file.name]
            if len(ofile_path) != 0:
                print("Found original file. Convert to pickle file")
                ofile.append(str(ofile_path[0]))
                result, mapfile = magconvert(str(ofile_path[0]),file,mapfile)
            else:
                print("Error: There is no data file. Please download from PDS.")
                self.value = None
                return
            # for ofile in ofile_path:
            #     if ofile in 
            # ofiles = os.listdir(setting["MAG"]["ofile_path"])
            # ofile_found = False
            # for ofile in ofiles:
            #     m = re.match(r'MAGMSOSCIAVG(\d{2})(\d{3})_(\d{2}).*', ofile)
            #     if not(int(m.group(1)) == year-2000 and int(m.group(2)) == day and int(m.group(3)) == sec):
            #         continue
            #     else:
            #         print("Found original file. Convert to pickle file")
            #         ofile_found = True
            #         result, mapfile = magconvert(ofile,file,mapfile)
        # ofileがないときにはエラー処理
            # if not ofile_found:
            #     print("Error: There is no data file. Please download from PDS.")
            #     # print("You need to download ")
            #     self.value = None
            #     return
    result['|B|'] = np.sqrt(np.array(result['Bx'].values) ** 2 + np.array(result['By'].values) ** 2 + np.array(result['Bz'].values) ** 2)
    result = result[['X_MSO','Y_MSO','Z_MSO','Bx','By','Bz','|B|']].copy()
    result = result.query('@startdate <= index <= @enddate')

    if self.info["unit"] == "Rm":
        result.loc[:,'X_MSO'] /= cst.Rm
        result.loc[:,'Y_MSO'] /= cst.Rm
        result.loc[:,'Z_MSO'] /= cst.Rm
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile
    self.value = result 
    mapfile.to_pickle('./MDUS/Data/MagOPMap.pkl')   
MagDataClass.MagData.LoadData = magload
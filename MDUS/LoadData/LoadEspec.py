from MDUS.LoadData import LoadFunction as ldf
from MDUS.Data.data import orbit as orbits
import MDUS.Constant.constant as cst
from MDUS.Convert.ConvertEspec import especconvert

import pandas as pd
import numpy as np

def especsetting(self,target=["H+"],quality=0) -> None:
    targets = ["H+","He2+","He+", "Na+", "O+"]
    for t in target:
        if t not in targets:
            raise ValueError("target must be H+, He2+, He+, Na+, or O+")
    self.info["Target"] = target

def especload(self,start=None,end=None,orbit=None) -> None:
    # 例外処理
    if start is None and end is None and orbit is None:
        raise ValueError("start, end, and orbit cannot be None at the same time")   
    if orbit is not None and orbit not in orbits.index.values:
        raise ValueError("No orbit data found") 

    # 時刻処理
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['MP1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['MP4'].values[0])
    else:
        startdate,enddate = ldf.convert_to_datetime(start,end)

    # データ読み込み
    ofile = []
    pfile = {}
    result = {}

    # settingの読み込み
    if "Target" not in self.info.keys():
        target = ["H+"]
        self.info["Target"] = target
    else:
        target = self.info["Target"]

    # 読み込むファイルの取得
    years = []
    days = []
    for i in range(len(target)):
        pfile[target[i]] = []
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        years.append(year)
        days.append(day)
        # ---
        # list形式の各要素をpfileに追加
        for t in target:
            pfile[t].append(ldf.found_pfile("FIPS_DDR_ESPEC",year,day,target=t))
        tmp = ldf.found_ofile("FIPS_DDR_ESPEC",year,day)
        if len(tmp) == 0:
            print("Warning: Cannot find original file")
            self.value = None
        ofile.append(str(tmp[-1]))   
    
    # データファイルがあるかの確認
    for t in target:
        result[t] = pd.DataFrame()
        for p, o, year, day in zip(pfile[t], ofile, years, days):
            try:
                df = pd.read_pickle(p)
                result[t] = pd.concat([result[t],df])
            except FileNotFoundError:
                print("Warning: %s not found" % p)
                if len(ofile) == 0:
                    print("original data path may not be correct")
                    print("Please check the datapath.json file")
                    self.value = None
                    return
                else:
                    print("Found original file. Convert to pickle file")  
                    df = especconvert(o,p,t,year,day)
                    result[t] = pd.concat([result[t],df])        
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile    
    for t in target:
        result[t] = result[t].query('@startdate <= index <= @enddate')
    self.value = result                
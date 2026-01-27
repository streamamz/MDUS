from MDUS.LoadData import LoadFunction as ldf

from MDUS.Data.data import orbit as orbits
import MDUS.Constant.constant as cst

import pandas as pd
import numpy as np

def ionntpload(self,start=None,end=None,orbit=None) -> None:
    # 例外処理
    if start is None and end is None and orbit is None:
        raise ValueError("start, end, and orbit cannot be None at the same time")    

    # 時刻処理
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['BS1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['BS4'].values[0])
    else:
        startdate,enddate = ldf.convert_to_datetime(start,end)

    # データ読み込み
    ofile = []
    pfile = []
    result = pd.DataFrame()

    # 読み込むファイルの取得
    years = []
    days = []
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        years.append(year)
        days.append(day)
        pfile.append(ldf.found_pfile("Ion_NTP",year,day))
        tmp = ldf.found_ofile("Ion_NTP",year,day)
        if len(tmp) == 0:
            print("Warning: Cannot find original file")
            self.value = None
        ofile.append(str(tmp[-1]))

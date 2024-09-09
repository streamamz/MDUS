from MDUS.Input import  InputFunction as ipf
from MDUS.Setting.setting import setting
import MDUS.Data.constant as cst
from MDUS.Data.data import orbit as orbits
import pandas as pd
import numpy as np

from MDUS.Class import ScanDataClass

# protonのみ対応
def scaninput(self,start=None,end=None,orbit=None,datatype="proton"):
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['MP1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['MP4'].values[0])
    else:
        startdate,enddate = ipf.convert_to_datetime(start,end)
    ofile = []
    pfile = []
    result = pd.DataFrame()
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        pfile.append(setting["FIPS_CDR_SCAN"]["path"] + "/" + str(year)+"_"+str(day).zfill(3) + "_" + datatype +".pkl")
    for file in pfile:
        try:
            df = pd.read_pickle(file)
            result = pd.concat([result,df])
        except FileNotFoundError:
            print("Error: " + file + " is not found")
    result = result.query('@startdate <= index <= @enddate')
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile
    self.info["Scan Data Type"] = datatype
    self.value = result

ScanDataClass.ScanData.Input = scaninput
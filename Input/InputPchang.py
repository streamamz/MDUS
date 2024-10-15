from MDUS.Input import InputFunction as ipf
from MDUS.Setting.setting import setting
from MDUS.Data.data import orbit as orbits
import pandas as pd
import numpy as np

from MDUS.Class import PchangDataClass

def pchanginput(self,start=None,end=None,orbit=None,datatype='H_PA'):
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
        pfile.append(setting["PCHANG"]["path"] + "/" + datatype + "/" + str(year)+"_"+str(day).zfill(3) + ".pkl")
    for file in pfile:
        try:
            df = pd.read_pickle(file)
            result = pd.concat([result,df])
        except FileNotFoundError:
            print("Error: " + file + " is not found")
            return
    result = result.query('@startdate <= index <= @enddate')
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile
    self.info["Pchang Data Type"] = datatype
    self.value = result

PchangDataClass.PchangData.Input = pchanginput
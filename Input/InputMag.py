from MDUS.Input import  InputFunction as ipf
from MDUS.Setting.setting import setting
import MDUS.Data.constant as cst
import pandas as pd
import numpy as np


def maginput(start,end,orbit=None,sec=1,Rm=True):
    if orbit is not None:
        startdate = pd.to_datetime(ipf.orbit.query('index == @orbit')['MP1'].values[0])
        enddate = pd.to_datetime(ipf.orbit.query('index == @orbit')['MP4'].values[0])
    else:
        startdate,enddate = ipf.convert_to_datetime(start,end)
    ofile = []
    pfile = []
    result = pd.DataFrame()
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        pfile.append(setting["MAG"]["path"] + "/" + str(year)+"_"+str(day).zfill(3)+"_"+str(sec).zfill(2)+".pkl")
    for file in pfile:
        try:
            df = pd.read_pickle(file)
            result = pd.concat([result,df])
        except FileNotFoundError:
            print("Error: " + file + " is not found")
    result['|B|'] = np.sqrt(np.array(result['Bx'].values) ** 2 + np.array(result['By'].values) ** 2 + np.array(result['Bz'].values) ** 2)
    result = result[['X_MSO','Y_MSO','Z_MSO','Bx','By','Bz','|B|']].copy()
    result = result.query('@startdate <= index <= @enddate')
    if Rm:
        result.loc[:,'X_MSO'] /= cst.Rm
        result.loc[:,'Y_MSO'] /= cst.Rm
        result.loc[:,'Z_MSO'] /= cst.Rm
    return startdate,enddate,ofile,pfile,result
import os
import shutil

import pandas as pd
import json
from pathlib import Path

import MDUS.Input.InputFunction as ip

def maginput(start,end,sec):
    result = pd.DataFrame()
    days = ip.get_totaldays(start,end)
    ofile, pfile = get_filename(days,sec)
    for p, o in zip(pfile,ofile):
        ptmp = setting["MAG"]["path"] + "/" + setting["MAG"]["name"] + "/" + p
        if os.path.isfile(ptmp):
            tmp = pd.read_pickle(ptmp)
        else:
            ip.make_directory("MAG")
            files = os.listdir(setting["MAG"]["path"])
            ftmp = [s for s in files if o in s]
            if len(ftmp) == 0:
                raise Exception("Error!: There is not an original file")
            else:
                otmp = ftmp[0]
                tmp = convert_file(ptmp,otmp)
        result = pd.concat([result,tmp])
    return ofile,pfile,result

# ====== sub function =====
# ==== setting file ====
setting_path = Path(__file__).resolve().parent.parent.joinpath("setting.json")
setting = open(setting_path,'r')
setting = json.load(setting)
# === get file name ===
pklfile_format = '%d_%03d_%02d.pkl'
ofile_format = format = 'MAGMSOSCIAVG%d%03d_%02d'#.*\.TAB'
def get_filename(days,sec):
    ofile = []
    pfile = []
    for i in days:
        ofile.append(ofile_format %(i[0]-2000,i[1],sec))
        pfile.append(pklfile_format %(i[0]-2000,i[1],sec))
    return ofile,pfile

# === convert file ===
def convert_file(pfile,ofile):
    otmp = setting["MAG"]["path"] + "/" + ofile
    tmp = pd.read_csv(otmp,header=None,delim_whitespace=True)
    shutil.move(otmp,setting["MAG"]["path"] + "/" + setting["MAG"]["name"] + "/original/" + ofile)
    tmp = modify_data(tmp)
    tmp.to_pickle(pfile)
    return tmp

# === modify data ===
def modify_data(data):
    result = pd.DataFrame()
    date = []
    timetag = []
    navg = []
    x = []
    y = []
    z = []
    Bx = []
    By = []
    Bz = []
    dBx = []
    dBy = []
    dBz = []
    for i in  data.itertuples():
        tmp = pd.Timestamp(year=i[1],month=1,day=1)
        date.append(tmp + pd.Timedelta(days=i[2],hours=i[3],minutes=i[4],seconds=i[5]))
        timetag.append(i[6])
        navg.append(i[7])
        x.append(i[8])
        y.append(i[9])
        z.append(i[10])
        Bx.append(i[11])
        By.append(i[12])
        Bz.append(i[13])
        dBx.append(i[14])
        dBy.append(i[15])
        dBz.append(i[16])
    result['date'] = date
    result['X'] = x
    result['Y'] = y
    result['Z'] = z
    result['Bx'] = Bx
    result['By'] = By
    result['Bz'] = Bz
    result['dBx'] = dBx
    result['dBy'] = dBy
    result['dBz'] = dBz
    result['Timetag'] = timetag
    result['NAVG'] = navg
    result = result.set_index('date')
    return result
    
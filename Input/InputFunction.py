import os

import json
from pathlib import Path
import pandas as pd

# ==== setting file ====
setting_path = Path(__file__).resolve().parent.parent.joinpath("setting.json")
setting = open(setting_path,'r')
setting = json.load(setting)

# ==== get total days ====
def get_totaldays(start,end):
    ds = pd.to_datetime(start)
    de = pd.to_datetime(end)
    days = []
    for i in range((de-ds).days+1):
        date = ds + pd.Timedelta(days=i)
        firstday = pd.Timestamp(year=date.year,month=1,day=1)
        days.append((date.year,(date-firstday).days+1))
    return days

# ==== make directory ====
def make_directory(type):
    # make directory for each type
    dirc = setting[type]["path"] + "/" + setting[type]["name"]
    if not os.path.isdir(dirc):
        os.makedirs(dirc)
    # make directory for original file
    dirc_original = dirc + "/original"
    if not os.path.isdir(dirc_original):
        os.makedirs(dirc_original)
    # make directory for xml file
    dirc_xml = dirc + "/xml"    
    if not os.path.isdir(dirc_xml):
        os.makedirs(dirc_xml)

# ==== download file ====
def download_file():
    pass
import pandas as pd
from MDUS.Setting.setting import setting

orbit = pd.read_pickle(setting["data"]["orbit"])
dip = pd.read_pickle(setting["data"]["dip"])
diptype = pd.read_pickle(setting["data"]["diptype"])
Mercury = pd.read_pickle(setting["data"]["Mercury"])
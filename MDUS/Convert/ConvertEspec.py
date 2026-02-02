import pandas as pd
import numpy as np
import re

import MDUS.Constant.constant as cst
import MDUS.LoadData.LoadFunction as ldf

def especconvert(ofile,pfile,target,years,days):
    # output
    result = {}
    targets = ["H+","He2+","He+", "Na+", "O+"]
    # データ読み込み
    tmp = pd.read_csv(ofile,skiprows=4,header=None,sep='\s+')
    # 日付計算
    mets = tmp[1].values
    dates = ldf.convert_epoch_to_datetime(mets,years,days)

    for i in range(len(targets)):
        indexnum = np.arange(2+i*64,66+i*64)
        temp = tmp[indexnum].copy()
        temp = temp.set_axis(cst.EQTAB[::-1],axis='columns')
        temp['date'] = dates
        temp = temp.set_index('date')
        result[targets[i]] = temp

        pfile = re.match(r"(.*/\d{4}_\d{3}_)", pfile).group(1)
        pfile_temp = pfile + targets[i] + '.pkl'
        # ファイル出力
        temp.to_pickle(pfile_temp)
    return result[target]
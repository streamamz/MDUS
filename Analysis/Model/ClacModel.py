# KT17
import KT17 as kt17
# KTH22
# version 8
from MDUS.Analysis.Model import kth22_model_for_mercury_v8_modificated as kth22

from astroquery.jplhorizons import Horizons
from astropy.time import Time
import numpy as np
import pandas as pd

from MDUS.Data import constant as const
from MDUS.Class import MagDataClass
from MDUS.Class import ScanDataClass

control_param_path = '/home/togawa/main/messenger/module/control_params_v8b.json'
fit_param_path = '/home/togawa/main/messenger/module/kth_own_cf_fit_parameters_opt_total_March23.dat'

def ClacKTH22(self,r_hel=None,DistIndex=50,
              dp=True,ns=True,rc=True,In=True,Ex=True,rename=False):    
    
    if r_hel is None:
        dt = Time(self.value.index[0]).jd1
        r_hel = Horizons(id='199',location='@sun',epochs=dt).vectors()['range'].value[0]
    
    x = self.value['X_MSO'].values.copy()
    y = self.value['Y_MSO'].values.copy()
    z = self.value['Z_MSO'].values.copy()
    
    if self.info["unit"] == "Rm":
        x *= const.Rm
        y *= const.Rm
        z *= const.Rm
    r_hel = np.full(len(x),r_hel)
    DistIndex = np.full(len(x),DistIndex)

    Bx_model, By_model, Bz_model = kth22.kth22_model_for_mercury_v8(x,y,z,r_hel,DistIndex,
                                                                    control_param_path,fit_param_path,
                                                                    dipole=dp,neutralsheet=ns,ringcurrent=rc,
                                                                    internal=In,external=Ex)
    Babs_model = np.sqrt(Bx_model**2 + By_model**2 + Bz_model**2)

    rename_tmp = ''
    if rename:
        if dp:
            rename_tmp += '_dp'
        if ns:
            rename_tmp += '_ns'
        if rc:
            rename_tmp += '_rc'
        if In:
            rename_tmp += '_In'
        if Ex:
            rename_tmp += '_Ex'
    self.value['Bx_KTH22'+rename_tmp] = Bx_model
    self.value['By_KTH22'+rename_tmp] = By_model
    self.value['Bz_KTH22'+rename_tmp] = Bz_model 
    self.value['|B|_KTH22'+rename_tmp] = Babs_model

MagDataClass.MagData.CalcKTH22 = ClacKTH22
ScanDataClass.ScanData.CalcKTH22 = ClacKTH22
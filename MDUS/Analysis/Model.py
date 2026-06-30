import numpy as np
np.sctypeDict["bool8"] = np.bool_
import KT17

def CalcModel(self, model="KT17",
              Rsun=0.4, DI=50, aberrated=False):
    if aberrated:
        coordinates = ["X_aMSM","Y_aMSM","Z_aMSM"]
    else:
        coordinates = ["X_MSM","Y_MSM","Z_MSM"]
    columns = self.value.columns
    if not set(coordinates).issubset(columns):
        raise ValueError("Data does not contain required coordinates. "\
        "you need to use GetPos() and CTransform() before using CalcModel()")
    # DI limits
    if DI < 0:
        print("DI should be non-negative. Setting DI=0")
        DI = 0
    if DI > 97:
        print("DI is too large. Setting DI=97")
        DI = 97
    # Model
    if model == "KT17":
        x_model, y_model, z_model = KT17.ModelField(
            self.value[coordinates[0]].values,
            self.value[coordinates[1]].values,
            self.value[coordinates[2]].values,
            Rsun=Rsun, DistIndex=DI
        )
    if aberrated:
        Bx_name = "Bx_" + model + "_aberrated"
        By_name = "By_" + model + "_aberrated"
        Bz_name = "Bz_" + model + "_aberrated"
        Btot_name = "Btot_" + model + "_aberrated"
    else:
        Bx_name = "Bx_" + model
        By_name = "By_" + model
        Bz_name = "Bz_" + model
        Btot_name = "Btot_" + model
    self.value[Bx_name] = x_model
    self.value[By_name] = y_model
    self.value[Bz_name] = z_model
    self.value[Btot_name] = np.sqrt(
        x_model**2 + y_model**2 + z_model**2
    )

def TraceField(xmsm, ymsm, zmsm, Rsun=0.4, DI=50):
    tmp = KT17.TraceField(xmsm, ymsm, zmsm, Rsun=Rsun, DistIndex=DI)
    return tmp.x, tmp.y, tmp.z
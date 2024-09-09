from MDUS.Class.DataClass import Data
from MDUS.Input import InputMag as ipm
# from MDUS.Plot import PlotMag as plm
from MDUS.Setting.setting import setting

#Dataクラスを継承してMagDataクラスを定義する
class MagData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = 'MAG'
# infoフィールドの中身を表示するInfoメソッドを定義する
# DataクラスのInfoメソッドを継承する
# typeフィールドの中身を表示する
    def Info(self):
        super().Info()
# start,end,secを引数に取るInputメソッドを定義する
# start,endは文字列，secは整数である
# secの既定は1であり，1,5,10,60のいずれでもなければ例外を発生させる
# start, end, secはmaginput関数に渡される
# 返り値は startdate, enddate, ofile, pfile, resultに格納
# それぞれ，Start Date, End Date, Original File, Input Fileとしてinfoフィールドに追加
# End Dateの直後にsecをsecondとしてinfoフィールドに追加

    def Input(self,start=None,end=None,orbit=None,sec=1,Rm=True):
        # startとendがどちらもNone，かつorbitがNoneの場合には例外を発生させる
        if sec not in [1,5,10,60]:
            raise ValueError("Error: sec must be 1, 5, 10, or 60")
        if start is None and end is None and orbit is None:
            raise ValueError("Error: start, end, and orbit cannot be None at the same time")
        startdate,enddate,ofile,pfile,result = ipm.maginput(start,end,orbit,sec,Rm)
        if orbit is not None:
            self.info["Orbit"] = orbit
        self.info["Start Date"] = startdate
        self.info["End Date"] = enddate
        self.info["Original File"] = ofile
        self.info["Input File"] = pfile
        self.info["Second"] = sec
        if Rm:
            self.info["unit"] = "Rm"
        else:
            self.info["unit"] = "km"
        self.value = result      
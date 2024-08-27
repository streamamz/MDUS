from MDUS.Class.DataClass import Data
from MDUS.Input import InputMag as ipm
from MDUS.Plot import PlotMag as plm
from MDUS.Setting.setting import setting

#Dataクラスを継承してMagDataクラスを定義する
class MagData(Data):
    def __init__(self):
        super().__init__()
        self.type = 'MAG'
# infoフィールドの中身を表示するInfoメソッドを定義する
# DataクラスのInfoメソッドを継承する
# typeフィールドの中身を表示する
    def Info(self):
        print("Data Type")
        print("\t" + self.type)
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
        self.value = result      

    def Plot(self,component=['|B|','Bx','By','Bz'],ds=None,de=None,filename=None,fsize=(9,3)):
# componentには'|B|','Bx','By','Bz'以外が指定された場合には例外を発生させる
        if set(component) - set(['|B|','Bx','By','Bz']):
            raise ValueError("Error: component must be '|B|','Bx','By', or 'Bz'")
        colors = []
# componentの数だけ色をcolorsに追加する
# '|B|'は黒，'Bx'は赤，'By'は青，'Bz'は緑に対応するようにする
        for comp in component:
            if comp == '|B|':
                colors.append('black')
            elif comp == 'Bx':
                colors.append('red')
            elif comp == 'By':
                colors.append('blue')
            else:
                colors.append('green')
        fig, ax = plm.plot_mag(self.value,component,colors,ds,de,fsize)
        if filename is not None:
            fig.tight_layout()
            fname = setting["figure"]["path"] + "/" + filename + ".png"
            fig.savefig(fname,dpi=400)
        return fig, ax 
# infoフィールドとvalueフィールドを持つDataクラスを定義する

class Data:
    def __init__(self):
        self.info = {}
        self.value = None
# infoフィールドの中身を表示するInfoメソッドを定義する 
# infoフィールドの中身が空の場合は"No Data"と表示する
# 空でない場合には，keyとvalueを表示する   
# keyとvalueを表示する際にはtabを使って整形する 
# valueを表示する際には，str関数を使って文字列に変換する
    def Info(self):
        if len(self.info) == 0:
            print("No Data")
        else:
            for key in self.info:
# dictのvalueがlistの場合には，各要素を改行して表示する
                if type(self.info[key]) == list:
                    print("\033[31m" + key + "\033[0m")
                    for value in self.info[key]:
                        print("\t" + str(value))
                else:
                    print("\033[31m" + key + "\033[0m")
                    print("\t" + str(self.info[key]))
# valueフィールドの中身を返すValueメソッドを定義する
    def Value(self):
        return self.value


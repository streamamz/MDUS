# ==== parent class for each data type ====
class Data:
    # constructor
    def __init__(self):
        self.value = None
        self.info = {}
    # ==== print info ====
    def Info(self):
        if self.info == {}:
            print('No Information')
        else:
            for key in self.info:
                print(str(key) + '\t:',self.info[key])
    # ==== return data ====
    def Value(self):
        return self.value
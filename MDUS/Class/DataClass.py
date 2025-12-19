import pandas as pd

class Data:
    def __init__(self):
        self.info = {}
        self.value = None
    def Info(self):
        if len(self.info) == 0:
            print("No Data")
        else:
            for key in self.info:
                if key == "Data Type":
                        print("\033[31m" + key + "\033[0m")
                        print("\t" + str(self.info[key]))
                else:
                    if type(self.info[key]) == list:
                        print("\033[34m" + key + "\033[0m")
                        for value in self.info[key]:
                            print("\t" + str(value))
                    else:
                        print("\033[34m" + key + "\033[0m")
                        print("\t" + str(self.info[key]))
    def Value(self,start=None,end=None,inplace=False):
        if start is None or end is None:
            return self.value
        try:
            start = pd.to_datetime(start)
            end = pd.to_datetime(end)
        except ValueError:
            raise ValueError("Error: start and end must be in the format of YYYY-MM-DD HH:MM:SS")
        if start > end:
            start,end = end,start
        if inplace:
            self.value = self.value.query("@start <= index <= @end")
            return self.value
        else:
            return self.value.query("@start <= index <= @end")

import numpy as np
class GetDataLimits:
    dataLimits = {}

    @classmethod
    def getDataLimitsIndexes(cls, axIn, x):
        cls.dataLimits = {}
        if type(x) is not np.ndarray :
            cls.dataLimits["minIndex"] = int(axIn.range[0]/x)
            cls.dataLimits["maxIndex"] = int(axIn.range[1]/x)
        elif type(x) is np.ndarray:
            i = 0
            while i < x.size:
                if x[i] > axIn.range[0]:
                   cls.dataLimits["minIndex"] = i
                   break
                i+=1
            i = len(x)-1
            while i > 0:
                if x[i] < axIn.range[1]:
                   cls.dataLimits["maxIndex"] = i
                   break
                i-=1

        print('axis range: {}'.format(axIn.range))  # <------- get range of x axis
        print('data indexes: {}'.format(cls.dataLimits))  # <------- get range of x axis

        return cls.dataLimits

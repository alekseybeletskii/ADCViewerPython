class GetDataLimits:
    dataLimits = {}

    @classmethod
    def getDataLimitsIndexes(cls, axIn, dx):
        cls.dataLimits = {}
        cls.dataLimits["minIndex"] = int(axIn.range[0]/dx)
        cls.dataLimits["maxIndex"] = int(axIn.range[1]/dx)
        print('axis range: {}'.format(axIn.range))  # <------- get range of x axis
        return cls.dataLimits

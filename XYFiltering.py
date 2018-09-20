from scipy.signal import savgol_filter


class XYFiltering:
    def __init__(self, callingObj):

        self.callingObj = callingObj

    def subtractSGFilter(self):
        for i in range(len(self.callingObj.d)):
            smoothed = self.savitzky_golay_filt(self.callingObj.d[i][self.callingObj.xLeft:self.callingObj.xRight], int(self.callingObj.winLength.text()), int(self.callingObj.polyOrder.text()))
            self.callingObj.d[i][self.callingObj.xLeft:self.callingObj.xRight] = self.callingObj.d[i][self.callingObj.xLeft:self.callingObj.xRight] - smoothed

    def replaceWithSGFilter(self):
        for i in range(len(self.callingObj.d)):
            smoothed = self.savitzky_golay_filt(self.callingObj.d[i][self.callingObj.xLeft:self.callingObj.xRight], int(self.callingObj.winLength.text()), int(self.callingObj.polyOrder.text()))
            self.callingObj.d[i][self.callingObj.xLeft:self.callingObj.xRight] =  smoothed

    def savitzky_golay_filt(self,data, window_length=1001, polyorder=0, deriv=0, delta=1.0, axis=-1, mode='interp'):
        return savgol_filter(data,window_length,polyorder,mode=mode)
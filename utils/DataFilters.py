from scipy.signal import savgol_filter
from scipy.signal import butter, sosfiltfilt

class DataFilters:
    def __init__(self, callingObj):

        self.callingObj = callingObj

    def subtractSGFilter(self):
        for i in range(len(self.callingObj.dataIn)):
            smoothed = self.savitzky_golay_filt(self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight], int(self.callingObj.winLength.text()), int(self.callingObj.polyOrder.text()))
            self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] = self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] - smoothed

    def replaceWithSGFilter(self):
        for i in range(len(self.callingObj.dataIn)):
            smoothed = self.savitzky_golay_filt(self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight], int(self.callingObj.winLength.text()), int(self.callingObj.polyOrder.text()))
            self.callingObj.dataIn[i][self.callingObj.xLeft:self.callingObj.xRight] =  smoothed

    def savitzky_golay_filt(self,data, window_length=1001, polyorder=0, deriv=0, delta=1.0, axis=-1, mode='interp'):
        return savgol_filter(data,window_length,polyorder,mode=mode)


    def butter_bandpass(self, lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            sos = butter(order, [low, high], analog=False, btype='band', output='sos')
            return sos

    def butterworthBandpassZeroPhase(self, data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        filtered = sosfiltfilt(sos, data)
        return filtered
import nnresample
from scipy import signal
import resampy
import  numpy as np
class DataResample:
    def __init__(self, callingObj):
        self.callingObj = callingObj

    def downSample(self,newSampleRateHz):
        for i in range(len(self.callingObj.dataIn)):
            # self.callingObj.dataIn[i] = nnresample.resample( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
            # self.callingObj.dataIn[i] = signal.resample_poly( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
            self.callingObj.dataIn[i] = resampy.resample( self.callingObj.dataIn[i], self.callingObj.frq[i], newSampleRateHz)
            self.callingObj.frq[i] = newSampleRateHz
            self.callingObj.dti[i] = np.double(1.0/newSampleRateHz)

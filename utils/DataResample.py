import nnresample
from scipy import signal
import resampy # resampy uses sinc filter that has linear phase response
# all frequency components of the input signal are shifted in time (usually delayed)
# by the same constant amount (the slope of the linear function)
import  numpy as np
class DataResample:
    def __init__(self, callingObj):
        self.callingObj = callingObj

    def downSampleResampy(self,newSampleRateHz):
        for i in range(len(self.callingObj.dataIn)):
            # self.callingObj.dataIn[i] = nnresample.resample( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
            # self.callingObj.dataIn[i] = signal.resample_poly( self.callingObj.dataIn[i], newSampleRateHz, self.callingObj.frq[i])
            self.callingObj.dataIn[i] = resampy.resample( self.callingObj.dataIn[i], self.callingObj.frq[i], newSampleRateHz)
            self.callingObj.frq[i] = newSampleRateHz
            self.callingObj.dti[i] = np.double(1.0/newSampleRateHz)

    def downSampleDecimate(self,target_frqHz):
        for i in range(len(self.callingObj.dataIn)):
            decimation_ratio = int(np.round(self.callingObj.frq[i]/ target_frqHz))
            self.callingObj.dataIn[i] = signal.decimate( self.callingObj.dataIn[i], decimation_ratio, zero_phase=True)
            self.callingObj.frq[i] = target_frqHz
            self.callingObj.dti[i] = np.double(1.0/target_frqHz)

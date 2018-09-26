from skimage.feature.peak import peak_local_max
import numpy as np
class SpectrogramPeaksDetection:
        def __init__(self, callingObj):
            self.callingObj = callingObj

        def findSpectroPeaks(self):
            allPeaks = peak_local_max(self.callingObj.Sxx,threshold_abs=0.9*np.max(self.callingObj.Sxx))
            peaksX = []
            peaksY = []
            for xIndex in allPeaks[:,1]:
                peaksX.append( self.callingObj.t[xIndex])
            for yIndex in allPeaks[:,0]:
                peaksY.append( self.callingObj.f[yIndex])


            # print('allPeaks:', allPeaks)
            # print('peaksX',allPeaks[:,0])
            # print('peaksY',allPeaks[:,1])
            self.callingObj.spectrPlot.plot(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)

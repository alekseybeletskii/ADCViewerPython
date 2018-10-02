from skimage.feature.peak import peak_local_max
import numpy as np
import pyqtgraph as pg

class SpectrogramPeaksDetection:
        def __init__(self, callingObj):
            self.callingObj = callingObj
            self.peakThreshold = 0

        def findSpectroPeaks(self):
            self.peakThreshold = self.callingObj.peakSlider.sliderScaledValue/self.callingObj.peakSlider.scaledMaximum
            print('peakThreshold = ', self.peakThreshold)
            allPeaks = peak_local_max(self.callingObj.Sxx,threshold_abs=self.peakThreshold*np.max(self.callingObj.Sxx))
            peaksX = []
            peaksY = []
            for xIndex in allPeaks[:,1]:
                peaksX.append( self.callingObj.t[xIndex])
            for yIndex in allPeaks[:,0]:
                peaksY.append( self.callingObj.f[yIndex])

            if self.callingObj:
                # self.callingObj.spectrPlot.plot(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)

                peaksCurve = pg.PlotDataItem(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)
                self.callingObj.spectrPlot.addItem(peaksCurve)

                # self.callingObj.peaksCurve.appendData(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)

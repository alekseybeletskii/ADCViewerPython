from skimage.feature.peak import peak_local_max
import numpy as np
import pyqtgraph as pg
from utils.GetDataLimits import GetDataLimits


class SpectrogramPeaksDetection:
        def __init__(self, callingObj):
            self.callingObj = callingObj
            self.peakThreshold = 0
            self.dataXLimitsIndexes = {}
            self.dataYLimitsIndexes = {}

        def findSpectroPeaks(self):
            axt = self.callingObj.spectrPlot.getAxis('bottom')
            axf = self.callingObj.spectrPlot.getAxis('left')
            dt = abs(np.double(self.callingObj.t[len(self.callingObj.t)-1]-self.callingObj.t[len(self.callingObj.t)-2]))
            self.dataXLimitsIndexes = GetDataLimits.getDataLimitsIndexes(axt, dt)
            df = abs(np.double(self.callingObj.f[len(self.callingObj.f)-1]-self.callingObj.f[len(self.callingObj.f)-2]))
            self.dataYLimitsIndexes = GetDataLimits.getDataLimitsIndexes(axf, df)

            SxxMinXIndex = self.dataXLimitsIndexes.get('minIndex')
            SxxMaxXIndex = self.dataXLimitsIndexes.get('maxIndex')
            SxxMinYIndex = self.dataYLimitsIndexes.get('minIndex')
            SxxMaxYIndex = self.dataYLimitsIndexes.get('maxIndex')
            # print('Sxx X size: ', len(self.callingObj.Sxx[0, :]))
            # print('Sxx Y size: ', len(self.callingObj.Sxx[:, 0]))
            # print('Sxx X range: ',  SxxMinXIndex, SxxMaxXIndex)
            # print('Sxx Y range: ',  SxxMinYIndex, SxxMaxYIndex)

            # self.peakThreshold = self.callingObj.peakSlider.sliderScaledValue/self.callingObj.peakSlider.scaledMaximum
            self.peakThreshold = self.callingObj.peakSlider.sliderScaledValue
            # allPeaks = peak_local_max(self.callingObj.Sxx,threshold_abs = self.peakThreshold*np.max(self.callingObj.Sxx))
            allPeaks = peak_local_max(self.callingObj.Sxx[SxxMinYIndex : SxxMaxYIndex, SxxMinXIndex:SxxMaxXIndex],threshold_abs = self.peakThreshold , min_distance=0)
            peaksX = []
            peaksY = []
            for xIndex in allPeaks[:,1]:
                peaksX.append( self.callingObj.t[xIndex+SxxMinXIndex])
            for yIndex in allPeaks[:,0]:
                peaksY.append( self.callingObj.f[yIndex+SxxMinYIndex])

            if self.callingObj:
                # self.callingObj.spectrPlot.plot(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)

                # peaksCurve = pg.PlotDataItem(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)
                # self.callingObj.spectrPlot.addItem(peaksCurve)

                self.callingObj.spectrPlot.removeItem(self.callingObj.peaksCurve)
                self.callingObj.peaksCurve = pg.PlotDataItem()
                self.callingObj.spectrPlot.addItem(self.callingObj.peaksCurve)
                self.callingObj.peaksCurve.setData(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=3)

            print('peakThreshold = ', self.peakThreshold)
            print('self.dataXLimitsIndexes: ', self.dataXLimitsIndexes)
            print('self.dataYLimitsIndexes: ', self.dataYLimitsIndexes)

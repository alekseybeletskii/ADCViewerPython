import pyqtgraph as pg
import numpy as np
from utils.GetDataLimits import GetDataLimits
from utils.XYFiltering import  XYFiltering
class XYPlotter:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.nextPen = 0
        self.dataXLimitsIndexes = {}

    def drawPlots(self):
        self.callingObj.mainPlotWidget.clear()
        for i in range(len(self.callingObj.dataIn)):
            signal = self.callingObj.dataIn[i]
            # time = np.arange(len(signal))
            # time = self.callingObj.dti[i]
            time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
            dti = self.callingObj.dti[i]
            self.nextPen = self.nextPen + 1
            # self.callingObj.mainPlotWidget.plot(time, signal, pen=None, symbol='t' + str(i + 1), symbolBrush=self.nextPen,
            #                symbolPen=self.nextPen + 3, symbolSize=10 + 3 * i)
            self.callingObj.mainPlotWidget.plot(time,signal, pen=(self.nextPen))

            # self.getXaxisLimits(dti)

            ax = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')

            self.dataXLimitsIndexes = GetDataLimits.getDataLimitsIndexes(ax, dti)

            # if not self.SGFilt.checkState() and not self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
            #     self.plot.plot(time, signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))

            # self.callingObj.xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            # self.callingObj.xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal)

            minXindex  = self.dataXLimitsIndexes.get("minIndex")
            maxXindex  = self.dataXLimitsIndexes.get("maxIndex")
            self.callingObj.xLeft = minXindex if minXindex > 0 else 0
            self.callingObj.xRight = maxXindex if maxXindex < len(signal) else len(signal)

            signal = signal[minXindex:maxXindex]
            time = time[minXindex:maxXindex]
            if self.callingObj.applySGF.checkState():
                xyFilt = XYFiltering(self.callingObj)

                smoothed = xyFilt.savitzky_golay_filt(signal,int(self.callingObj.winLength.text()),int(self.callingObj.polyOrder.text()))
                self.callingObj.mainPlotWidget.plot(time, smoothed, pen=pg.mkPen(color='k'))
            print('samplingRate,Hz: ', np.double(self.callingObj.frq[i]))
            print('size, points: ', np.double(len(signal)))

    # def getXaxisLimits(self, dti):
    #     axX = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')
    #     self.callingObj.xLeft = int(axX.range[0]/dti)
    #     self.callingObj.xRight = int(axX.range[1]/dti)
    #     # axY = self.plot.plotItem.getAxis('left')
    #     print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
    #     # print('y axis range: {}'.format(axY.range))  # <------- get range of y axis
import pyqtgraph as pg
import numpy as np
from utils.XYFiltering import  XYFiltering
class XYPlotter:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.nextPen = 0

    def drawPlots(self):
        self.callingObj.plot.clear()
        for i in range(len(self.callingObj.dataIn)):
            signal = self.callingObj.dataIn[i]
            # time = np.arange(len(signal))
            # time = self.callingObj.dti[i]
            time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
            dti = self.callingObj.dti[i]
            self.nextPen = self.nextPen + 1
            # self.callingObj.plot.plot(time, signal, pen=None, symbol='t' + str(i + 1), symbolBrush=self.nextPen,
            #                symbolPen=self.nextPen + 3, symbolSize=10 + 3 * i)
            self.callingObj.plot.plot(time,signal, pen=(self.nextPen))
            self.getXaxisLimits(dti)
            # if not self.SGFilt.checkState() and not self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
            #     self.plot.plot(time, signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.callingObj.xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            self.callingObj.xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal)
            signal = signal[self.callingObj.xLeft:self.callingObj.xRight]
            time = time[self.callingObj.xLeft:self.callingObj.xRight]
            if self.callingObj.applySGF.checkState():
                xyFilt = XYFiltering(self.callingObj)

                smoothed = xyFilt.savitzky_golay_filt(signal,int(self.callingObj.winLength.text()),int(self.callingObj.polyOrder.text()))
                self.callingObj.plot.plot(time, smoothed, pen=pg.mkPen(color='k'))
            print('samplingRate,Hz: ', np.double(self.callingObj.frq[i]))
            print('size, points: ', np.double(len(signal)))

    def getXaxisLimits(self, dti):
        axX = self.callingObj.plot.plotItem.getAxis('bottom')
        self.callingObj.xLeft = int(axX.range[0]/dti)
        self.callingObj.xRight = int(axX.range[1]/dti)
        # axY = self.plot.plotItem.getAxis('left')
        print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
        # print('y axis range: {}'.format(axY.range))  # <------- get range of y axis
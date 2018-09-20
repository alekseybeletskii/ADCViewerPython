import pyqtgraph as pg
import numpy as np
from XYFiltering import  XYFiltering
class XYPlotter:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.nextPen = 0

    def drawPlots(self):
        self.callingObj.plot.clear()
        for i in range(len(self.callingObj.d)):
            signal = self.callingObj.d[i]
            time = np.arange(len(signal))
            # time = self.callingObj.t[i]
            self.nextPen = self.nextPen + 1
            self.callingObj.plot.plot(time,signal, pen=(self.nextPen))
            self.getXaxisLimits()
            # if not self.SGFilt.checkState() and not self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
            #     self.plot.plot(time, signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))
            self.callingObj.xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            self.callingObj.xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1
            signal = signal[self.callingObj.xLeft:self.callingObj.xRight]
            time = time[self.callingObj.xLeft:self.callingObj.xRight]
            if self.callingObj.applySGF.checkState():
                xyFilt = XYFiltering(self.callingObj)

                smoothed = xyFilt.savitzky_golay_filt(signal,int(self.callingObj.winLength.text()),int(self.callingObj.polyOrder.text()))
                self.callingObj.plot.plot(time, smoothed, pen=pg.mkPen(color='k'))

    def getXaxisLimits(self):
        axX = self.callingObj.plot.plotItem.getAxis('bottom')
        self.callingObj.xLeft = int(axX.range[0])
        self.callingObj.xRight = int(axX.range[1])
        # axY = self.plot.plotItem.getAxis('left')
        print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
        # print('y axis range: {}'.format(axY.range))  # <------- get range of y axis
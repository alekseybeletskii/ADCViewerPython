# /*
#  * ******************** BEGIN LICENSE BLOCK *********************************
#  *
#  * w7x-PyViewer
#  * Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
#  * All rights reserved
#  *
#  * github: https://github.com/alekseybeletskii
#  *
#  * The w7x-PyViewer software serves for visualization and simple processing
#  * of any data recorded with Analog Digital Converters in binary or text form.
#  *
#  * Commercial support is available. To find out more contact the author directly.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions are met:
#  *
#  *     1. Redistributions of source code must retain the above copyright notice, this
#  *          list of conditions and the following disclaimer.
#  *     2. Redistributions in binary form must reproduce the above copyright notice,
#  *         this list of conditions and the following disclaimer in the documentation
#  *         and/or other materials provided with the distribution.
#  *
#  * The software is distributed to You under terms of the GNU General Public
#  * License. This means it is "free software". However, any program, using
#  * w7x-PyViewer _MUST_ be the "free software" as well.
#  * See the GNU General Public License for more details
#  * (file ./COPYING in the root of the distribution
#  * or website <http://www.gnu.org/licenses/>)
#  *
#  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  *
#  * ******************** END LICENSE BLOCK ***********************************
#  */
#


import pyqtgraph as pg
import numpy as np
from utils.GetDataLimits import GetDataLimits
from utils.DataFilters import  DataFilters





class XYPlotter:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.nextPen = 0
        self.dataXLimitsIndexes = {}


        # self.callingObj.mainPlotWidget.addLegend( )

        self.legend = pg.LegendItem()  # args are (size, offset)
        # self.legend.setParentItem(self.callingObj.mainPlotWidget.graphicsItem())  # Note we do NOT call plt.addItem in this case
        self.allPlotItems = []
        # self.legend = pg.LegendItem()

    def drawPlots(self):
        # self.callingObj.mainPlotWidget.clear()
        self.clearPlots()
        # Add labels to the axis
        self.callingObj.mainPlotWidget.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        self.callingObj.mainPlotWidget.setLabel('left', "Amplitude", units='a.u.')



        for i in range(len(self.callingObj.dataIn)):

            signal = self.callingObj.dataIn[i]
            dti = self.callingObj.dti[i]
            # time = np.arange(len(signal))
            # time = self.callingObj.dti[i]
            # time = np.arange(0, (len(signal)) * dti, dti) if len(self.callingObj.dti[i])==1 else dti
            time = np.arange(0, (signal.size) * dti, dti)+self.callingObj.dataInADCChannelTimeShift[i] if self.callingObj.dti[i].size==1 else dti

            self.nextPen = self.nextPen + 2

            # self.callingObj.mainPlotWidget.plot(time, signal, pen=None, symbol='t' + str(i + 1), symbolBrush=self.nextPen,
            #                symbolPen=self.nextPen + 3, symbolSize=10 + 3 * i)
            plt = self.callingObj.mainPlotWidget.plot(time,signal, pen=(self.nextPen),  name='    '+self.callingObj.dataInLabels[i])
            self.allPlotItems.append(plt)

            ax = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')

            self.dataXLimitsIndexes = GetDataLimits.getDataLimitsIndexes(ax, dti)

            # if not self.SGFilt.checkState() and not self.subtrFilt.checkState() and not self.replaceWithSGFilt.checkState():
            #     self.plot.plot(time, signal, pen=(self.nextPen))
            # self.plot.plot(time[0:len(signal)],signal, pen=(self.nextPen))

            # self.callingObj.xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
            # self.callingObj.xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal)

            minXindex  = self.dataXLimitsIndexes.get("minIndex")
            maxXindex  = self.dataXLimitsIndexes.get("maxIndex")
            minXindex = self.callingObj.xLeft = minXindex if minXindex > 0 else 0
            maxXindex = self.callingObj.xRight = maxXindex if maxXindex < len(signal) else len(signal)

            signal = signal[minXindex:maxXindex]
            time = time[minXindex:maxXindex]
            if self.callingObj.applySGF.checkState():
                dataFilters = DataFilters(self.callingObj)

                smoothed = dataFilters.savitzky_golay_filt(signal,self.callingObj.settings["sgFilterWindow"],self.callingObj.settings["sgFilterPolyOrder"])
                self.callingObj.mainPlotWidget.plot(time, smoothed, pen=pg.mkPen(color='k'))
            print('samplingRate,Hz: ', np.double(self.callingObj.frq[i]))
            print('size, points: ', np.double(len(signal)))

        # self.createPyqtgraphLegend()


    def clearPlots(self):
        self.allPlotItems.clear()
        self.nextPen = 0
        self.clearPyqtgraphLegend()


    def clearAllPlotsAndData(self):
        self.callingObj.mainPlotWidget.clear()
        for itm in self.allPlotItems:
            self.callingObj.mainPlotWidget.removeItem(itm)
        self.allPlotItems.clear()
        self.clearPyqtgraphLegend()


    def clearPyqtgraphLegend(self):
        for itm in self.allPlotItems:
            self.legend.removeItem(itm)
        if self.legend.scene() is not None:
            self.legend.scene().removeItem(self.legend)




    # def getXaxisLimits(self, dti):
    #     axX = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')
    #     self.callingObj.xLeft = int(axX.range[0]/dti)
    #     self.callingObj.xRight = int(axX.range[1]/dti)
    #     # axY = self.plot.plotItem.getAxis('left')
    #     #print('x axis range: {}'.format(axX.range))  # <------- get range of x axis
    #     # #print('y axis range: {}'.format(axY.range))  # <------- get range of y axis

    # x =  np.linspace(0.01,0.05,10)
    # y =  np.linspace(100000,200000,10)
    # self.spectrPlot.plot(x, y, pen=pg.mkPen(color=(255,0,0), width=5), name="Red curve", symbol='o' , symbolBrush = "k", symbolPen = "k", symbolSize=18)
    def createPyqtgraphLegend(self):
        self.legend = pg.LegendItem((200, 50), offset=(70, 30))  # args are (size, offset)
        self.legend.setParentItem(self.callingObj.mainPlotWidget.graphicsItem())  # Note we do NOT call plt.addItem in this case

        for i in range(len(self.allPlotItems)):
            self.legend.addItem(self.allPlotItems[i], self.callingObj.dataInLabels[i])




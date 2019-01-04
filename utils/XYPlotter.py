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
from utils.DataLimits import DataLimits
from utils.DataFilters import DataFilters
from utils.ColorPalette import ColorPalette
from PyQt5.QtGui import QColor
from PyQt5.Qt import Qt





class XYPlotter:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.dataXLimitsIndexes = {}
        self.allSmoothedPlotItems = []
        self.colors = ColorPalette.getColorPalette()

    def setCurveColor(self, index, color=QColor(Qt.black)):
        self.callingObj.allData[index].getPlotDataItem().setPen(color.name())
        iColor = index % len(self.colors)
        self.colors[iColor] = color.name()

    def setCurveVisibility(self, index, isVisible=True):
        if isVisible:
            self.callingObj.mainPlotWidget.addItem(self.callingObj.allData[index].getPlotDataItem())
            # self.callingObj.allData[index].getPlotDataItem().curve.show()
            self.callingObj.allData[index].getPlotDataItem().setVisible(True)

        else:
            self.callingObj.mainPlotWidget.removeItem(self.callingObj.allData[index].getPlotDataItem())
            # self.callingObj.allData[index].getPlotDataItem().curve.hide()
            self.callingObj.allData[index].getPlotDataItem().setVisible(False)


        # print('item status: ', index,' : ', self.callingObj.allData[index].getPlotDataItem().isVisible())


    def drawPlots(self):

        # self.callingObj.mainPlotWidget.clear()
        self.clearPlots()
        # Add labels to the axis
        self.callingObj.mainPlotWidget.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        self.callingObj.mainPlotWidget.setLabel('left', "Amplitude", units='a.u.')


        nextColor = 0
        for i in range(len(self.callingObj.allData)):

            # nextPen = pg.mkPen(colors[i], width=3, style=QtCore.Qt.DashLine)

            # self.callingObj.mainPlotWidget.plot(time, signal, pen=None, symbol='t' + str(i + 1), symbolBrush=self.nextPen,
            #                symbolPen=self.nextPen + 3, symbolSize=10 + 3 * i)

            self.callingObj.allData[i].getPlotDataItem().setPen(self.colors[nextColor])
            self.callingObj.allData[i].getPlotDataItem().setVisible(True)
            self.callingObj.mainPlotWidget.addItem(self.callingObj.allData[i].getPlotDataItem())

            # print(self.callingObj.allData[i].getPlotDataItem().name())

            if self.callingObj.applySGF.checkState():
                time, signal = self.callingObj.allData[i].getPlotDataItem().getData()
                dti = self.callingObj.allData[i].getDt()
                axis = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')
                self.dataXLimitsIndexes = DataLimits.getDataLimitsIndexes(axis, dti, len(signal))
                minXindex = self.dataXLimitsIndexes.get("minIndex")
                maxXindex = self.dataXLimitsIndexes.get("maxIndex")

                signal = signal[minXindex:maxXindex]
                time = time[minXindex:maxXindex]

                dataFilters = DataFilters(self.callingObj)
                smoothed = dataFilters.savitzky_golay_filt(signal,self.callingObj.settings["sgFilterWindow"],self.callingObj.settings["sgFilterPolyOrder"])
                plt = self.callingObj.mainPlotWidget.plot(time, smoothed, pen=pg.mkPen(color='k'))
                self.allSmoothedPlotItems.append(plt)
            # print('samplingRate,Hz: ', np.double(self.callingObj.frq[i]))
            # print('size, points: ', np.double(len(signal)))

            nextColor = nextColor + 1 if nextColor < len(self.colors) - 1 else 0

        # self.callingObj.allData[0].setTimeShift(0.03)
        # x,y = self.allPlotItems[0].getData()
        # print(x)
        # print(y)




    def clearPlots(self):
        for itm in self.callingObj.allData:
            self.callingObj.mainPlotWidget.removeItem(itm.getPlotDataItem())
        for itm in self.allSmoothedPlotItems:
            self.callingObj.mainPlotWidget.removeItem(itm)
        self.allSmoothedPlotItems.clear()



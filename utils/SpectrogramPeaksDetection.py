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


from skimage.feature.peak import peak_local_max
import numpy as np
import pyqtgraph as pg
from  importExport.ExportToTxtImg import ExportToTxtImg
from utils.DataLimits import DataLimits


class SpectrogramPeaksDetection:
        def __init__(self, callingObj):
            self.callingObj = callingObj
            self.peakThreshold = 0
            # self.dataXLimitsIndexes = {}
            # self.dataYLimitsIndexes = {}
            self.peaksX = []
            self.peaksY = []

            # self.zoomedSxxMaxMin = {}


            self.callingObj.peakSlider.appendPeaks_btn.clicked.connect(self.appendPeaksToList)
            self.callingObj.peakSlider.removePeaks_btn.clicked.connect(self.removePeaks)
            self.callingObj.peakSlider.drawAllPeaks_btn.clicked.connect(self.drawAllPeaks)
            self.callingObj.peakSlider.saveAllPeaks_btn.clicked.connect(self.saveAllPeaksToFile)

        def saveAllPeaksToFile(self):
            exportToFile = ExportToTxtImg(self.callingObj)
            exportToFile.savePlotTofile(self.callingObj.allPeaksXPoints, self.callingObj.allPeaksYPoints)
        def appendPeaksToList(self):
            self.callingObj.allPeaksXPoints.extend(self.peaksX)
            self.callingObj.allPeaksYPoints.extend(self.peaksY)
            self.drawPeaks([], [], "k")
        def removePeaks(self):
            self.callingObj.allPeaksXPoints.clear()
            self.callingObj.allPeaksYPoints.clear()
            self.peaksX.clear()
            self.peaksY.clear()
            self.drawPeaks([], [], "k")
        def drawAllPeaks(self):
            self.drawPeaks(self.callingObj.allPeaksXPoints, self.callingObj.allPeaksYPoints, "k")



        def findSpectroPeaks(self):


            # SxxMinXIndex = self.dataXLimitsIndexes.get('minIndex')
            # SxxMaxXIndex = self.dataXLimitsIndexes.get('maxIndex')
            # SxxMinYIndex = self.dataYLimitsIndexes.get('minIndex')
            # SxxMaxYIndex = self.dataYLimitsIndexes.get('maxIndex')
            # #print('Sxx X size: ', len(self.callingObj.Sxx[0, :]))
            # #print('Sxx Y size: ', len(self.callingObj.Sxx[:, 0]))
            # #print('Sxx X range: ',  SxxMinXIndex, SxxMaxXIndex)
            # #print('Sxx Y range: ',  SxxMinYIndex, SxxMaxYIndex)

            # SxxZoomed = self.callingObj.Sxx[SxxMinYIndex : SxxMaxYIndex, SxxMinXIndex:SxxMaxXIndex]

            # self.peakThreshold = self.callingObj.peakSlider.sliderScaledValue/self.callingObj.peakSlider.scaledMaximum
            self.peakThreshold = self.callingObj.peakSlider.sliderScaledValue
            # allPeaks = peak_local_max(self.callingObj.Sxx,threshold_abs = self.peakThreshold*np.max(self.callingObj.Sxx))
            allPeaks = peak_local_max(self.callingObj.Sxx[self.callingObj.fLimitsIndexes.get('minIndex') : self.callingObj.fLimitsIndexes.get('maxIndex'), self.callingObj.tLimitsIndexes.get('minIndex'):self.callingObj.tLimitsIndexes.get('maxIndex')],threshold_abs = self.peakThreshold , min_distance=0)
            self.peaksX = []
            self.peaksY = []
            for xIndex in allPeaks[:,1]:
                self.peaksX.append( self.callingObj.t[xIndex+self.callingObj.tLimitsIndexes.get('minIndex')])
            for yIndex in allPeaks[:,0]:
                self.peaksY.append( self.callingObj.f[yIndex+self.callingObj.fLimitsIndexes.get('minIndex')])

            self.drawPeaks(self.peaksX, self.peaksY, "r")

            #print('peakThreshold = ', self.peakThreshold)
            #print('self.dataXLimitsIndexes: ', self.dataXLimitsIndexes)
            #print('self.dataYLimitsIndexes: ', self.dataYLimitsIndexes)

        # def findSpectroLimits(self):
        #     axt = self.callingObj.spectrPlot.getAxis('bottom')
        #     axf = self.callingObj.spectrPlot.getAxis('left')
        #     dt = abs(np.double(
        #         self.callingObj.t[len(self.callingObj.t) - 1] - self.callingObj.t[len(self.callingObj.t) - 2]))
        #     self.dataXLimitsIndexes = GetDataLimits.getDataLimitsIndexes(axt, dt)
        #     df = abs(np.double(
        #         self.callingObj.f[len(self.callingObj.f) - 1] - self.callingObj.f[len(self.callingObj.f) - 2]))
        #     self.dataYLimitsIndexes = GetDataLimits.getDataLimitsIndexes(axf, df)
        #
        #     self.zoomedSxxMaxMin['max'] = np.max(self.callingObj.Sxx[self.dataYLimitsIndexes.get('minIndex') : self.dataYLimitsIndexes.get('maxIndex'), self.dataXLimitsIndexes.get('minIndex'):self.dataXLimitsIndexes.get('maxIndex')])
        #     self.zoomedSxxMaxMin['min'] = np.min(self.callingObj.Sxx[self.dataYLimitsIndexes.get('minIndex') : self.dataYLimitsIndexes.get('maxIndex'), self.dataXLimitsIndexes.get('minIndex'):self.dataXLimitsIndexes.get('maxIndex')])



        # def findSliderRange(self):
        #
        #     self.callingObj.peakSlider.setSliderMaxMin(self.zoomedSxxMaxMin['max'], self.zoomedSxxMaxMin['min'])


        def drawPeaks(self, x, y, pen):
            if self.callingObj:
                # self.callingObj.spectrPlot.plot(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)

                # peaksCurve = pg.PlotDataItem(peaksX, peaksY, pen=None, name="Red curve", symbol='o' , symbolBrush = "r", symbolPen = "r", symbolSize=9)
                # self.callingObj.spectrPlot.addItem(peaksCurve)
                self.callingObj.spectrPlot.removeItem(self.callingObj.peaksCurve)
                self.callingObj.peaksCurve = pg.PlotDataItem()
                self.callingObj.spectrPlot.addItem(self.callingObj.peaksCurve)
                # custom pen : pen=pg.mkPen(color=(255,0,0), width=5)
                self.callingObj.peaksCurve.setData(x, y,
                                                   pen=None, name="allPeaks", symbol='o', symbolBrush=pen,
                                                   symbolPen=pen, symbolSize=2)

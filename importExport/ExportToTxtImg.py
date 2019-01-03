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


from os import path, makedirs
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from datetime import datetime
from utils.DataLimits import DataLimits


from PyQt5.QtGui import QScreen


class ExportToTxtImg:
    def __init__(self, callingObj):

        self.callingObj = callingObj
        self.here = path.dirname(path.realpath(__file__))
        self.exportDirName = "exported"
        self.exportDirPath = path.join(self.here, '..', self.exportDirName)
        if not path.exists(self.exportDirPath):
            makedirs(self.exportDirPath)

    def export_to_csv(self, var):

        for i in range(len(self.callingObj.allData)):
            # filename = str(i) + ".csv"
            filename = self.callingObj.allData[i].getPlotDataItem().name() + ".csv"
            filepath = path.join(self.exportDirPath, filename.replace(":", "-"))

            time, signal = self.callingObj.allData[i].getPlotDataItem().getData()
            dti = self.callingObj.allData[i].getDt()
            axis = self.callingObj.mainPlotWidget.plotItem.getAxis('bottom')
            self.dataXLimitsIndexes = DataLimits.getDataLimitsIndexes(axis, dti, len(signal))
            minXindex = self.dataXLimitsIndexes.get("minIndex")
            maxXindex = self.dataXLimitsIndexes.get("maxIndex")

            signal = signal[minXindex:maxXindex]
            time = time[minXindex:maxXindex]

            if var == 'v1':
                np.savetxt(filepath, np.array([time, signal]).T, delimiter=', ')
            elif var == 'v2':
                np.savetxt(filepath + "_time_" + ".csv", time)
                np.savetxt(filepath + "_data_" + ".csv", signal)

        #print('data exported to csv files')

    # def export_to_csv_v2(self):
    #
    #     for i in range(len(self.callingObj.dataIn)):
    #         filename = self.callingObj.dataInLabels[i]
    #         filepath = path.join(self.exportDirPath, filename.replace(":", "-"))
    #
    #         signal = self.callingObj.dataIn[i]
    #         # time = self.callingObj.dti[i]
    #         # time = np.arange(0, (len(signal)) * self.callingObj.dti[i], self.callingObj.dti[i])
    #         dti = self.callingObj.dti[i]
    #         time = np.arange(0, (signal.size) * dti, dti) if self.callingObj.dti[i].size==1 else dti
    #         xLeft = self.callingObj.xLeft if self.callingObj.xLeft > 0 else 0
    #
    #         xRight = self.callingObj.xRight if self.callingObj.xRight < len(signal) else len(signal) - 1
    #
    #         np.savetxt(filepath + "_time_" + ".csv", time[xLeft:xRight])
    #         np.savetxt(filepath + "_data_" + ".csv", signal[xLeft:xRight])
    #
    #         # df = pd.DataFrame(np.array([time[xLeft:xRight], signal[xLeft:xRight]]).T,index=None, columns=None)
    #         # df.to_csv(filename, header=None, index=None)
    #
    #     #print('data exported to csv files, time separated')


    def savePlotTofile(self, x, y):

        filename = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S') + ".peaks"
        filepath = path.join(self.exportDirPath, filename.replace(":","-"))
        # peaksX = self.callingObj.allPeaksXPoints
        # peaksY = self.callingObj.allPeaksYPoints

        xy = np.array([x, y]).T
        # xy.sort(axis=0)
        # xy[np.argsort(xy[:, 0])]


        xy = xy[xy[:, 0].argsort()]

        # np.savetxt(filepath, np.array([x, y]).T, delimiter=', ')
        np.savetxt(filepath, xy, delimiter=', ')

        # pg.plot(np.arange(len(y)),y)
        # pg.plot(xy[:,0],xy[:,1],pen='r',  symbol='o' )



        #print('data exported to utcnow.peaks file')

    def exportWidgetToImg(self, widget, imgTitle):

        # exporter = pg.exporters.ImageExporter(widget.scene())
        # exporter.export(filepath)
        # exporter.parameters()['width'] = widget.scene().sceneRect().width()
#!!!!!!!!!!!
        # for some reason, pyqtgraph.exporters.ImageExporter deteriorates spectrogram resolution during export
        # both in exported file and in the exported widget
#!!!!!!!!!!!

        # filename = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f') + ".jpg"
        filename = imgTitle + ".png"
        filepath = path.join(self.exportDirPath, filename.replace(":","-"))
        p = widget.grab()
        p.save(filepath, 'jpg')


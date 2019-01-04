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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# convert firstgui.ui to Python code:
# pyuic5 -x name.ui -o name.py



from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import Qt

from GUIs import w7xPyViewerLayout
# it also keeps events etc that we defined in Qt Design
import sys
import numpy as np
import pyqtgraph as pg
from importExport.ImportFromTxt import ImportFromTxt
from importExport.ImportFromMdsplus import ImportFromMdsplus
from importExport.ImportFromLGraph import ImportFromLGraph
from utils.XYPlotter import XYPlotter
from importExport.ExportToTxtImg import ExportToTxtImg
from utils.DataFilters import DataFilters
from utils.DataResample import DataResample
from W7XSpectrogram import W7XSpectrogram
from utils.w7xPyViewerSettings import w7xPyViewerSettings
from GUIs.LegendItem import LegendItem
from os import path as ospath
from utils.DataLimits import DataLimits



# from PyQt5.QtGui import QColor




class W7XPyViewer(QtWidgets.QMainWindow, w7xPyViewerLayout.Ui_w7xPyViewer):

    def __init__(self):

        super(self.__class__, self).__init__()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('leftButtonPan', False)

        self.allData = []

        self.latestFilePath = ospath.expanduser('~')
        # self.files = []
        # self.dataIn = []
        # self.dataInADCChannel = []
        # self.dataInADCChannelTimeShift = []
        # self.dti = []
        # self.frq = []
        # self.dataInLabels = []
        # self.nextPen = 0
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        # self.actionOpen_csv_dx.triggered.connect(self.openCsv_dx)
        # self.actionOpen_csv_dx.triggered.connect(lambda: self.openDataSource(self.actionOpen_csv_dx))
        # self.actionOpen_csv_fullX.triggered.connect(self.openCsv_fullX)
        self.actionOpen_csv.triggered.connect(lambda: self.openDataSource(self.actionOpen_csv))
        # self.actionOpen_mdsplus.triggered.connect(self.openMdsplus)
        self.actionOpen_mdsplus.triggered.connect(lambda: self.openDataSource(self.actionOpen_mdsplus))
        # self.actionOpen_LGraph.triggered.connect(self.openLGraph)
        self.actionOpen_LGraph.triggered.connect(lambda: self.openDataSource(self.actionOpen_LGraph))
        self.actionDrawPlots.triggered.connect(self.drawPlots)

        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v1)
        self.actionExport_time_to_separate_file.triggered.connect(self.export_to_csv_v2)

        self.actionClear.triggered.connect(self.clearAllViewer)
        self.actionExit.triggered.connect(self.exitApp)
        # self.xLeft=0
        # self.xRight=0
        self.drawSpectrogramUI.clicked.connect(self.drawSpectrogram)
        self.settings_btn.clicked.connect(self.settingsUi)
        self.applySGF.clicked.connect(self.drawPlots)
        self.replaceWithSGF.clicked.connect(self.replaceWithSGFilter)
        self.subtractSGF.clicked.connect(self.subtractSGFilter)

        self.w7xPyViewerSettingsWidget = w7xPyViewerSettings(self, self)
        self.settings = {}
        self.w7xPyViewerSettingsWidget.setDefaultSettings()

        self.hotkey = {}

        self.ui_hotkey('ajustSettings', "Shift+s", self.settingsUi)

        # self.resampler = DataResample(self)

        # self.allPlotItems = []
        self.xyPlotter = XYPlotter(self)

        self.proxy = pg.SignalProxy(self.mainPlotWidget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.listOfDataLablesWidget.setStyleSheet("QListWidget { background: transparent }")

        # self.listOfDataLablesWidget.itemEntered.connect(
        #     lambda item:
        #     item.setCheckState(Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked)
        #
        # )
        # self.listOfDataLablesWidget.itemEntered.connect(self.showHidePlot )

        # self.listOfDataLablesWidget.itemClicked.connect(lambda item:
        # item.setCheckState(Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked))

        # self.listOfDataLablesWidget.itemClicked.connect(self.showHidePlot )
        # self.listOfDataLablesWidget.itemClicked.connect(lambda item:
        # item.setBackground(QtWidgets.QColorDialog.getColor()))

        # self.listOfDataLablesWidget.currentItemChanged.connect(self.showHidePlot)

    # def showHideColorPlot(self):

    def openDataSource(self, buttonPressed):
        switcher = {
            'Open_mdsplus': self.openMdsplus,
            'Open_csv': self.openCsv,
            'Open_LGraph': self.openLGraph,

        }

        f = switcher.get(buttonPressed.text(), 'unknown')
        f()

        self.populateListOfDataLables()

        self.drawPlots()



    def testing(self):
        # print ( self.listOfDataLablesWidget.currentItem().text())
        # print ( self.listOfDataLablesWidget.currentItem().checkState())
         # print ( self.listOfDataLablesWidget.currentItem().setBackground(QtWidgets.QColorDialog.getColor()))
        # print ( self.listOfDataLablesWidget.currentRow())
        QtWidgets.QColorDialog.getColor()



    def mouseMoved(self, evt):
        mousePoint = self.mainPlotWidget.plotItem.vb.mapSceneToView(evt[0])
        self.mouseXY_UI.setText(
            "<span style='font-size: 12pt; color: green'> x = %0.6f, <span style='color: green'> y = %0.6f</span>" % (
                mousePoint.x(), mousePoint.y()))


    def settingsUi(self):
        self.w7xPyViewerSettingsWidget.show()

    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)

    # def resampleDataResampy(self):
    #     resampler = DataResample(self)
    #     newSampleRateHz = int(np.double(self.NewSamplingRate_kHz.text())*1000) if np.double(self.NewSamplingRate_kHz.text())>0.01 else 1000000
    #     resampler.downSampleResampy(newSampleRateHz)

    # def resampleDataDecimation(self, dataToResample, frq_Hz, target_frq_Hz):
    #         d = self.resampler.downSampleDecimate(dataToResample, frq_Hz, target_frq_Hz)
    #         dt = np.double(1.0/target_frq_Hz)
    #         return d, dt




    def drawSpectrogram(self):
        w7xSpectr = W7XSpectrogram(self)
        w7xSpectr.show()
        for i in range(len(self.allData)):
            _, signal = self.allData[i].getPlotDataItem().getData()
            dti = self.allData[i].getDt()
            axis = self.mainPlotWidget.plotItem.getAxis('bottom')
            self.dataXLimitsIndexes = DataLimits.getDataLimitsIndexes(axis, dti, len(signal))
            minXindex = self.dataXLimitsIndexes.get("minIndex")
            maxXindex = self.dataXLimitsIndexes.get("maxIndex")
            w7xSpectr.setDataToSpectrogram(self.allData[i].getPlotDataItem().name(), signal[minXindex:maxXindex],
                                           int(round(np.power(dti, -1))))
            w7xSpectr.drawSpectrogram()
            # w7xSpectr.close()
        # self.clearAllViewer()

    def clearAllViewer(self):
        self.xyPlotter.clearAllPlotsAndData()
        self.mainPlotWidget.plotItem.enableAutoRange()
        # self.files.clear()
        # self.dataIn.clear()
        # self.dti.clear()
        # self.frq.clear()
        # self.nextPen = 0
        # self.dataInLabels.clear()
        # self.xLeft=0
        # self.xRight=0

    # def openCsv_dx(self):
    #     CsvTxtR = ImportFromTxt(self)
    #     CsvTxtR.openCsvTxt_dx()

    def openLGraph(self):
        self.clearAllViewer()
        LGraphR = ImportFromLGraph(self)
        self.allData = LGraphR.openLGraph()

    def openCsv(self):
        self.clearAllViewer()
        CsvTxtR = ImportFromTxt(self)
        self.allData = CsvTxtR.openCsvTxt()

    # def openMdsplusQXT(self):
    #     self.openMdsplus('qxt1', 'importExport/QXTchList.txt')
    # def openMdsplusQOC(self):
    #     self.openMdsplus('qoc','importExport/QOCchList.txt')

    def openMdsplus(self):
        self.clearAllViewer()
        mdsPlusR = ImportFromMdsplus(self)
        self.allData = mdsPlusR.openMdsPlus()

        # start = self.settings["startMdsplusTime"]
        # end = self.settings["endMdsplusTime"]
        # resample = self.settings["deltaMdsplusTime"]
        # shotNumber = self.settings["shotNum"]
        # treeName  =  self.settings["treeName"]

        # self.dataInLabels = openMds.readCurveDataLabels()

        # for i in range(len(self.dataInLabels)):
        #     d, dt = openMds.getMdsplusData( self.dataInLabels[i], treeName, shotNumber, start, end, resample)
        #
        #     if self.settings["applyDownsampling"]:
        #         d, dt = self.resampleDataDecimation(d, 1.0/dt, self.settings["targetFrq_kHz"]*1000)
        #
        #     self.dataIn.append(d)
        #     self.dti.append(dt)
        #     self.frq.append(int(round(np.power(dt, -1))))
        #
        #     self.dataInADCChannel.append(int(0))
        #     self.dataInADCChannelTimeShift.append(np.double(0))


    def export_to_csv_v1(self):
        toTxt = ExportToTxtImg(self)
        toTxt.export_to_csv('v1')

    def export_to_csv_v2(self):
        toTxt = ExportToTxtImg(self)
        toTxt.export_to_csv('v2')


    def drawPlots(self):
        self.xyPlotter.drawPlots()

    def populateListOfDataLables(self):

        self.listOfDataLablesWidget.clear()
        # self.listOfDataLablesWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        colors = self.xyPlotter.colors
        nextColor = 0

        for i in range(len(self.allData)):
            legendItem = LegendItem(self.xyPlotter, i, True, self.allData[i].getPlotDataItem().name(),
                                    colors[nextColor])
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(legendItem.sizeHint())
            item.setFlags(Qt.NoItemFlags)
            self.listOfDataLablesWidget.addItem(item)
            self.listOfDataLablesWidget.setItemWidget(item, legendItem)
            nextColor = nextColor + 1 if nextColor < len(colors) - 1 else 0
    # def populateListOfDataLables(self):
    #     for lb in self.dataInLabels:
    #         item = QtWidgets.QListWidgetItem(lb, self.listOfDataLablesWidget)
    #         item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
    #         item.setCheckState(Qt.Unchecked)

    def getAllCheckedItemsIndices(self):
        checked_items = []
        for index in range(self.listOfDataLablesWidget.count()):
            if self.listWidgetLabels.item(index).checkState() == Qt.Checked:
                checked_items.append(self.listWidgetLabels.item(index))



    def subtractSGFilter(self):

        xyFilt = DataFilters(self)
        xyFilt.subtractSGFilter()
        # self.drawPlots()

    def replaceWithSGFilter(self):
        xyFilt = DataFilters(self)
        xyFilt.replaceWithSGFilter()
        # self.drawPlots()

    def exitApp(self):
            sys.exit()
            # self.close()

    def closeEvent(self, event):
        event.accept()
        sys.exit()
        # close = QtWidgets.QMessageBox()
        # close.setWindowTitle('closing...')
        # close.setText("Sure?!")
        # close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        # close = close.exec()
        #
        # if close == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        #     if __name__ == '__main__':
        #         sys.exit()
        # else:
        #     event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = W7XPyViewer()
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

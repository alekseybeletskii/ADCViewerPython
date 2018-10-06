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
#  * ADCDataViewer _MUST_ be the "free software" as well.
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


from PyQt5 import QtWidgets

from GUIs import mainLayout
# it also keeps events etc that we defined in Qt Design
import sys
import numpy as np
import pyqtgraph as pg
from importExport.ImportFromTxt import ImportFromTxt
from importExport.ImportFromMdsplus import ImportFromMdsplus
from utils.XYPlotter import XYPlotter
from importExport.ExportToTxt import ExportToTxt
from utils.XYFiltering import XYFiltering
from utils.DataResample import DataResample
from w7xSpectrogram import w7xSpectrogram


class mainApp(QtWidgets.QMainWindow, mainLayout.Ui_MainWindow):

    def __init__(self):

        super(self.__class__, self).__init__()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('leftButtonPan', False)
        self.files = []
        self.dataIn = []
        self.dti = []
        self.frq = []
        self.channelsList = []
        self.nextPen = 0
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.actionOpen_csv_dt.triggered.connect(self.openCsv_dt)
        self.actionOpen_csv_fullX.triggered.connect(self.openCsv_fullX)
        self.actionOpen_mdsplus_QXT.triggered.connect(self.openMdsplusQXT)
        self.actionOpen_mdsplus_QOC.triggered.connect(self.openMdsplusQOC)
        self.actionDrawPlots.triggered.connect(self.drawPlots)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v1)
        self.actionExport_time_to_separate_file.triggered.connect(self.export_to_csv_v2)

        self.actionClear.triggered.connect(self.clearAll)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft=0
        self.xRight=0
        self.drawUI.clicked.connect(self.drawPlots)
        self.drawSpectrogramUI.clicked.connect(self.drawSpectrogram)
        self.resample_btn.clicked.connect(self.resampleDataDecimation)
        self.subtractSGF.clicked.connect(self.subtractSGFilter)
        self.replaceWithSGF.clicked.connect(self.replaceWithSGFilter)

    def resampleDataResampy(self):
        resampler = DataResample(self)
        # print('np.double(self.NewSamplingRate_kHz.text())*1000', np.double(self.NewSamplingRate_kHz.text())*1000)
        newSampleRateHz = int(np.double(self.NewSamplingRate_kHz.text())*1000) if np.double(self.NewSamplingRate_kHz.text())>0.01 else 1000000
        resampler.downSampleResampy(newSampleRateHz)

    def resampleDataDecimation(self):
        resampler = DataResample(self)
        newSampleRateHz = int(np.double(self.NewSamplingRate_kHz.text())*1000) if np.double(self.NewSamplingRate_kHz.text())>0.01 else 1000000
        resampler.downSampleDecimate(newSampleRateHz)



    def drawSpectrogram(self):
        for sig in self.dataIn:
            w7xSpectr = w7xSpectrogram(self)
            w7xSpectr.show()
            w7xSpectr.setDataToSpectrogram(sig[self.xLeft:self.xRight])
            w7xSpectr.drawSpectrogram()
        self.clearAll()

    def clearAll(self):
        self.mainPlotWidget.clear()
        self.files.clear()
        self.dataIn.clear()
        self.dti.clear()
        self.frq.clear()
        self.nextPen = 0
        self.channelsList.clear()
        self.xLeft=0
        self.xRight=0


    def openCsv_dt(self):
        CsvTxtR = ImportFromTxt(self)
        CsvTxtR.openCsvTxt_dt()
    def openCsv_fullX(self):
        CsvTxtR = ImportFromTxt(self)
        CsvTxtR.openCsvTxt_fullX()

    def openMdsplusQXT(self):
        openQxt = ImportFromMdsplus(self)
        openQxt.openQXT()

    def openMdsplusQOC(self):
        openQoc = ImportFromMdsplus(self)
        openQoc.openQOC()

    def export_to_csv_v1(self):
        toTxt = ExportToTxt(self)
        toTxt.export_to_csv_v1()

    def export_to_csv_v2(self):
        toTxt = ExportToTxt(self)
        toTxt.export_to_csv_v2()

    def drawPlots(self):
        xyPlotter = XYPlotter(self)
        xyPlotter.drawPlots()

    def subtractSGFilter(self):

        xyFilt = XYFiltering(self)
        xyFilt.subtractSGFilter()
        self.drawPlots()

    def replaceWithSGFilter(self):
        xyFilt = XYFiltering(self)
        xyFilt.replaceWithSGFilter()
        self.drawPlots()

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
    window = mainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

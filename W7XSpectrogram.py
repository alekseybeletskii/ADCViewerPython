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


# !/usr/bin/env python3
# -*- coding: utf-8 -*-


# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui, QtWidgets, QtCore
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog


from GUIs import spectrogramLayout
# it also keeps events etc that we defined in Qt Design
import sys
# from PyQt5 import QtGui

import numpy as np

import pyqtgraph as pg
import time

from scipy import signal
import pyqtgraph
from utils.TestDataGenerator import TestDataGenerator
from utils.SpectrogramPeaksDetection import SpectrogramPeaksDetection

from GUIs.SliderWidget import SliderWidget
from utils.SpectgrogramSettings import SpectgrogramSettings

from utils.DataFilters import DataFilters
from utils.DataResample import DataResample

from importExport.ExportToTxtImg import ExportToTxtImg

# from os import path
# import pyqtgraph.exporters
# from datetime import datetime
from utils.DataLimits import DataLimits

from importExport.ImportFromMdsplus import ImportFromMdsplus


class W7XSpectrogram(QtWidgets.QMainWindow, spectrogramLayout.Ui_Spectrogram):

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.setConfigOption('leftButtonPan', False)

        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.spectrogramSettingsWidget = SpectgrogramSettings(self, self)
        self.settings = {}
        self.spectrogramSettingsWidget.setDefaultSettings()

        self.redrawSpectrogramBtn.clicked.connect(self.drawSpectrogram)
        self.settings_btn.clicked.connect(self.settingsUi)
        self.actionClearAll.triggered.connect(self.clearAllSpectrogram)

        self.actionGenerateTestData.triggered.connect(self.generateData)
        self.actionOpen_mdsplus.triggered.connect(self.openMdsplus)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft = 0
        self.xRight = 0

        self.Sxx = np.ndarray

        self.spectrogramWindow = self.spectrogram_UI
        self.f = None
        self.t = None
        self.frq = 0

        self.SxxMax = None
        self.SxxMin = None

        self.zoomedSxxMaxMin = {}
        self.dataXLimitsIndexes = {}
        self.tLimitsIndexes = {}
        self.fLimitsIndexes = {}

        self.spectrogramTitle = ' '

        self.peakSlider = SliderWidget(0.1, 1)
        self.peakSlider.setToolTip('peaks detection')

        self.horizontalLayout_spectr.addWidget(self.peakSlider)

        self.peaksCurve = pg.PlotDataItem()

        self.allPeaksXPoints = []
        self.allPeaksYPoints = []
        self.spectrPeaksDetection = SpectrogramPeaksDetection(self)

        self.spectrPlot = self.spectrogramWindow.addPlot()
        self.spectrPlot.setTitle(self.spectrogramTitle, **{'color': '#0000ff', 'size': '12pt'})
        # Add labels to the axis
        self.spectrPlot.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        self.spectrPlot.setLabel('left', "Frequency", units='Hz')

        # a histogram with which to control the gradient of the image
        self.hist = pg.HistogramLUTItem(fillHistogram=False)
        self.hist.gradient.restoreState(self.settings["histoGradient"])
        # If don't add the histogram to the window, it stays invisible
        self.spectrogramWindow.addItem(self.hist)
        self.hotkey = {}
        self.ui_hotkey('ajustSettings', "Shift+s", self.settingsUi)
        self.ui_hotkey('drawSpectr', "Shift+d", self.drawSpectrogram)
        self.dataToSpectrogram = np.array([])
        self.spectrogramImage = None
        # self.generateData()
        self.proxy = pg.SignalProxy(self.spectrPlot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, evt):
        mousePoint = self.spectrPlot.vb.mapSceneToView(evt[0])
        self.mouseXY_UI.setText(
            "<span style='font-size: 14pt; color: green'> x = %0.2f, <span style='color: green'> y = %0.2f</span>" % (
                mousePoint.x(), mousePoint.y()))

    def openMdsplus(self):
        start = self.settings["startMdsplusTime"]
        end = self.settings["endMdsplusTime"]
        resample = self.settings["deltaMdsplusTime"]
        shotNumber = self.settings["shotNum"]
        treeName = self.settings["treeName"]

        openMds = ImportFromMdsplus(self)
        self.dataInLabels = openMds.readDataLabels()

        for i in range(len(self.dataInLabels)):
            d, dt = openMds.getMdsplusData(self.dataInLabels[i], treeName, shotNumber, start, end, resample)
            self.frq = (int(round(np.power(dt, -1))))
            self.setDataToSpectrogram(self.dataInLabels[i], d, self.frq)
            self.drawSpectrogram()
            if not i == len(self.dataInLabels) - 1:
                self.dataToSpectrogram = np.array([])

    def findSpectroLimitsIndexes(self):
        axt = self.spectrPlot.getAxis('bottom')
        axf = self.spectrPlot.getAxis('left')
        dt = abs(np.double(
            self.t[len(self.t) - 1] - self.t[len(self.t) - 2]))
        self.tLimitsIndexes = DataLimits.getDataLimitsIndexes(axt, dt, len(self.t))
        df = abs(np.double(
            self.f[len(self.f) - 1] - self.f[len(self.f) - 2]))
        self.fLimitsIndexes = DataLimits.getDataLimitsIndexes(axf, df, len(self.f))

        self.dataXLimitsIndexes = DataLimits.getDataLimitsIndexes(axt, np.power(np.double(self.frq), -1),
                                                                  len(self.dataToSpectrogram))

        self.zoomedSxxMaxMin['max'] = np.max(
            self.Sxx[self.fLimitsIndexes.get('minIndex'): self.fLimitsIndexes.get('maxIndex'),
            self.tLimitsIndexes.get('minIndex'):self.tLimitsIndexes.get('maxIndex')])
        self.zoomedSxxMaxMin['min'] = np.min(
            self.Sxx[self.fLimitsIndexes.get('minIndex'): self.fLimitsIndexes.get('maxIndex'),
            self.tLimitsIndexes.get('minIndex'):self.tLimitsIndexes.get('maxIndex')])

    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)



    def butterBandPassZeroPhase(self):
        dataFilters = DataFilters(self)
        self.dataToSpectrogram = dataFilters.butterworthBandFilterZeroPhase(self.dataToSpectrogram,
                                                                            self.settings["bandPassLowcut_kHz"] * 1000,
                                                                            self.settings["bandPassHighcut_kHz"] * 1000,
                                                                            self.frq, self.settings["bandPassOrder"],
                                                                            'bandpass')

    def butterBandStopZeroPhase(self):
        dataFilters = DataFilters(self)
        self.dataToSpectrogram = dataFilters.butterworthBandFilterZeroPhase(self.dataToSpectrogram,
                                                                            self.settings["bandStopLowcut_kHz"] * 1000,
                                                                            self.settings["bandStopHighcut_kHz"] * 1000,
                                                                            self.frq, self.settings["bandStopOrder"],
                                                                            'bandstop')

    def settingsUi(self):
        self.spectrogramSettingsWidget.show()

    def updatePeakSliderRange(self):
        self.findSpectroLimitsIndexes()
        self.peakSlider.setSliderMaxMin(self.zoomedSxxMaxMin['max'], self.zoomedSxxMaxMin['min'])

    def findSpectroPeaks(self):
        self.spectrPeaksDetection.findSpectroPeaks()

    def generateData(self):
        testDataGenerator = TestDataGenerator(self)
        # d, f = testDataGenerator.generatePeriodicAndNoise()
        title = 'Nightingale song spectrogram'
        d, f = testDataGenerator.nightingaleSongSpectr()
        self.setDataToSpectrogram(title, d, f)

    def setDataToSpectrogram(self, specTitle, signalIn, frq):
        self.spectrogramTitle = specTitle
        self.dataToSpectrogram = signalIn
        self.frq = frq
        self.spectrogramSettingsWidget.settings["fs_kHz"] = self.frq / 1000.0
        self.spectrogramSettingsWidget.putSettingsToUi()
        self.spectrogramSettingsWidget.checkAndApplySettins()
        self.dataXLimitsIndexes["minIndex"] = 0
        self.dataXLimitsIndexes["maxIndex"] = len(self.dataToSpectrogram) - 1

    def resampleDataDecimation(self):
        resampler = DataResample(self)
        targetFrq_Hz = int(np.double(self.settings["targetFrq_kHz"]) * 1000) if self.frq > np.double(
            self.settings["targetFrq_kHz"]) > 0.01 else self.frq
        self.dataToSpectrogram = resampler.downSampleDecimate(self.dataToSpectrogram, self.frq, targetFrq_Hz)
        self.frq = self.settings["targetFrq_kHz"] * 1000
        self.spectrogramSettingsWidget.settings["fs_kHz"] = self.frq / 1000.0
        self.spectrogramSettingsWidget.putSettingsToUi()
        self.spectrogramSettingsWidget.checkAndApplySettins()
        self.dataXLimitsIndexes["minIndex"] = 0
        self.dataXLimitsIndexes["maxIndex"] = len(self.dataToSpectrogram) - 1


    def drawSpectrogram(self):

        if self.dataToSpectrogram.size > 0:
            self.draw()

        if self.settings["exportSpectrogramToImg"]:
            self.exportToImg(self.spectrogramTitle)

    def draw(self):
        # self.frq = self.settings["fs_kHz"] * 1000.0
        print('input data frequency, *BEFORE* downsampling, Hz: ' + str(self.frq))
        self.spectrPlot.removeItem(self.spectrogramImage)
        # self.peakSlider.slider.disconnect()

        self.dataToSpectrogram = self.dataToSpectrogram[self.dataXLimitsIndexes["minIndex"] : self.dataXLimitsIndexes["maxIndex"]]


        if self.settings["applyDownsampling"] and self.settings["targetFrq_kHz"] < self.settings["fs_kHz"]:
            self.resampleDataDecimation()
            # self.spectrogramSettingsWidget.settings["applyDownsampling"] = False
            # self.spectrogramSettingsWidget.putSettingsToUi()
            print('input data frequency, *AFTER* downsampling, Hz: ' + str(self.frq))

        if self.settings["applyBandPass"]:
            self.butterBandPassZeroPhase()
            # self.spectrogramSettingsWidget.settings["applyBandPass"] = False
            # self.spectrogramSettingsWidget.putSettingsToUi()

        if self.settings["applyBandStop"]:
            self.butterBandStopZeroPhase()

        if self.settings["nfft"] >= len(self.dataToSpectrogram):
            # self.spectrogramSettingsWidget.settings["nfft"] = int(len(self.dataToSpectrogram) / 4.0)
            self.spectrogramSettingsWidget.settings["nfft"] = 256
            self.spectrogramSettingsWidget.putSettingsToUi()
            self.spectrogramSettingsWidget.checkAndApplySettins()

        self.f, self.t, self.Sxx = signal.spectrogram(self.dataToSpectrogram,
                                                      nfft=self.settings["nfft"],
                                                      fs=int(float(self.settings["fs_kHz"]) * 1000.0),
                                                      window=self.settings["window"],
                                                      nperseg=self.settings["nperseg"],
                                                      noverlap=self.settings["noverlap"],
                                                      detrend=self.settings["detrend"],
                                                      scaling=self.settings["scaling"],
                                                      mode=self.settings["mode"])
        if str(self.settings["scaleLinLogSqrt"]).casefold() == 'log10':
            self.Sxx = np.log10(self.Sxx)
        elif str(self.settings["scaleLinLogSqrt"]).casefold() == 'sqrt':
            self.Sxx = np.sqrt(self.Sxx)
            # self.Sxx = np.cbrt(self.Sxx)
            # self.Sxx = np.exp2(self.Sxx)
            # self.Sxx = np.exp(self.Sxx)
            # self.Sxx = np.power(self.Sxx, 0.2)
            # self.Sxx = np.log(self.Sxx)

        self.SxxMin = np.min(self.Sxx)
        self.SxxMax = np.max(self.Sxx)
        self.spectrogramImage = pyqtgraph.ImageItem()
        self.spectrPlot.addItem(self.spectrogramImage)

        # self.Sxx contains the amplitude for each pixel
        self.spectrogramImage.setImage(self.Sxx)
        # Scale the X and Y Axis to time and frequency (standard is pixels)
        self.spectrogramImage.scale(self.t[-1] / np.size(self.Sxx, axis=1),
                                    self.f[-1] / np.size(self.Sxx, axis=0))
        self.hist.setImageItem(self.spectrogramImage)

        # self.spectrPlot.removeItem( self.spectrogramImage)

        self.hist.setLevels(self.SxxMin, self.SxxMax)
        self.hist.gradient.restoreState(self.settings["histoGradient"])
        if self.settings["setHistogramLevels"]:
            self.hist.setLevels(self.settings["histogramLevelMin"] * self.SxxMax,
                                self.settings["histogramLevelMax"] * self.SxxMax)
        # Limit panning/zooming to the spectrogram
        self.spectrPlot.setLimits(xMin=0, xMax=self.t[-1], yMin=0, yMax=self.f[-1])

        self.ajustPeakSliderWidget()

        self.spectrPlot.setTitle(self.spectrogramTitle, **{'color': '#0000ff', 'size': '14pt'})

    def exportToImg(self, imgTitle):
        # when widget is not displayed on the screen but used to export image
        # QtWidgets.QApplication.processEvents()
        imgExporter = ExportToTxtImg(self)
        imgExporter.exportWidgetToImg(self.spectrogramWindow, imgTitle)

    def ajustPeakSliderWidget(self):
        self.spectrPlot.sigRangeChanged.connect(self.updatePeakSliderRange)
        self.peakSlider.setSliderMaxMin(self.SxxMax, self.SxxMin)
        self.peakSlider.slider.setValue(self.peakSlider.slider.maximum())
        self.peakSlider.slider.valueChanged.connect(self.findSpectroPeaks)

    # def showOrExport(self):

    def exitApp(self):
        # sys.exit()
        self.close()

    def closeEvent(self, event):
        # event.accept()
        # sys.exit()

        if __name__ == '__main__':
            event.accept()
            sys.exit()
        else:
            event.accept()

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

    # @staticmethod
    # def generateTestData():
    #     # Create the data
    #     fs = 1e4
    #     N = 1e5
    #     amp = 2 * np.sqrt(2)
    #     noise_power = 0.01 * fs / 2
    #     # noise_power = 0.001 * fs / 2
    #     time = np.arange(N) / float(fs)
    #     mod = 500 * np.cos(2 * np.pi * 0.25 * time)
    #     carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
    #     noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
    #     noise *= np.exp(-time / 5)
    #     return  carrier + noise
    #
    def clearAllSpectrogram(self):
        # self.spectrogram_UI.clear()
        self.Sxx = []
        self.SxxMax = None
        self.SxxMin = None
        self.allPeaksXPoints = []
        self.allPeaksYPoints = []
        self.dataToSpectrogram = np.array([])
        self.zoomedSxxMaxMin.clear()
        self.dataXLimitsIndexes.clear()
        self.tLimitsIndexes.clear()
        self.fLimitsIndexes.clear()

        self.spectrogramTitle = ' '
        self.spectrPlot.setTitle(' ')

        self.spectrPlot.removeItem(self.spectrogramImage)
        self.spectrogramImage = None

        self.peakSlider.slider.disconnect()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = W7XSpectrogram(parent=None)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

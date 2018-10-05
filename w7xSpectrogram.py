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


# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

from GUIs import spectrogramLayout
# it also keeps events etc that we defined in Qt Design
import sys
# from PyQt5 import QtGui

import numpy as np

import pyqtgraph as pg

from scipy import signal
import pyqtgraph
from utils.TestDataGenerator import TestDataGenerator
from utils.SpectrogramPeaksDetection import SpectrogramPeaksDetection

from GUIs.SliderWidget import SliderWidget
from utils.SpectgrogramSettings import SpectgrogramSettings

class w7xSpectrogram(QtWidgets.QMainWindow, spectrogramLayout.Ui_MainWindow):


    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.setConfigOption('leftButtonPan', False)


        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.spectrogramSettingsWidget = SpectgrogramSettings(self,self)
        self.settings = {}
        self.spectrogramSettingsWidget.setDefaultSettings()

        self.dataToSpectrogram = w7xSpectrogram.generateTestData()

        self.redrawSpectrogramBtn.clicked.connect(self.drawSpectrogram)
        self.settings_btn.clicked.connect(self.settingsUi)
        self.actionClearAll.triggered.connect(self.clearAll)

        self.actionGenerateTestData.triggered.connect(self.generateData)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft = 0
        self.xRight = 0

        self.Sxx = np.ndarray

        self.win = self.spectrogram_UI
        self.spectrPlot = None
        self.f = None
        self.t = None
        self.SxxMax = None
        self.SxxMin = None

        self.peakSlider = SliderWidget(0.1, 1)

        self.horizontalLayout_spectr.addWidget(self.peakSlider)

        self.peaksCurve = pg.PlotDataItem()

        self.allPeaksXPoints = []
        self.allPeaksYPoints = []

        self.spectrPeaksDetection = SpectrogramPeaksDetection(self)

        self.spectrPlot = self.win.addPlot()

        # a histogram with which to control the gradient of the image
        self.hist = pg.HistogramLUTItem(fillHistogram=False)
        # If don't add the histogram to the window, it stays invisible
        self.win.addItem(self.hist)
        self.hotkey = {}
        self.ui_hotkey('ajustSettings', "Shift+s", self.settingsUi)

    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)

    def settingsUi(self):
        self.spectrogramSettingsWidget.show()

    def updatePeakSliderRange(self):
        self.spectrPeaksDetection.findSpectroLimits()
        self.spectrPeaksDetection.findSliderRange()


    def findSpectroPeaks(self):
        self.spectrPeaksDetection.findSpectroPeaks()


    def clearAll(self):
        self.spectrogram_UI.clear()
        self.Sxx = np.ndarray
        self.SxxMax = None
        self.SxxMin = None
        self.allPeaksXPoints = []
        self.allPeaksYPoints = []

    def generateData(self):
        testDataGenerator = TestDataGenerator(self)
        self.dataToSpectrogram = testDataGenerator.nightingaleSongSpectr()

    def setDataToSpectrogram(self,signalIn):
        self.dataToSpectrogram = signalIn
    # def drawSpectrogram(self,signalIn):

    def drawSpectrogram(self):

        self.peakSlider.slider.disconnect()

        self.f, self.t, self.Sxx = signal.spectrogram(self.dataToSpectrogram,
                                                      nfft=self.settings["nfft"],
                                                      fs= self.settings["fs_kHz"]*1000.0,
                                                      window = self.settings["window"],
                                                      nperseg=self.settings["nperseg"],
                                                      noverlap=self.settings["noverlap"],
                                                      detrend=self.settings["detrend"],
                                                      scaling=self.settings["scaling"],
                                                      mode=self.settings["mode"])

        if str(self.settings["scaleLinLogSqrt"]).casefold() == 'log10':
            self.Sxx = 10 * np.log10(self.Sxx)
        elif str(self.settings["scaleLinLogSqrt"]).casefold() == 'sqrt':
            self.Sxx = np.sqrt(self.Sxx)

        self.SxxMin = np.min(self.Sxx)
        self.SxxMax = np.max(self.Sxx)

        img = pyqtgraph.ImageItem()

        self.spectrPlot.addItem(img)


        # self.Sxx contains the amplitude for each pixel
        img.setImage(self.Sxx)
        # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(self.t[-1] / np.size(self.Sxx, axis=1),
                  self.f[-1] / np.size(self.Sxx, axis=0))


        # x =  np.linspace(0.01,0.05,10)
        # y =  np.linspace(100000,200000,10)
        # self.spectrPlot.plot(x, y, pen=pg.mkPen(color=(255,0,0), width=5), name="Red curve", symbol='o' , symbolBrush = "k", symbolPen = "k", symbolSize=18)

        self.hist.setImageItem(img)
        tickMiddle = 0.5
        if str(self.settings["scaleLinLogSqrt"]).casefold() == 'linear':
            self.hist.setLevels(self.SxxMin, self.SxxMax)
        if str(self.settings["scaleLinLogSqrt"]).casefold() == 'sqrt':
            self.hist.setLevels(self.SxxMin, self.SxxMax)
            tickMiddle = 0.8

        if str(self.settings["scaleLinLogSqrt"]).casefold() == 'log10':
            self.hist.setLevels(self.SxxMin, self.SxxMax)

        # This gradient is roughly comparable to the gradient used by Matplotlib
        # You can adjust it and then save it using hist.gradient.saveState()
        # self.hist.gradient.restoreState(
        #     {'mode': 'rgb',
        #      'ticks': [(0.5, (0, 182, 188, 255)),
        #                (1.0, (246, 111, 0, 255)),
        #                (0.0, (75, 0, 113, 255))]})

        # self.hist.gradient.restoreState(
        #     {'mode': 'rgb',
        #      'ticks': [(tickMiddle, (0, 160, 160, 255)),
        #                (1.0, (255, 255, 255, 255)),
        #                (0.0, (255, 255, 255, 255))]})

        # self.hist.gradient.restoreState(
        #     {'mode': 'rgb',
        #      'ticks': [(tickMiddle, (0, 160, 160, 255)),
        #
        #                (0.0, (255, 255, 255, 255))]})
        self.hist.gradient.restoreState(self.settings["histoGradient"])


        # self.hist.setHistogramRange(0,1)



        # Limit panning/zooming to the spectrogram
        self.spectrPlot.setLimits(xMin=0, xMax=self.t[-1], yMin=0, yMax=self.f[-1])
        # Add labels to the axis
        self.spectrPlot.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        self.spectrPlot.setLabel('left', "Frequency", units='Hz')




        self.show()

        self.spectrPlot.sigRangeChanged.connect(self.updatePeakSliderRange)

        self.peakSlider.setSliderMaxMin(self.SxxMax, self.SxxMin)
        self.peakSlider.slider.setValue(self.peakSlider.slider.maximum())
        self.peakSlider.slider.valueChanged.connect(self.findSpectroPeaks)

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

    @staticmethod
    def generateTestData():
        # Create the data
        fs = 1e4
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        # noise_power = 0.001 * fs / 2
        time = np.arange(N) / float(fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        return  carrier + noise

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = w7xSpectrogram(parent=None)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

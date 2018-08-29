# /*
#  * ******************** BEGIN LICENSE BLOCK *********************************
#  *
#  * w7x-dataViewer
#  * Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
#  * All rights reserved
#  *
#  * github: https://github.com/alekseybeletskii
#  *
#  * The w7x-dataViewer software serves for visualization and simple processing
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


import os.path as ospath

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui, QtWidgets
from ast import literal_eval as make_tuple
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import spectrogramLayout  # This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Design
import sys
# from PyQt5 import QtGui

import numpy as np

import pandas as pd

import MDSplus as m

import pyqtgraph as pg

from scipy import signal
import matplotlib.pyplot as plt
import pyqtgraph

from scipy.signal import savgol_filter


class w7xSpectrogram(QtWidgets.QMainWindow, spectrogramLayout.Ui_MainWindow):

    @classmethod
    def generateTestData(cls):
        # Create the data
        fs = 10e3
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        time = np.arange(N) / float(fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        return  carrier + noise
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)

        # nfft : int, optional.
        #  Length of the FFT used, if a zero padded FFT is desired. If None, the FFT length is nperseg. Defaults to None.
        self.nfft = 256
        # fs : float, optional.
        #  Sampling frequency of the x time series. Defaults to 1.0.
        self.fs = 1000
        # window : str or tuple or array_like, optional.
        #  Desired window to use. Defaults to a Tukey window with shape parameter of 0.25
        # Window types: boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen,
        # bohman, blackmanharris, nuttall, barthann (and some others that needs parameters)
        # self.window = ''.join(('tukey', '0.25'))
        self.window = 'hamming'
        # nperseg : int, optional.
        #  Length of each segment. Defaults to None, but if window is str or tuple,
        # is set to 256, and if window is array_like, is set to the length of the window.
        self.nperseg = 256
        # noverlap : int, optional.
        #  Number of points to overlap between segments. If None, noverlap = nperseg // 8. Defaults to None.
        self.noverlap = 32
        # detrend : str or function or False, optional
        # Specifies how to detrend each segment. If detrend is a string, it is passed as the type argument
        # to the detrend function. If it is a function, it takes a segment and returns a detrended segment.
        # If detrend is False, no detrending is done. Defaults to ‘constant’.
        #  If type == 'constant', only the mean of data is subtracted.
        self.detrend = False
        # scaling : { ‘density’, ‘spectrum’ }, optional
        # Selects between computing the power spectral density (‘density’)
        # where Sxx has units of V**2/Hz and computing the power spectrum (‘spectrum’) where Sxx has units of V**2,
        # if x is measured in V and fs is measured in Hz. Defaults to ‘density’.
        self.scaling = 'density'
        # mode : str, optional
        # Defines what kind of return values are expected. Options are [‘psd’, ‘complex’, ‘magnitude’, ‘angle’, ‘phase’].
        # ‘complex’ is equivalent to the output of stft with no padding or boundary extension.
        # ‘magnitude’ returns the absolute magnitude of the STFT. ‘angle’ and ‘phase’ return the complex angle of the STFT,
        #  with and without unwrapping, respectively.
        self.mode = 'psd'

         # ‘linear’ is no scaling
        # 'log' is 10*np.log10(Sxx)
        # 'sqrt' is np.sqrt(Sxx)
        self.scale = 'linear'

        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.resetParams_ui.clicked.connect(self.setDefaultParams)

        self.dataToSpectrogram = w7xSpectrogram.generateTestData()

        self.redrawSpectrogramBtn.clicked.connect(self.drawSpectrogram)
        self.actionClearAll.triggered.connect(self.clearAll)

        self.actionGenerateTestData.triggered.connect(self.generateData)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft = 0
        self.xRight = 0

    def clearAll(self):
        self.spectrogram_UI.clear()

    def setDefaultParams(self):
        self.nfft = 256
        self.nfft_ui.setText('256')
        self.fs = 1000
        self.fs_kHz_ui.setText('1000')
        self.window = 'hamming'
        self.window_ui.setText('hamming')
        self.nperseg = 256
        self.nperseg_ui.setText('256')
        self.noverlap = 32
        self.noverlap_ui.setText('32')
        self.detrend = 'constant'
        self.detrend_ui.setText('constant')
        self.scaling = 'density'
        self.scaling_ui.setText('density')
        self.mode = 'psd'
        self.mode_ui.setText('psd')
    def setParamsValues(self):
        self.nfft = int(self.nfft_ui.text())
        self.fs = float(self.fs_kHz_ui.text())*1000.0
        # self.window = make_tuple(self.window_ui.text())
        self.window = self.window_ui.text()
        self.nperseg = int(self.nperseg_ui.text())
        self.noverlap = int(self.noverlap_ui.text())
        detrend = self.detrend_ui.text()
        self.detrend = False if detrend.casefold() =='false' else detrend
        self.scaling = self.scaling_ui.text()
        self.mode = self.mode_ui.text()
    def generateData(self):
        # Create the data
        fs = 10e3
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        time = np.arange(N) / float(fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        self.dataToSpectrogram = carrier + noise
        return  carrier + noise

    def setDataToSpectrogram(self,signalIn):
        self.dataToSpectrogram = signalIn
    # def drawSpectrogram(self,signalIn):
    def drawSpectrogram(self):
        self.spectrogram_UI.clear()
        # signalIn = self.generateData()
        self.setParamsValues()
        # f, t, Sxx = signal.spectrogram(self.generateData(), 10000)
        f, t, Sxx = signal.spectrogram(self.dataToSpectrogram, fs=self.fs, window = self.window, nperseg=self.nperseg, noverlap=self.noverlap, nfft=self.nfft,
                                       detrend=self.detrend, scaling=self.scaling, mode=self.mode)

        if str(self.scaleLinLogSqrt.currentText()).casefold() == 'log10':
            Sxx = 10 * np.log10(Sxx)
        elif str(self.scaleLinLogSqrt.currentText()).casefold() == 'sqrt':
            Sxx = np.sqrt(Sxx)


        # Interpret image data as row-major instead of col-major
        pyqtgraph.setConfigOptions(imageAxisOrder='row-major')
        # pyqtgraph.mkQApp()
        # win = pyqtgraph.GraphicsLayoutWidget()
        win = self.spectrogram_UI
        # A plot area (ViewBox + axes) for displaying the image
        p1 = win.addPlot()

        # Item for displaying image data
        img = pyqtgraph.ImageItem()
        p1.addItem(img)
        # Add a histogram with which to control the gradient of the image
        hist = pyqtgraph.HistogramLUTItem()
        # Link the histogram to the image
        hist.setImageItem(img)
        # If you don't add the histogram to the window, it stays invisible, but I find it useful.
        win.addItem(hist)
        # Show the window
        # self.show()
        # Fit the min and max levels of the histogram to the data available
        hist.setLevels(np.min(Sxx), np.max(Sxx))
        # This gradient is roughly comparable to the gradient used by Matplotlib
        # You can adjust it and then save it using hist.gradient.saveState()
        hist.gradient.restoreState(
            {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]})
        # Sxx contains the amplitude for each pixel
        img.setImage(Sxx)
        # Scale the X and Y Axis to time and frequency (standard is pixels)
        img.scale(t[-1] / np.size(Sxx, axis=1),
                  f[-1] / np.size(Sxx, axis=0))
        # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
        # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')

        self.show()


        # Plotting with Matplotlib in comparison
        # plt.pcolormesh(t, f, Sxx)
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.colorbar()
        # plt.show()

    def exitApp(self):
        if __name__ == '__main__':
            sys.exit()
        else:
            self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = w7xSpectrogram(parent=None)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

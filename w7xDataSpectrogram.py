#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os.path as ospath

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import  QtGui, QtWidgets

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

class w7xSpectrogram(QtWidgets.QMainWindow, spectrogramLayout.Ui_MainWindow, spectrogramLayout.GraphicsLayoutWidget):
    # Interpret image data as row-major instead of col-major


    def __init__(self):
        super(self.__class__, self).__init__()
        self.signalIn = np.ndarray
        self.t = np.ndarray
        self.f = np.ndarray
        self.Sxx = np.ndarray
        self.fs = np.float64(10e3)


        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.fs = self.samplingRate_kHz.text()
        self.actionClear.triggered.connect(self.clearAll)
        self.actionExit.triggered.connect(self.exitApp)
        self.xLeft=0
        self.xRight=0




    def generateData(self):
        # Create the data
        fs = 10e3
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        time = np.arange(N) / float(self.fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        return carrier + noise


    def drawSpectrogram(self,signalIn):
        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.mkQApp()

        f, t, Sxx = signal.spectrogram(signalIn, 10e3)
        win = self.spectrogram_UI
        # win = pg.GraphicsLayoutWidget
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
        win.show()
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
                  t[-1] / np.size(Sxx, axis=0))
        # Limit panning/zooming to the spectrogram
        p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=t[-1])
        # Add labels to the axis
        p1.setLabel('bottom', "Time", units='s')
        # If you include the units, Pyqtgraph automatically scales the axis and adjusts the SI prefix (in this case kHz)
        p1.setLabel('left', "Frequency", units='Hz')



    def clearAll(self):
        self.plot.clear()
        self.files.clear()
        self.nextPen = 0
        self.channelsList.clear()


















    def exitApp(self):
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = w7xSpectrogram()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

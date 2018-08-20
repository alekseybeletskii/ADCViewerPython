#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
/*
 * 	********************* BEGIN LICENSE BLOCK *********************************
 * 	Soft-X-T_Viewer
 * 	Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
 * 	All rights reserved
 *
 * 	github: https://github.com/alekseybeletskii
 *
 * 	The ADCViewerPython software serves for visualization and simple processing
 * 	of any data recorded with Analog Digital Converters in binary or text form.
 *
 * 	Commercial support is available. To find out more contact the author directly.
 *
 * 	Redistribution and use in source and binary forms, with or without
 * 	modification, are permitted provided that the following conditions are met:
 *
 * 	  1. Redistributions of source code must retain the above copyright notice, this
 * 	     list of conditions and the following disclaimer.
 * 	  2. Redistributions in binary form must reproduce the above copyright notice,
 * 	     this list of conditions and the following disclaimer in the documentation
 * 	     and/or other materials provided with the distribution.
 *
 * 	The software is distributed to You under terms of the GNU General Public
 * 	License. This means it is "free software". However, any program, using
 * 	ADCViewerPython _MUST_ be the "free software" as well.
 * 	See the GNU General Public License for more details
 * 	(file ./COPYING in the root of the distribution
 * 	or website <http://www.gnu.org/licenses/>)
 *
 * 	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * 	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * 	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * 	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 * 	ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * 	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * 	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * 	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * 	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * 	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * 	********************* END LICENSE BLOCK ***********************************
 */
"""

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

import mainLayout  # This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Design
import sys
from PyQt5 import QtGui

import numpy as np

import pandas as pd

import MDSplus as m


class mainApp(QtGui.QMainWindow, mainLayout.Ui_MainWindow):

    def __init__(self):

        super(self.__class__, self).__init__()
        self.files = []
        self.d = []
        self.nextPen = 0


        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.actionOpen_csv.triggered.connect(self.openCsv)
        self.actionDrawPlotsFromCsv.triggered.connect(self.drawPlotsFromCsv)
        self.actionOpen_mdsplus.triggered.connect(self.openMdsplus)
        self.actionDrawPlotsFromMdsplus.triggered.connect(self.drawPlotsFromMdsplus)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv)

        self.actionClear.triggered.connect(self.clearPlots)
        self.actionExit.triggered.connect(self.exitApp)

    #        plotexample(self)

    def clearPlots(self):
        self.plot.clear()
        self.files.clear()
        self.d = 0
        self.nextPen = 0

    def openCsv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #        files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        #         files, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileNames()", "csv files (*.csv)","csv files (*.csv);;All Files (*)", options=options)
        self.files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "All Files (*)",
                                                     "All Files (*)", options=options)

    def drawPlotsFromCsv(self):
        for i in range(len(self.files)):
            self.nextPen = self.nextPen + 1
            self.df = pd.read_csv(self.files[i], names=['x', 'y'], header=None)
            self.plot.plot(self.df['x'], self.df['y'], pen=self.nextPen)
            # print(self.files[i])
            # print(type(self.df))

    # def export_to_csv(self):
    #     # output to file
    #     for i in range(len(self.files)):
    #         filename = self.files[i] + "_" + ".csv"
    #         # np.savetxt(filename, np.array([self.df['x'], self.df['y']]).T, header="x, y", delimiter=', ')
    #         np.savetxt(filename, np.array([self.df['x'], self.df['y']]).T, delimiter=', ')

    def exitApp(self):
        sys.exit()

    def openMdsplus(self):
        # c = m.Connection('mds-data-1')
        c = m.Connection('ssh://oleb@mds-trm-1.ipp-hgw.mpg.de')
        c.get('SETTIMECONTEXT(*,*,10000Q)')
        #                c.get('SETTIMECONTEXT(*,*,10000Q)')
        c.openTree('qxt1', 171123027)
        #                c.openTree('qxt1',171123034)

        # self.d = np.array(c.get('DATA:CH82'))
        # np.append(self.d,
        #           c.get('DATA:CH83'),
        #           c.get('DATA:CH84')
        #           )

        self.d.append(c.get('DATA:CH82'))
        self.d.append(c.get('DATA:CH83'))
        self.d.append(c.get('DATA:CH84'))






    def export_to_csv(self):
        # output to file
        for i in range(len(self.d)):
            filename = self.files[i] + "_" + ".csv"
            # time array
            signal = self.d[i]
            time = (i, len(self.d[i]))
            np.savetxt(filename, np.array([time, signal]).T, delimiter=', ')


    def drawPlotsFromMdsplus(self):
        for i in range(len(self.d)):
            self.nextPen = self.nextPen + 1
            self.plot.plot(self.d[i], pen=(self.nextPen))


def main():
    app = QtGui.QApplication(sys.argv)
    window = mainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

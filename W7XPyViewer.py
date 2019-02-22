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
import sys
import numpy as np
import pyqtgraph as pg
from importExport.ImportFromTxt import ImportFromTxt
from importExport.ImportFromMdsplus import ImportFromMdsplus
from importExport.ImportFromLGraph import ImportFromLGraph
from utils.XYPlotter import XYPlotter
from importExport.ExportToTxtImg import ExportToTxtImg
from W7XSpectrogram import W7XSpectrogram
from utils.w7xPyViewerSettings import w7xPyViewerSettings
from utils.DataModifier import DataModifier
from GUIs.LegendItem import LegendItem
from os import path as ospath
from utils.DataLimits import DataLimits

class W7XPyViewer(QtWidgets.QMainWindow, w7xPyViewerLayout.Ui_w7xPyViewer):

    def __init__(self):

        super(self.__class__, self).__init__()

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('leftButtonPan', False)

        self.allData = []

        self.importFromSource = None

        self.latestFilePath = ospath.expanduser('~')

        self.setupUi(self)  # This is defined in design.py file automatically

        self.w7xPyViewerSettingsWidget = w7xPyViewerSettings(self, self)
        self.settings = {}
        self.w7xPyViewerSettingsWidget.setDefaultSettings()

        self.dataModifierWidget = DataModifier(self)

        self.actionOpen_Source.triggered.connect(lambda: self.openDataSource())

        self.actionCheckUncheckAll.triggered.connect(self.checkUncheckAllItems)

        self.actionSettings.triggered.connect(self.settingsUi)
        self.actionExport_to_csv.triggered.connect(self.export_to_csv_v1)
        self.actionExport_time_to_separate_file.triggered.connect(self.export_to_csv_v2)

        self.actionClear.triggered.connect(self.clearAllViewer)
        self.actionExit.triggered.connect(self.exitApp)

        self.drawSpectrogramUI.clicked.connect(self.drawSpectrogram)
        # self.settings_btn.clicked.connect(self.settingsUi)
        self.showDataModifier_ui.clicked.connect(self.dataModifierUi)



        self.hotkey = {}

        self.ui_hotkey('ajustSettings', "Shift+s", self.settingsUi)
        self.ui_hotkey('openSource', "Shift+o", self.openDataSource)

        self.xyPlotter = XYPlotter(self)

        self.proxy = pg.SignalProxy(self.mainPlotWidget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.listOfDataLablesWidget.setStyleSheet("QListWidget { background: transparent }")
        self.listOfDataLablesWidget.doubleClicked.connect(self.checkUncheckAllItems)
        self.listOfDataLablesWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)




    def openDataSource(self):

        self.clearAllViewer()
        switcher = {
            'MDSPlus': self.openMdsplus,
            'csv_txt': self.openCsv,
            'LGraph2': self.openLGraph
        }

        f = switcher.get(self.settings["dataSource"], 'unknown')
        f()
        self.importFromSource = None

        self.dataModifierWidget.createDefaultModifiersFile()

        self.populateListOfDataLables()

        self.drawPlots()



    def mouseMoved(self, evt):
        mousePoint = self.mainPlotWidget.plotItem.vb.mapSceneToView(evt[0])
        self.mouseXY_UI.setText(
            "<span style='font-size: 12pt; color: green'> x = %0.6f, <span style='color: green'> y = %0.6f</span>" % (
                mousePoint.x(), mousePoint.y()))


    def settingsUi(self):
        self.w7xPyViewerSettingsWidget.show()

    def dataModifierUi(self):
        self.dataModifierWidget.show()



    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)

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

    def clearAllViewer(self):
        # self.mainPlotWidget.clear()
        self.xyPlotter.clearPlots()
        self.listOfDataLablesWidget.clear()
        self.mainPlotWidget.plotItem.enableAutoRange()
        self.allData.clear()

    def openLGraph(self):
        self.clearAllViewer()
        self.importFromSource = ImportFromLGraph(self)
        self.allData = self.importFromSource.openLGraph()

    def openCsv(self):
        self.clearAllViewer()
        self.importFromSource = ImportFromTxt(self)
        self.allData = self.importFromSource.openCsvTxt()

    def openMdsplus(self):
        self.clearAllViewer()
        self.importFromSource = ImportFromMdsplus(self)
        self.allData = self.importFromSource.openMdsPlus()

    def export_to_csv_v1(self):
        toTxt = ExportToTxtImg(self)
        toTxt.export_to_csv('v1')
        toTxt = None

    def export_to_csv_v2(self):
        toTxt = ExportToTxtImg(self)
        toTxt.export_to_csv('v2')
        toTxt = None


    def drawPlots(self):
        self.xyPlotter.drawPlots()

    def populateListOfDataLables(self):
        # self.listOfDataLablesWidget.itemEntered.connect(
        #     lambda item:
        #     item.setCheckState(Qt.Checked if item.checkState() == Qt.Unchecked else Qt.Unchecked)
        #
        # )

        self.listOfDataLablesWidget.clear()

        colors = self.xyPlotter.colors
        nextColor = 0

        for i in range(len(self.allData)):
            legendItem = LegendItem(self.xyPlotter, i, True, self.allData[i].getPlotDataItem().name(),
                                    colors[nextColor])
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(legendItem.sizeHint())
            # item.setFlags(Qt.NoItemFlags)
            self.listOfDataLablesWidget.addItem(item)
            self.listOfDataLablesWidget.setItemWidget(item, legendItem)
            nextColor = nextColor + 1 if nextColor < len(colors) - 1 else 0


    def getAllCheckedItemsIndices(self):
        checked_items = []
        for index in range(self.listOfDataLablesWidget.count()):
            if self.listOfDataLablesWidget.item(index).checkState() == Qt.Checked:
                checked_items.append(self.listOfDataLablesWidget.item(index))
        return checked_items

    def checkUncheckAllItems(self):
        for index in range(self.listOfDataLablesWidget.count()):
            self.listOfDataLablesWidget.itemWidget(self.listOfDataLablesWidget.item(index)).itemCheckbox.click()
            # if self.listOfDataLablesWidget.itemWidget(self.listOfDataLablesWidget.item(index)).itemCheckbox.checkState() == Qt.Checked:
            #     self.listOfDataLablesWidget.itemWidget(self.listOfDataLablesWidget.item(index)).itemCheckbox.setChecked(False)
            # else:
            #     self.listOfDataLablesWidget.itemWidget(self.listOfDataLablesWidget.item(index)).itemCheckbox.setChecked(True)

            # print(self.listOfDataLablesWidget.itemWidget(self.listOfDataLablesWidget.item(index)).itemCheckbox.checkState())




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
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

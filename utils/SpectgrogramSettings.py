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


import sys
from GUIs import spectrogramSettingsLayout
from PyQt5 import QtWidgets, QtGui
import json
from pathlib import Path
from os import path, makedirs


class SpectgrogramSettings(QtWidgets.QMainWindow,spectrogramSettingsLayout.Ui_spectrogramSettingsWidget):

    def __init__(self, callingObj, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.settings = {}
        self.callingObj = callingObj

        self.saveSettings_btn.clicked.connect(self.saveSettingsToFile)
        self.resetSetings_btn.clicked.connect(self.setDefaultSettings)
        self.getFromUiApplyAndClose_btn.clicked.connect(self.getFromUiApplyAndClose)

        self.here = path.dirname(path.realpath(__file__))
        self.settingsDirName = "settings"
        self.settingsDirPath = path.join(self.here, '..', self.settingsDirName)
        if not path.exists(self.settingsDirPath):
            makedirs(self.settingsDirPath)
        self.settingsFilePath = Path(path.join(self.settingsDirPath, 'spectrSettings.txt'))

        self.hotkey = {}
        self.ui_hotkey('ajustSettings', "Return", self.getFromUiApplyAndClose)

    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)

    def getFromUiApplyAndClose(self):
        self.getFromUi()
        self.checkAndApplySettins()
        self.close()
    def saveSettingsToFile(self):

        if self.saveHistogramColor_ui:
           self.settings["histoGradient"] = self.callingObj.hist.gradient.saveState()
           self.saveHistogramColor_ui.setCheckState(False)

        self.getFromUi()
        self.checkAndApplySettins()

        with open(self.settingsFilePath, 'w') as outfile:
            json.dump(self.settings,outfile, indent=4)
        self.close()

    def getFromUi(self):

        self.settings["shotNum"]=int(self.shotNum_ui.text())
        self.settings["treeName"]=self.treeName_ui.text()
        self.settings["startMdsplusTime"]=self.startMdsplusTime_ui.text()
        self.settings["endMdsplusTime"]=self.endMdsplusTime_ui.text()
        self.settings["deltaMdsplusTime"]=self.deltaMdsplusTime_ui.text()

        self.settings["nfft"]=int(self.nfft_ui.text())
        self.settings["fs_kHz"]=float(self.fs_kHz_ui.text())

        #print('fs_kHz', self.fs_kHz_ui.text() )

        self.settings["window"]=self.window_ui.text()
        self.settings["nperseg"]=int(self.nperseg_ui.text())
        self.settings["noverlap"]=int(self.noverlap_ui.text())
        detrend = self.detrend_ui.text()
        self.settings["detrend"]=False if detrend.casefold() =='false' else detrend
        self.settings["scaling"]=self.scaling_ui.text()
        self.settings["mode"]=self.mode_ui.text()
        self.settings["scaleLinLogSqrt"]=self.scaleLinLogSqrt_ui.currentText()

        # self.settings["histoGradient"] = self.callingObj.hist.gradient.saveState()


        self.settings["applyBandPass"] = self.applyBandPass_ui.checkState()
        self.settings["bandpassLowcut_kHz"] = float(self.bandpassLowcut_kHz_ui.text())
        self.settings["bandpassHighcut_kHz"] = float(self.bandpassHighcut_kHz_ui.text())
        self.settings["order"] = int(self.order_ui.text())

        self.settings["applyDownsampling"] = self.applyDownsampling_ui.checkState()
        self.settings["targetFrq_kHz"] = float(self.targetFrq_kHz_ui.text())

        self.settings["setHistogramLevels"] = self.setHistogramLevels_ui.checkState()
        self.settings["histogramLevelMin"] = float(self.histogramLevelMin_ui.text())
        self.settings["histogramLevelMax"] = float(self.histogramLevelMax_ui.text())

        self.settings["saveHistogramColor"] = self.saveHistogramColor_ui.checkState()
        self.settings["exportSpectrogramToImg"] = self.exportSpectrogramToImg_ui.checkState()








    def putSettingsToUi(self):

        self.shotNum_ui.setText(str(self.settings["shotNum"]))
        self.treeName_ui.setText(str(self.settings["treeName"]))
        self.startMdsplusTime_ui.setText(str(self.settings["startMdsplusTime"]))
        self.endMdsplusTime_ui.setText(str(self.settings["endMdsplusTime"]))
        self.deltaMdsplusTime_ui.setText(str(self.settings["deltaMdsplusTime"]))

        self.nfft_ui.setText(str(self.settings["nfft"]))
        self.fs_kHz_ui.setText(str(self.settings["fs_kHz"]))
        self.window_ui.setText(str(self.settings["window"]))
        self.nperseg_ui.setText(str(self.settings["nperseg"]))
        self.noverlap_ui.setText(str(self.settings["noverlap"]))
        self.detrend_ui.setText(str(self.settings["detrend"]))
        self.scaling_ui.setText(str(self.settings["scaling"]))
        self.mode_ui.setText(str(self.settings["mode"]))
        self.scaleLinLogSqrt_ui.setCurrentText(self.settings["scaleLinLogSqrt"])

        # self.callingObj.hist.gradient.restoreState(self.settings["histoGradient"])

        self.applyBandPass_ui.setCheckState(self.settings["applyBandPass"])
        self.bandpassLowcut_kHz_ui.setText(str(self.settings["bandpassLowcut_kHz"]))
        self.bandpassHighcut_kHz_ui.setText(str(self.settings["bandpassHighcut_kHz"]))
        self.order_ui.setText(str(self.settings["order"]))

        self.applyDownsampling_ui.setCheckState(self.settings["applyDownsampling"])
        self.targetFrq_kHz_ui.setText(str(self.settings["targetFrq_kHz"]))

        self.setHistogramLevels_ui.setCheckState(self.settings["setHistogramLevels"])
        self.histogramLevelMin_ui.setText(str(self.settings["histogramLevelMin"]))
        self.histogramLevelMax_ui.setText(str(self.settings["histogramLevelMax"]))

        self.saveHistogramColor_ui.setCheckState(self.settings["saveHistogramColor"])
        self.exportSpectrogramToImg_ui.setCheckState(self.settings["exportSpectrogramToImg"])

    def loadSettingsFromFile(self):
        with open(self.settingsFilePath) as json_file:
            settingsFromFile = json.load(json_file)

            self.settings["shotNum"] = settingsFromFile["shotNum"]
            self.settings["treeName"] = settingsFromFile["treeName"]
            self.settings["startMdsplusTime"] = settingsFromFile["startMdsplusTime"]
            self.settings["endMdsplusTime"] = settingsFromFile["endMdsplusTime"]
            self.settings["deltaMdsplusTime"] = settingsFromFile["deltaMdsplusTime"]

            self.settings["fs_kHz"] = settingsFromFile["fs_kHz"]
            self.settings["nfft"] = settingsFromFile["nfft"]
            self.settings["window"] = settingsFromFile["window"]
            self.settings["nperseg"] = settingsFromFile["nperseg"]
            self.settings["noverlap"] = settingsFromFile["noverlap"]
            detrend = settingsFromFile["detrend"]
            self.settings["detrend"] = False if detrend.casefold() == 'false' else detrend
            self.settings["scaling"] = settingsFromFile["scaling"]
            self.settings["mode"] = settingsFromFile["mode"]
            self.settings["scaleLinLogSqrt"] = settingsFromFile["scaleLinLogSqrt"]
            self.settings["histoGradient"] = settingsFromFile["histoGradient"]

            self.settings["applyBandPass"] = settingsFromFile["applyBandPass"]
            self.settings["bandpassLowcut_kHz"] = settingsFromFile["bandpassLowcut_kHz"]
            self.settings["bandpassHighcut_kHz"] = settingsFromFile["bandpassHighcut_kHz"]
            self.settings["order"] = settingsFromFile["order"]

            self.settings["applyDownsampling"] = settingsFromFile["applyDownsampling"]
            self.settings["targetFrq_kHz"] = settingsFromFile["targetFrq_kHz"]

            self.settings["setHistogramLevels"] = settingsFromFile["setHistogramLevels"]
            self.settings["histogramLevelMin"] = settingsFromFile["histogramLevelMin"]
            self.settings["histogramLevelMax"] = settingsFromFile["histogramLevelMax"]

            self.settings["saveHistogramColor"] = settingsFromFile["saveHistogramColor"]
            self.settings["exportSpectrogramToImg"] = settingsFromFile["exportSpectrogramToImg"]

        self.putSettingsToUi()

    def setDefaultSettings(self):
        if self.settingsFilePath.is_file():
            self.loadSettingsFromFile()
            self.checkAndApplySettins()
            return
        self.settings = {}

        self.settings["shotNum"]=180906039
        self.settings["treeName"]='qoc'
        self.settings["startMdsplusTime"]='*'
        self.settings["endMdsplusTime"]='*'
        self.settings["deltaMdsplusTime"]='*'

        self.settings["nfft"]=5000
        self.settings["fs_kHz"]=2000
        self.settings["window"]='hamming'
        self.settings["nperseg"]=5000
        self.settings["noverlap"]=4000
        self.settings["detrend"]='constant'
        self.settings["scaling"]='density'
        self.settings["mode"]='psd'
        self.settings["scaleLinLogSqrt"]='sqrt'
        self.settings["histoGradient"]= {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]}

        self.settings["applyBandPass"] = False
        self.settings["bandpassLowcut_kHz"] = 5
        self.settings["bandpassHighcut_kHz"] = 20
        self.settings["order"] = 5

        self.settings["applyDownsampling"] = False
        self.settings["targetFrq_kHz"] = 500

        self.settings["setHistogramLevels"] = False
        self.settings["histogramLevelMin"] = 0
        self.settings["histogramLevelMax"] = 0.01

        self.settings["saveHistogramColor"] = False
        self.settings["exportSpectrogramToImg"] = False




        self.putSettingsToUi()
        self.checkAndApplySettins()
        # return self.settings

    def checkAndApplySettins(self):
        self.settings["shotNum"] = self.settings["shotNum"] if  self.settings["shotNum"] > 100000000 else 180906039
        # self.settings["deltaMdsplusTime"] = self.settings["deltaMdsplusTime"] if  float(self.settings["deltaMdsplusTime"]) > 1 else '*'

        self.settings["fs_kHz"] = self.settings["fs_kHz"] if float(self.settings["fs_kHz"]) > 0 else 1
        self.settings["nfft"] = self.settings["nfft"] if self.settings["nfft"] > 0 else 512
        self.settings["nperseg"] = self.settings["nperseg"] if self.settings["nperseg"] < self.settings["nfft"] else self.settings["nfft"]
        self.settings["noverlap"] = self.settings["noverlap"] if self.settings["noverlap"] < self.settings["nperseg"] else int(0.9*(self.settings["nperseg"]))
        self.settings["targetFrq_kHz"] = self.settings["targetFrq_kHz"] if float(self.settings["targetFrq_kHz"]) < float(self.settings["fs_kHz"]) else self.settings["fs_kHz"]
        self.putSettingsToUi()

        self.callingObj.settings = self.settings


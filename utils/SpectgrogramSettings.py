import sys
from GUIs import spectrogramSettingsLayout
from PyQt5 import QtWidgets
import json
from pathlib import Path


class SpectgrogramSettings(QtWidgets.QMainWindow,spectrogramSettingsLayout.Ui_spectrogramSettingsWidget):

    def __init__(self, callingObj, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.settings = {}
        self.callingObj = callingObj

        self.saveSettings_btn.clicked.connect(self.saveSettingsToJSON)
        self.resetSetings_btn.clicked.connect(self.loadSettingsFromJSON)
        self.setToUiAndClose_btn.clicked.connect(self.setToUiAndClose)
        self.settingsFile = Path("settings/spectrSettings.txt")

    def setToUiAndClose(self):
        self.getFromUi()
        self.checkAndApplySettins()
        self.close()

    def getFromUi(self):
        self.settings["nfft"]=int(self.nfft_ui.text())
        self.settings["fs_kHz"]=float(self.fs_kHz_ui.text())
        self.settings["window"]=self.window_ui.text()
        self.settings["nperseg"]=int(self.nperseg_ui.text())
        self.settings["noverlap"]=int(self.noverlap_ui.text())
        detrend = self.detrend_ui.text()
        self.settings["detrend"]=False if detrend.casefold() =='false' else detrend
        self.settings["scaling"]=self.scaling_ui.text()
        self.settings["mode"]=self.mode_ui.text()
        self.settings["scaleLinLogSqrt"]=self.scaleLinLogSqrt.currentText()

        self.settings["histoGradient"] = self.callingObj.hist.gradient.saveState()

    def saveSettingsToJSON(self):



        self.getFromUi()
        self.checkAndApplySettins()

        with open(self.settingsFile, 'w') as outfile:
            json.dump(self.settings,outfile, indent=4)

        # gradientState = self.callingObj.hist.gradient.saveState()
        # print(gradientState)



        self.close()

    def putSettingsToUi(self):

        self.nfft_ui.setText(str(self.settings["nfft"]))
        self.fs_kHz_ui.setText(str(self.settings["fs_kHz"]))
        self.window_ui.setText(str(self.settings["window"]))
        self.nperseg_ui.setText(str(self.settings["nperseg"]))
        self.noverlap_ui.setText(str(self.settings["noverlap"]))
        self.detrend_ui.setText(str(self.settings["detrend"]))
        self.scaling_ui.setText(str(self.settings["scaling"]))
        self.mode_ui.setText(str(self.settings["mode"]))
        self.scaleLinLogSqrt.setCurrentText(self.settings["scaleLinLogSqrt"])

    def loadSettingsFromJSON(self):

        with open(self.settingsFile) as json_file:
            settingsFromFile = json.load(json_file)
            self.settings["nfft"] = settingsFromFile["nfft"]
            self.settings["fs_kHz"] = settingsFromFile["fs_kHz"]
            self.settings["window"] = settingsFromFile["window"]
            self.settings["nperseg"] = settingsFromFile["nperseg"]
            self.settings["noverlap"] = settingsFromFile["noverlap"]
            detrend = settingsFromFile["detrend"]
            self.settings["detrend"] = False if detrend.casefold() == 'false' else detrend
            self.settings["scaling"] = settingsFromFile["scaling"]
            self.settings["mode"] = settingsFromFile["mode"]
            self.settings["scaleLinLogSqrt"] = settingsFromFile["scaleLinLogSqrt"]
            self.settings["histoGradient"] = settingsFromFile["histoGradient"]


            self.putSettingsToUi()

    def setDefaultSettings(self):
        if self.settingsFile.is_file():
            self.loadSettingsFromJSON()
            self.checkAndApplySettins()
            return
        self.settings = {}
        self.settings["nfft"]=1024
        self.settings["fs_kHz"]=500
        self.settings["window"]='hamming'
        self.settings["nperseg"]=1024
        self.settings["noverlap"]=900
        self.settings["detrend"]='constant'
        self.settings["scaling"]='density'
        self.settings["mode"]='psd'
        self.settings["scaleLinLogSqrt"]='linear'
        self.settings["histoGradient"]= {'mode': 'rgb',
             'ticks': [(0.5, (0, 182, 188, 255)),
                       (1.0, (246, 111, 0, 255)),
                       (0.0, (75, 0, 113, 255))]}

        self.putSettingsToUi()
        self.checkAndApplySettins()
        # return self.settings

    def checkAndApplySettins(self):
        self.settings["nperseg"] = self.settings["nperseg"] if self.settings["nperseg"] < self.settings["nfft"] else self.settings["nfft"]
        self.settings["noverlap"] = self.settings["noverlap"] if self.settings["noverlap"] < self.settings["nperseg"] else int(0.8*(self.settings["nperseg"]))
        self.putSettingsToUi()

        self.callingObj.settings = self.settings


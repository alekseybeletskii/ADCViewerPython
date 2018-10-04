import sys
from GUIs import spectrogramSettingsLayout
from PyQt5 import QtWidgets
import json

class SpectgrogramSettings(QtWidgets.QMainWindow,spectrogramSettingsLayout.Ui_spectrogramSettingsWidget):

    def __init__(self, callingObj, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.settings = {}
        self.callingObj = callingObj

        self.saveSettings_btn.clicked.connect(self.saveParamsToJSON)
        self.resetSetings_btn.clicked.connect(self.loadSettingsFromJSON)


    def saveParamsToJSON(self):

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

        with open('GUIs/spectrParams.txt', 'w') as outfile:
            json.dump(self.settings,outfile, indent=4)

        self.callingObj.settings = self.settings
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

        with open('GUIs/spectrParams.txt') as json_file:
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

            self.putSettingsToUi()

    def setDefaultSettings(self):
        self.settings = {}
        self.settings["nfft"]=1024
        self.settings["fs_kHz"]=500
        self.settings["window"]='hamming'
        self.settings["nperseg"]=self.settings["nfft"]
        self.settings["noverlap"]=900
        self.settings["detrend"]='constant'
        self.settings["scaling"]='density'
        self.settings["mode"]='psd'
        self.settings["scaleLinLogSqrt"]='linear'

        self.putSettingsToUi()

        return self.settings



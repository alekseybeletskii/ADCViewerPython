import sys
from GUIs import w7xPyViewerSettingsLayout
from PyQt5 import QtWidgets, QtGui
import json
from pathlib import Path
from os import path, makedirs



class w7xPyViewerSettings(QtWidgets.QMainWindow, w7xPyViewerSettingsLayout.Ui_w7xPyViewerSettingsWidget):

    def __init__(self, callingObj, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.settings = {}
        self.callingObj = callingObj

        self.here = path.dirname(path.realpath(__file__))
        self.settingsDirName = "settings"
        self.settingsDirPath = path.join(self.here, '..', self.settingsDirName)
        if not path.exists(self.settingsDirPath):
            makedirs(self.settingsDirPath)
        self.settingsFilePath = Path(path.join(self.settingsDirPath,'w7xViewerSettings.txt'))

        self.saveSettings_btn.clicked.connect(self.saveSettingsToFile)
        self.resetSetings_btn.clicked.connect(self.setDefaultSettings)
        self.getFromUiApplyAndClose_btn.clicked.connect(self.getFromUiApplyAndClose)

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
        self.settings["applyDownsampling"] = self.applyDownsampling_ui.checkState()
        self.settings["targetFrq_kHz"]=float(self.targetFrq_kHz_ui.text())
        self.settings["sgFilterWindow"]=int(self.sgFilterWindow_ui.text())
        self.settings["sgFilterPolyOrder"]=int(self.sgFilterPolyOrder_ui.text())


    def putSettingsToUi(self):

        self.shotNum_ui.setText(str(self.settings["shotNum"]))
        self.treeName_ui.setText(str(self.settings["treeName"]))
        self.startMdsplusTime_ui.setText(str(self.settings["startMdsplusTime"]))
        self.endMdsplusTime_ui.setText(str(self.settings["endMdsplusTime"]))
        self.deltaMdsplusTime_ui.setText(str(self.settings["deltaMdsplusTime"]))
        self.applyDownsampling_ui.setCheckState(self.settings["applyDownsampling"])
        self.targetFrq_kHz_ui.setText(str(self.settings["targetFrq_kHz"]))
        self.sgFilterWindow_ui.setText(str(self.settings["sgFilterWindow"]))
        self.sgFilterPolyOrder_ui.setText(str(self.settings["sgFilterPolyOrder"]))


    def loadSettingsFromFile(self):
        with open(self.settingsFilePath) as json_file:
            settingsFromFile = json.load(json_file)
            self.settings["shotNum"] = settingsFromFile["shotNum"]
            self.settings["treeName"] = settingsFromFile["treeName"]
            self.settings["startMdsplusTime"] = settingsFromFile["startMdsplusTime"]
            self.settings["endMdsplusTime"] = settingsFromFile["endMdsplusTime"]
            self.settings["deltaMdsplusTime"] = settingsFromFile["deltaMdsplusTime"]
            self.settings["applyDownsampling"] = settingsFromFile["applyDownsampling"]
            self.settings["targetFrq_kHz"] = settingsFromFile["targetFrq_kHz"]
            self.settings["sgFilterWindow"] = settingsFromFile["sgFilterWindow"]
            self.settings["sgFilterPolyOrder"] = settingsFromFile["sgFilterPolyOrder"]

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
        self.settings["applyDownsampling"]=False
        self.settings["targetFrq_kHz"]=1
        self.settings["sgFilterWindow"]=101
        self.settings["sgFilterPolyOrder"]=1

        self.putSettingsToUi()
        self.checkAndApplySettins()
        # return self.settings

    def checkAndApplySettins(self):
        self.settings["targetFrq_kHz"] = self.settings["targetFrq_kHz"] if float(self.settings["targetFrq_kHz"]) > 0.01 else 1
        self.settings["shotNum"] = self.settings["shotNum"] if  self.settings["shotNum"] > 100000000 else 180906039
        self.settings["sgFilterWindow"] = self.settings["sgFilterWindow"] if  not self.settings["sgFilterWindow"] %2 == 0 else self.settings["sgFilterWindow"] + 1
        # self.settings["deltaMdsplusTime"] = self.settings["deltaMdsplusTime"] if  float(self.settings["deltaMdsplusTime"]) > 1 else '*'

        self.putSettingsToUi()

        self.callingObj.settings = self.settings


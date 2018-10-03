import sys
from GUIs import spectrogramSettingsLayout
from PyQt5 import QtWidgets

class SpectgrogramSettings(QtWidgets.QMainWindow,spectrogramSettingsLayout.Ui_spectrogramSettingsWidget):

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        # self.callingObj = callingObj







# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataModifierLayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dataModifierWidget(object):
    def setupUi(self, dataModifierWidget):
        dataModifierWidget.setObjectName("dataModifierWidget")
        dataModifierWidget.resize(320, 100)
        dataModifierWidget.setMinimumSize(QtCore.QSize(320, 100))
        dataModifierWidget.setMaximumSize(QtCore.QSize(320, 100))
        self.layoutWidget = QtWidgets.QWidget(dataModifierWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 9, 301, 83))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.showSGF_ui = QtWidgets.QCheckBox(self.splitter_2)
        self.showSGF_ui.setObjectName("showSGF_ui")
        self.subtractSGF_ui = QtWidgets.QPushButton(self.splitter_2)
        self.subtractSGF_ui.setObjectName("subtractSGF_ui")
        self.replaceWithSGF_ui = QtWidgets.QPushButton(self.splitter_2)
        self.replaceWithSGF_ui.setObjectName("replaceWithSGF_ui")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.fixADC0_ui = QtWidgets.QPushButton(self.splitter)
        self.fixADC0_ui.setObjectName("fixADC0_ui")
        self.fixADC0start_ui = QtWidgets.QLineEdit(self.splitter)
        self.fixADC0start_ui.setObjectName("fixADC0start_ui")
        self.fixADC0end_ui = QtWidgets.QLineEdit(self.splitter)
        self.fixADC0end_ui.setText("")
        self.fixADC0end_ui.setObjectName("fixADC0end_ui")
        self.verticalLayout.addWidget(self.splitter)
        self.splitter_3 = QtWidgets.QSplitter(self.layoutWidget)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.useModifiers_ui = QtWidgets.QPushButton(self.splitter_3)
        self.useModifiers_ui.setObjectName("useModifiers_ui")
        self.reloadFromSource_ui = QtWidgets.QPushButton(self.splitter_3)
        self.reloadFromSource_ui.setEnabled(False)
        self.reloadFromSource_ui.setStyleSheet("background:blue")
        self.reloadFromSource_ui.setObjectName("reloadFromSource_ui")
        self.verticalLayout.addWidget(self.splitter_3)

        self.retranslateUi(dataModifierWidget)
        QtCore.QMetaObject.connectSlotsByName(dataModifierWidget)

    def retranslateUi(self, dataModifierWidget):
        _translate = QtCore.QCoreApplication.translate
        dataModifierWidget.setWindowTitle(_translate("dataModifierWidget", "dataModifier"))
        self.showSGF_ui.setToolTip(_translate("dataModifierWidget", "show Savitzky-Golay filter"))
        self.showSGF_ui.setText(_translate("dataModifierWidget", "show SGFilter"))
        self.subtractSGF_ui.setToolTip(_translate("dataModifierWidget", "subtract Savitzky-Golay filter"))
        self.subtractSGF_ui.setText(_translate("dataModifierWidget", "-SGFilter"))
        self.replaceWithSGF_ui.setToolTip(_translate("dataModifierWidget", "replace with Savitzky-Golay filter"))
        self.replaceWithSGF_ui.setText(_translate("dataModifierWidget", "=SGFilter"))
        self.fixADC0_ui.setToolTip(_translate("dataModifierWidget", "fix ADC 0 error"))
        self.fixADC0_ui.setText(_translate("dataModifierWidget", "fix ADC 0"))
        self.fixADC0start_ui.setPlaceholderText(_translate("dataModifierWidget", "start, sec"))
        self.fixADC0end_ui.setPlaceholderText(_translate("dataModifierWidget", "end, sec"))
        self.useModifiers_ui.setText(_translate("dataModifierWidget", "use modifiers"))
        self.reloadFromSource_ui.setText(_translate("dataModifierWidget", "reload from source"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dataModifierWidget = QtWidgets.QWidget()
    ui = Ui_dataModifierWidget()
    ui.setupUi(dataModifierWidget)
    dataModifierWidget.show()
    sys.exit(app.exec_())


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'w7xPyViewerLayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_w7xPyViewer(object):
    def setupUi(self, w7xPyViewer):
        w7xPyViewer.setObjectName("w7xPyViewer")
        w7xPyViewer.resize(618, 402)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(w7xPyViewer.sizePolicy().hasHeightForWidth())
        w7xPyViewer.setSizePolicy(sizePolicy)
        w7xPyViewer.setMinimumSize(QtCore.QSize(618, 402))
        self.centralwidget = QtWidgets.QWidget(w7xPyViewer)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(618, 382))
        self.centralwidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(600, 20))
        self.groupBox.setMaximumSize(QtCore.QSize(600, 20))
        self.groupBox.setObjectName("groupBox")
        self.replaceWithSGF = QtWidgets.QPushButton(self.groupBox)
        self.replaceWithSGF.setGeometry(QtCore.QRect(150, 0, 40, 20))
        self.replaceWithSGF.setMinimumSize(QtCore.QSize(40, 20))
        self.replaceWithSGF.setMaximumSize(QtCore.QSize(40, 20))
        self.replaceWithSGF.setObjectName("replaceWithSGF")
        self.drawSpectrogramUI = QtWidgets.QPushButton(self.groupBox)
        self.drawSpectrogramUI.setGeometry(QtCore.QRect(2, 0, 50, 20))
        self.drawSpectrogramUI.setMinimumSize(QtCore.QSize(50, 20))
        self.drawSpectrogramUI.setMaximumSize(QtCore.QSize(50, 20))
        self.drawSpectrogramUI.setObjectName("drawSpectrogramUI")
        self.subtractSGF = QtWidgets.QPushButton(self.groupBox)
        self.subtractSGF.setGeometry(QtCore.QRect(110, 0, 40, 20))
        self.subtractSGF.setMinimumSize(QtCore.QSize(40, 20))
        self.subtractSGF.setMaximumSize(QtCore.QSize(40, 20))
        self.subtractSGF.setObjectName("subtractSGF")
        self.applySGF = QtWidgets.QCheckBox(self.groupBox)
        self.applySGF.setGeometry(QtCore.QRect(60, 0, 50, 20))
        self.applySGF.setMinimumSize(QtCore.QSize(50, 20))
        self.applySGF.setMaximumSize(QtCore.QSize(50, 20))
        self.applySGF.setObjectName("applySGF")
        self.mouseXY_UI = QtWidgets.QLabel(self.groupBox)
        self.mouseXY_UI.setGeometry(QtCore.QRect(280, 0, 250, 20))
        self.mouseXY_UI.setMinimumSize(QtCore.QSize(250, 20))
        self.mouseXY_UI.setMaximumSize(QtCore.QSize(250, 20))
        self.mouseXY_UI.setObjectName("mouseXY_UI")
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainPlotWidget = PlotWidget(self.centralwidget)
        self.mainPlotWidget.setBaseSize(QtCore.QSize(0, 0))
        self.mainPlotWidget.setObjectName("mainPlotWidget")
        self.horizontalLayout.addWidget(self.mainPlotWidget)
        self.listOfDataLablesWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listOfDataLablesWidget.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listOfDataLablesWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listOfDataLablesWidget.setObjectName("listOfDataLablesWidget")
        self.horizontalLayout.addWidget(self.listOfDataLablesWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        w7xPyViewer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(w7xPyViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        w7xPyViewer.setMenuBar(self.menubar)
        self.actionClear = QtWidgets.QAction(w7xPyViewer)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtWidgets.QAction(w7xPyViewer)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(w7xPyViewer)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExport_to_csv = QtWidgets.QAction(w7xPyViewer)
        self.actionExport_to_csv.setObjectName("actionExport_to_csv")
        self.actionOpen_mdsplus = QtWidgets.QAction(w7xPyViewer)
        self.actionOpen_mdsplus.setObjectName("actionOpen_mdsplus")
        self.actionCheckUncheckAll = QtWidgets.QAction(w7xPyViewer)
        self.actionCheckUncheckAll.setObjectName("actionCheckUncheckAll")
        self.actionExport_time_to_separate_file = QtWidgets.QAction(w7xPyViewer)
        self.actionExport_time_to_separate_file.setObjectName("actionExport_time_to_separate_file")
        self.actionOpen_csv = QtWidgets.QAction(w7xPyViewer)
        self.actionOpen_csv.setObjectName("actionOpen_csv")
        self.actionOpen_Source = QtWidgets.QAction(w7xPyViewer)
        self.actionOpen_Source.setObjectName("actionOpen_Source")
        self.actionSettings = QtWidgets.QAction(w7xPyViewer)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addAction(self.actionOpen_Source)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_time_to_separate_file)
        self.menuFile.addAction(self.actionExport_to_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(w7xPyViewer)
        QtCore.QMetaObject.connectSlotsByName(w7xPyViewer)

    def retranslateUi(self, w7xPyViewer):
        _translate = QtCore.QCoreApplication.translate
        w7xPyViewer.setWindowTitle(_translate("w7xPyViewer", "w7xPyViewer"))
        self.replaceWithSGF.setToolTip(_translate("w7xPyViewer", "replace with Savitzky-Golay filter"))
        self.replaceWithSGF.setText(_translate("w7xPyViewer", "=SGF"))
        self.drawSpectrogramUI.setText(_translate("w7xPyViewer", "spectr"))
        self.subtractSGF.setToolTip(_translate("w7xPyViewer", "subtract Savitzky-Golay filter"))
        self.subtractSGF.setText(_translate("w7xPyViewer", "-SGF"))
        self.applySGF.setToolTip(_translate("w7xPyViewer", "show Savitzky-Golay filter"))
        self.applySGF.setText(_translate("w7xPyViewer", "SGF"))
        self.mouseXY_UI.setText(_translate("w7xPyViewer", "mouse X, Y"))
        self.menuFile.setTitle(_translate("w7xPyViewer", "Data"))
        self.actionClear.setText(_translate("w7xPyViewer", "Clear"))
        self.actionExit.setText(_translate("w7xPyViewer", "Exit"))
        self.actionAbout.setText(_translate("w7xPyViewer", "about"))
        self.actionExport_to_csv.setText(_translate("w7xPyViewer", "Export to csv"))
        self.actionOpen_mdsplus.setText(_translate("w7xPyViewer", "Open_mdsplus"))
        self.actionCheckUncheckAll.setText(_translate("w7xPyViewer", "(Un)Check all"))
        self.actionExport_time_to_separate_file.setText(_translate("w7xPyViewer", "Export to csv (time separate)"))
        self.actionOpen_csv.setText(_translate("w7xPyViewer", "Open_csv"))
        self.actionOpen_csv.setToolTip(_translate("w7xPyViewer", "store full first column as X"))
        self.actionOpen_Source.setText(_translate("w7xPyViewer", "Open Source (Shift+o)"))
        self.actionSettings.setText(_translate("w7xPyViewer", "Settings (Shift+s)"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w7xPyViewer = QtWidgets.QMainWindow()
    ui = Ui_w7xPyViewer()
    ui.setupUi(w7xPyViewer)
    w7xPyViewer.show()
    sys.exit(app.exec_())


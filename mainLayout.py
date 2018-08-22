# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainLayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 667)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.timeScale = QtWidgets.QLineEdit(self.centralwidget)
        self.timeScale.setMinimumSize(QtCore.QSize(0, 0))
        self.timeScale.setMaximumSize(QtCore.QSize(200, 15))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timeScale.setFont(font)
        self.timeScale.setPlaceholderText("")
        self.timeScale.setObjectName("timeScale")
        self.verticalLayout_3.addWidget(self.timeScale)
        self.plot = PlotWidget(self.centralwidget)
        self.plot.setBaseSize(QtCore.QSize(0, 0))
        self.plot.setObjectName("plot")
        self.verticalLayout_3.addWidget(self.plot)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_csv = QtWidgets.QAction(MainWindow)
        self.actionOpen_csv.setObjectName("actionOpen_csv")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExport_to_csv = QtWidgets.QAction(MainWindow)
        self.actionExport_to_csv.setObjectName("actionExport_to_csv")
        self.actionDrawPlotsFromCsv = QtWidgets.QAction(MainWindow)
        self.actionDrawPlotsFromCsv.setObjectName("actionDrawPlotsFromCsv")
        self.actionOpen_mdsplus = QtWidgets.QAction(MainWindow)
        self.actionOpen_mdsplus.setObjectName("actionOpen_mdsplus")
        self.actionDrawPlotsFromMdsplus = QtWidgets.QAction(MainWindow)
        self.actionDrawPlotsFromMdsplus.setObjectName("actionDrawPlotsFromMdsplus")
        self.actionExport_time_to_separate_file = QtWidgets.QAction(MainWindow)
        self.actionExport_time_to_separate_file.setObjectName("actionExport_time_to_separate_file")
        self.menuFile.addAction(self.actionOpen_mdsplus)
        self.menuFile.addAction(self.actionDrawPlotsFromMdsplus)
        self.menuFile.addAction(self.actionExport_time_to_separate_file)
        self.menuFile.addAction(self.actionExport_to_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_csv)
        self.menuFile.addAction(self.actionDrawPlotsFromCsv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_csv.setText(_translate("MainWindow", "Open_csv"))
        self.actionClear.setText(_translate("MainWindow", "ClearPlots"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "about"))
        self.actionExport_to_csv.setText(_translate("MainWindow", "Export_to_csv"))
        self.actionDrawPlotsFromCsv.setText(_translate("MainWindow", "DrawPlotsFromCsv"))
        self.actionOpen_mdsplus.setText(_translate("MainWindow", "Open_mdsplus"))
        self.actionDrawPlotsFromMdsplus.setText(_translate("MainWindow", "DrawPlotsFromMdsplus"))
        self.actionExport_time_to_separate_file.setText(_translate("MainWindow", "Export time to separate file"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


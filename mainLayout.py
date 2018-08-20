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
        MainWindow.resize(857, 667)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.plot = PlotWidget(self.splitter)
        self.plot.setBaseSize(QtCore.QSize(0, 0))
        self.plot.setObjectName("plot")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 857, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        self.menuFile.addAction(self.actionOpen_csv)
        self.menuFile.addAction(self.actionDrawPlotsFromCsv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_mdsplus)
        self.menuFile.addAction(self.actionDrawPlotsFromMdsplus)
        self.menuFile.addAction(self.actionExport_to_csv)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addAction(self.actionExit)
        self.menu.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menu.setTitle(_translate("MainWindow", "?"))
        self.actionOpen_csv.setText(_translate("MainWindow", "Open_csv"))
        self.actionClear.setText(_translate("MainWindow", "ClearPlots"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "about"))
        self.actionExport_to_csv.setText(_translate("MainWindow", "Export_to_csv"))
        self.actionDrawPlotsFromCsv.setText(_translate("MainWindow", "DrawPlotsFromCsv"))
        self.actionOpen_mdsplus.setText(_translate("MainWindow", "Open_mdsplus"))
        self.actionDrawPlotsFromMdsplus.setText(_translate("MainWindow", "DrawPlotsFromMdsplus"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


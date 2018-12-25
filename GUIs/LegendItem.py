from PyQt5 import QtCore
from PyQt5.QtCore import Qt
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QWidget, QPushButton, QCheckBox


class LegendItem(QWidget):

    def __init__(self, plotter, itemIndex=0, isChecked=True, itemTextValue='newCurve', curveColor=Qt.black):
        super(self.__class__, self).__init__()
        self.initSelf(plotter, itemIndex, isChecked, itemTextValue, curveColor)

    def initSelf(self, plotter, itemIndex, isChecked, itemTextValue, curveColor):
        # spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.plotter = plotter

        self.itemIndex = itemIndex
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        # self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.itemCheckbox = QCheckBox(self)
        self.itemCheckbox.setChecked(isChecked)
        self.itemCheckbox.setObjectName('itemCheckbox')
        self.itemCheckbox.setFixedSize(QtCore.QSize(15, 15))

        self.itemCheckbox.clicked.connect(lambda: self.setCurveVisible(self.itemCheckbox))

        self.itemText = QLabel(self)
        self.itemText.setObjectName("itemText")
        self.itemText.setText(itemTextValue)

        self.itemColorPicker = QLabel(self)
        self.itemColorPicker.setObjectName("itemColorPicker")
        self.itemColorPicker.setFixedSize(QtCore.QSize(15, 15))
        self.itemColorPicker.setStyleSheet(f'background-color: {curveColor}')
        self.itemColorPicker.mousePressEvent = self.setNewColor

        self.horizontalLayout.addWidget(self.itemCheckbox)
        self.horizontalLayout.addWidget(self.itemColorPicker)
        self.horizontalLayout.addWidget(self.itemText)

    def setCurveVisible(self, itemCheckbox):
        isChecked = True if itemCheckbox.checkState() == Qt.Checked else False
        self.plotter.setCurveVisibility(self.itemIndex, isChecked)

    def setNewColor(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.itemColorPicker.setStyleSheet(f'background-color: {color.name()}')
            self.itemCheckbox.setChecked(True)
            self.plotter.setCurveColor(self.itemIndex, color)

    def setItemTextValue(self, curveName):
        self.itemText.setText(curveName)

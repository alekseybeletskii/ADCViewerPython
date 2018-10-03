import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsWidget, QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, QVBoxLayout, QWidget


class SliderWidget(QWidget, QGraphicsWidget):
    def __init__(self, minimum, maximum, parent=None):
        super(SliderWidget, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setMaximumWidth(80)

        self.resize(self.sizeHint())

        self.setSliderMaxMin(maximum, minimum)

    def setSliderMaxMin(self, max, min):
        self.scaledMaximum = max
        self.scaledMinimum = min
        self.slider.valueChanged.connect(self.setLabelValue)
        self.sliderScaledValue = None
        self.setLabelValue(self.slider.value())
        

    def setLabelValue(self, value):
        self.sliderScaledValue = self.scaledMinimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
        self.scaledMaximum - self.scaledMinimum)
        self.label.setText("{0:.1e}".format(self.sliderScaledValue))

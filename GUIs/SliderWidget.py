from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, QVBoxLayout, QWidget, QPushButton


class SliderWidget(QWidget):
    def __init__(self, minimum, maximum, parent=None):
        super(SliderWidget, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalSliderLayout")
        self.label = QLabel(self)
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalSliderLayout")
        spacerItem = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)
        spacerItem1 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addItem(self.horizontalLayout)

        self.appendPeaks_btn = QPushButton(self)
        self.appendPeaks_btn.setText('+')
        self.appendPeaks_btn.setToolTip("add to all peaks")
        self.appendPeaks_btn.setMaximumSize(15, 15)
        self.removePeaks_btn = QPushButton(self)
        self.removePeaks_btn.setText('x')
        self.removePeaks_btn.setToolTip('erase peaks')
        self.removePeaks_btn.setMaximumSize(15, 15)
        self.drawAllPeaks_btn = QPushButton(self)
        self.drawAllPeaks_btn.setText('d')
        self.drawAllPeaks_btn.setToolTip('draw all peaks')
        self.drawAllPeaks_btn.setMaximumSize(15, 15)
        self.saveAllPeaks_btn = QPushButton(self)
        self.saveAllPeaks_btn.setText('s')
        self.saveAllPeaks_btn.setToolTip('save all peaks')
        self.saveAllPeaks_btn.setMaximumSize(15, 15)
        self.horizontalLayoutBtn = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalSliderLayoutBtn")
        self.horizontalLayoutBtn.addWidget(self.appendPeaks_btn)
        self.horizontalLayoutBtn.addWidget(self.drawAllPeaks_btn)
        self.horizontalLayoutBtn.addWidget(self.removePeaks_btn)
        self.horizontalLayoutBtn.addWidget(self.saveAllPeaks_btn)
        self.verticalLayout.addItem(self.horizontalLayoutBtn)





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

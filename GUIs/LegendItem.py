# /*
#  * ******************** BEGIN LICENSE BLOCK *********************************
#  *
#  * w7x-PyViewer
#  * Copyright (c) 2017 onward, Aleksey Beletskii  <beletskiial@gmail.com>
#  * All rights reserved
#  *
#  * github: https://github.com/alekseybeletskii
#  *
#  * The w7x-PyViewer software serves for visualization and simple processing
#  * of any data recorded with Analog Digital Converters in binary or text form.
#  *
#  * Commercial support is available. To find out more contact the author directly.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions are met:
#  *
#  *     1. Redistributions of source code must retain the above copyright notice, this
#  *          list of conditions and the following disclaimer.
#  *     2. Redistributions in binary form must reproduce the above copyright notice,
#  *         this list of conditions and the following disclaimer in the documentation
#  *         and/or other materials provided with the distribution.
#  *
#  * The software is distributed to You under terms of the GNU General Public
#  * License. This means it is "free software". However, any program, using
#  * w7x-PyViewer _MUST_ be the "free software" as well.
#  * See the GNU General Public License for more details
#  * (file ./COPYING in the root of the distribution
#  * or website <http://www.gnu.org/licenses/>)
#  *
#  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  *
#  * ******************** END LICENSE BLOCK ***********************************
#  */
#


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
            # self.itemCheckbox.setChecked(True)
            self.plotter.setCurveColor(self.itemIndex, color)

    def setItemTextValue(self, curveName):
        self.itemText.setText(curveName)

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


from GUIs import dataModifierLayout
from PyQt5 import QtWidgets, QtGui
import json
from pathlib import Path
from os import path, makedirs
from utils.DataFilters import DataFilters




class DataModifier(QtWidgets.QMainWindow, dataModifierLayout.Ui_dataModifierWidget):

    def __init__(self,  parent):
        super(self.__class__, self).__init__(parent)

        self.setupUi(self)
        self.mainObject = parent
        self.dataModifiers = {}

        self.here = path.dirname(path.realpath(__file__))
        self.settingsDirName = "settings"
        self.settingsDirPath = path.join(self.here, '..', self.settingsDirName)
        if not path.exists(self.settingsDirPath):
            makedirs(self.settingsDirPath)
        self.dataModifiersFilePath = Path(path.join(self.settingsDirPath,'dataModifiers.txt'))

        self.useModifiers_ui.clicked.connect(self.useModifiers)
        self.subtractSGF_ui.clicked.connect(self.subtractSGFilter)
        self.replaceWithSGF_ui.clicked.connect(self.replaceWithSGFilter)
        self.fixADC0_ui.clicked.connect(self.fixADC0)
        self.showSGF_ui.clicked.connect(self.mainObject.drawPlots)

        self.hotkey = {}
        self.ui_hotkey('closeDataModifier', "Return", self.close)

    def ui_hotkey(self, key_name, key_combo, func):
        self.hotkey[key_name] = QtWidgets.QShortcut(QtGui.QKeySequence(key_combo), self)
        self.hotkey[key_name].activated.connect(func)

    def useModifiers(self):
        if self.dataModifiersFilePath.is_file():
            self.loadDataModifiersFromFile()
            self.checkAndApply()
            return
        self.createDefaultModifiersFile()


    def createDefaultModifiersFile(self):
        self.dataModifiers = {}
        for data in self.mainObject.allData:
            # self.dataModifiers[data.getLabel()] = {'timeshift':0.0, 'datamultiplier':1.0, 'datashift':0.0, 'independentvar':0.0, 'datatype':'whatever'}
            self.dataModifiers[data.getLabel()] = data.getDataModifiers()
        with open(self.dataModifiersFilePath, 'w') as outfile:
            json.dump(self.dataModifiers, outfile, indent=4)


    def loadDataModifiersFromFile(self):
        with open(self.dataModifiersFilePath) as json_file:
            dataModifiersFromFile = json.load(json_file)
            self.dataModifiers = dataModifiersFromFile

    def checkAndApply(self):
        # print(json.dumps(self.dataModifiers, indent=4))
        # for label in self.dataModifiers:
        #     print(label)
        for data in self.mainObject.allData:
            if data.getLabel() in self.dataModifiers:
                data.setDataModifiers(self.dataModifiers[data.getLabel()])
                data.applyDataModifiers()


        

    def subtractSGFilter(self):

        xyFilt = DataFilters(self.mainObject)
        xyFilt.subtractSGFilter()
        xyFilt = None

    def replaceWithSGFilter(self):
        xyFilt = DataFilters(self.mainObject)
        xyFilt.replaceWithSGFilter()
        xyFilt = None

    def fixADC0(self):
        for data in self.mainObject.allData:
            try:
                start = float(self.fixADC0start_ui.text())
                end = float(self.fixADC0end_ui.text())
            except :
                start = end = 0

            data.compensateAdcZeroShift(start, end)





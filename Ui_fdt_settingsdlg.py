# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fdt_settingsdlg.ui'
#
# Created: Mon Jul 15 16:24:47 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        """

        :param SettingsDialog:
        """
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(320, 429)
        SettingsDialog.setMinimumSize(QtCore.QSize(320, 320))
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setContentsMargins(0, 6, 0, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(SettingsDialog)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 308, 371))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setMargin(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridsLabel = QtGui.QLabel(self.groupBox)
        self.gridsLabel.setObjectName(_fromUtf8("gridsLabel"))
        self.gridLayout.addWidget(self.gridsLabel, 1, 0, 1, 1)
        self.pinsLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pinsLabel.sizePolicy().hasHeightForWidth())
        self.pinsLabel.setSizePolicy(sizePolicy)
        self.pinsLabel.setObjectName(_fromUtf8("pinsLabel"))
        self.gridLayout.addWidget(self.pinsLabel, 0, 0, 1, 1)
        self.pinsCmbBx = QtGui.QComboBox(self.groupBox)
        self.pinsCmbBx.setObjectName(_fromUtf8("pinsCmbBx"))
        self.gridLayout.addWidget(self.pinsCmbBx, 0, 1, 1, 1)
        self.featuresLabel = QtGui.QLabel(self.groupBox)
        self.featuresLabel.setObjectName(_fromUtf8("featuresLabel"))
        self.gridLayout.addWidget(self.featuresLabel, 2, 0, 1, 1)
        self.gridsCmbBx = QtGui.QComboBox(self.groupBox)
        self.gridsCmbBx.setStyleSheet(_fromUtf8(""))
        self.gridsCmbBx.setObjectName(_fromUtf8("gridsCmbBx"))
        self.gridLayout.addWidget(self.gridsCmbBx, 1, 1, 1, 1)
        self.featuresCmbBx = QtGui.QComboBox(self.groupBox)
        self.featuresCmbBx.setObjectName(_fromUtf8("featuresCmbBx"))
        self.gridLayout.addWidget(self.featuresCmbBx, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.squaresGrpBx = QgsCollapsibleGroupBox(self.scrollAreaWidgetContents)
        self.squaresGrpBx.setObjectName(_fromUtf8("squaresGrpBx"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.squaresGrpBx)
        self.verticalLayout_5.setMargin(6)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_3 = QtGui.QLabel(self.squaresGrpBx)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridMajorLabel = QtGui.QLabel(self.squaresGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridMajorLabel.sizePolicy().hasHeightForWidth())
        self.gridMajorLabel.setSizePolicy(sizePolicy)
        self.gridMajorLabel.setText(_fromUtf8(""))
        self.gridMajorLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/grid-major.svg")))
        self.gridMajorLabel.setObjectName(_fromUtf8("gridMajorLabel"))
        self.gridLayout_6.addWidget(self.gridMajorLabel, 1, 0, 1, 1)
        self.gridsMinorLabel = QtGui.QLabel(self.squaresGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridsMinorLabel.sizePolicy().hasHeightForWidth())
        self.gridsMinorLabel.setSizePolicy(sizePolicy)
        self.gridsMinorLabel.setText(_fromUtf8(""))
        self.gridsMinorLabel.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/fossildigtools/icons/grid-minor.svg")))
        self.gridsMinorLabel.setObjectName(_fromUtf8("gridsMinorLabel"))
        self.gridLayout_6.addWidget(self.gridsMinorLabel, 2, 0, 1, 1)
        self.gridsMinorSpnBx = QtGui.QSpinBox(self.squaresGrpBx)
        self.gridsMinorSpnBx.setMaximum(999)
        self.gridsMinorSpnBx.setObjectName(_fromUtf8("gridsMinorSpnBx"))
        self.gridLayout_6.addWidget(self.gridsMinorSpnBx, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.squaresGrpBx)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_6.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridsUnitCmdBx = QtGui.QComboBox(self.squaresGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridsUnitCmdBx.sizePolicy().hasHeightForWidth())
        self.gridsUnitCmdBx.setSizePolicy(sizePolicy)
        self.gridsUnitCmdBx.setObjectName(_fromUtf8("gridsUnitCmdBx"))
        self.gridsUnitCmdBx.addItem(_fromUtf8(""))
        self.gridsUnitCmdBx.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.gridsUnitCmdBx, 0, 1, 1, 1)
        self.gridsMajorSpnBx = QtGui.QSpinBox(self.squaresGrpBx)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridsMajorSpnBx.sizePolicy().hasHeightForWidth())
        self.gridsMajorSpnBx.setSizePolicy(sizePolicy)
        self.gridsMajorSpnBx.setStyleSheet(_fromUtf8(""))
        self.gridsMajorSpnBx.setMaximum(999)
        self.gridsMajorSpnBx.setObjectName(_fromUtf8("gridsMajorSpnBx"))
        self.gridLayout_6.addWidget(self.gridsMajorSpnBx, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_6)
        self.label = QtGui.QLabel(self.squaresGrpBx)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.squaresGrpBx)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)
        SettingsDialog.setTabOrder(self.gridsUnitCmdBx, self.gridsMajorSpnBx)
        SettingsDialog.setTabOrder(self.gridsMajorSpnBx, self.gridsMinorSpnBx)
        SettingsDialog.setTabOrder(self.gridsMinorSpnBx, self.scrollArea)
        SettingsDialog.setTabOrder(self.scrollArea, self.buttonBox)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings", None))
        self.groupBox.setTitle(_translate("SettingsDialog", "Map layers", None))
        self.gridsLabel.setText(_translate("SettingsDialog", "Grids", None))
        self.pinsLabel.setText(_translate("SettingsDialog", "Pins", None))
        self.featuresLabel.setText(_translate("SettingsDialog", "Features", None))
        self.squaresGrpBx.setTitle(_translate("SettingsDialog", "Grid squares", None))
        self.label_3.setText(_translate("SettingsDialog", "Major and minor grids must be set, with major grid divisible by minor. ", None))
        self.label_2.setText(_translate("SettingsDialog", "Units", None))
        self.gridsUnitCmdBx.setItemText(0, _translate("SettingsDialog", "cm", None))
        self.gridsUnitCmdBx.setItemText(1, _translate("SettingsDialog", "in", None))
        self.label.setText(_translate("SettingsDialog", "Note: Changing grid size later will require deletion of existing grids.", None))

from qgis.gui import QgsCollapsibleGroupBox
import resources_rc

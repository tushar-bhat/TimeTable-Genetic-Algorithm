# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result2.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(875, 559)
        Dialog.setMinimumSize(QtCore.QSize(875, 559))
        Dialog.setMaximumSize(QtCore.QSize(875, 559))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cmbChromosome = QtWidgets.QComboBox(self.groupBox_3)
        self.cmbChromosome.setObjectName("cmbChromosome")
        self.cmbChromosome.addItem("")
        self.cmbChromosome.addItem("")
        self.cmbChromosome.addItem("")
        self.cmbChromosome.addItem("")
        self.cmbChromosome.addItem("")
        self.verticalLayout_4.addWidget(self.cmbChromosome)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cmbCategory = QtWidgets.QComboBox(self.groupBox)
        self.cmbCategory.setObjectName("cmbCategory")
        self.cmbCategory.addItem("")
        self.cmbCategory.addItem("")
        self.cmbCategory.addItem("")
        self.verticalLayout_3.addWidget(self.cmbCategory)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cmbEntry = QtWidgets.QComboBox(self.groupBox_2)
        self.cmbEntry.setObjectName("cmbEntry")
        self.verticalLayout_2.addWidget(self.cmbEntry)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox_6 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnExport = QtWidgets.QPushButton(self.groupBox_6)
        self.btnExport.setObjectName("btnExport")
        self.horizontalLayout_3.addWidget(self.btnExport)
        self.horizontalLayout.addWidget(self.groupBox_6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblFit = QtWidgets.QLabel(self.groupBox_4)
        self.lblFit.setObjectName("lblFit")
        self.verticalLayout_5.addWidget(self.lblFit)
        self.lblSbj = QtWidgets.QLabel(self.groupBox_4)
        self.lblSbj.setObjectName("lblSbj")
        self.verticalLayout_5.addWidget(self.lblSbj)
        self.lblSecRest = QtWidgets.QLabel(self.groupBox_4)
        self.lblSecRest.setObjectName("lblSecRest")
        self.verticalLayout_5.addWidget(self.lblSecRest)
        self.lblSecIdle = QtWidgets.QLabel(self.groupBox_4)
        self.lblSecIdle.setObjectName("lblSecIdle")
        self.verticalLayout_5.addWidget(self.lblSecIdle)
        self.lblInstrRest = QtWidgets.QLabel(self.groupBox_4)
        self.lblInstrRest.setObjectName("lblInstrRest")
        self.verticalLayout_5.addWidget(self.lblInstrRest)
        self.lblInstrLoad = QtWidgets.QLabel(self.groupBox_4)
        self.lblInstrLoad.setObjectName("lblInstrLoad")
        self.verticalLayout_5.addWidget(self.lblInstrLoad)
        self.lblLunch = QtWidgets.QLabel(self.groupBox_4)
        self.lblLunch.setObjectName("lblLunch")
        self.verticalLayout_5.addWidget(self.lblLunch)
        self.lblMeet = QtWidgets.QLabel(self.groupBox_4)
        self.lblMeet.setObjectName("lblMeet")
        self.verticalLayout_5.addWidget(self.lblMeet)
        self.verticalLayout_7.addWidget(self.groupBox_4)
        self.groupProblems = QtWidgets.QGroupBox(Dialog)
        self.groupProblems.setObjectName("groupProblems")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupProblems)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblTime = QtWidgets.QLabel(self.groupProblems)
        self.lblTime.setObjectName("lblTime")
        self.verticalLayout_6.addWidget(self.lblTime)
        self.lblCPU = QtWidgets.QLabel(self.groupProblems)
        self.lblCPU.setObjectName("lblCPU")
        self.verticalLayout_6.addWidget(self.lblCPU)
        self.lblMemory = QtWidgets.QLabel(self.groupProblems)
        self.lblMemory.setObjectName("lblMemory")
        self.verticalLayout_6.addWidget(self.lblMemory)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.verticalLayout_7.addWidget(self.groupProblems)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.tableResult = QtWidgets.QTableView(Dialog)
        self.tableResult.setMinimumSize(QtCore.QSize(698, 300))
        self.tableResult.setMaximumSize(QtCore.QSize(698, 3000))
        self.tableResult.setObjectName("tableResult")
        self.horizontalLayout_4.addWidget(self.tableResult)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Result Viewer"))
        self.groupBox_3.setTitle(_translate("Dialog", "Chromosome"))
        self.cmbChromosome.setItemText(0, _translate("Dialog", "Chromosome 1"))
        self.cmbChromosome.setItemText(1, _translate("Dialog", "Chromosome 2"))
        self.cmbChromosome.setItemText(2, _translate("Dialog", "Chromosome 3"))
        self.cmbChromosome.setItemText(3, _translate("Dialog", "Chromosome 4"))
        self.cmbChromosome.setItemText(4, _translate("Dialog", "Chromosome 5"))
        self.groupBox.setTitle(_translate("Dialog", "Category"))
        self.cmbCategory.setItemText(0, _translate("Dialog", "Section"))
        self.cmbCategory.setItemText(1, _translate("Dialog", "Room"))
        self.cmbCategory.setItemText(2, _translate("Dialog", "Instructor"))
        self.groupBox_2.setTitle(_translate("Dialog", "Entry"))
        self.groupBox_6.setTitle(_translate("Dialog", "Operation"))
        self.btnExport.setText(_translate("Dialog", "Export Result"))
        self.groupBox_4.setTitle(_translate("Dialog", "Chromosome Details"))
        self.lblFit.setText(_translate("Dialog", "Total Fitness:"))
        self.lblSbj.setText(_translate("Dialog", "Subject Placement: "))
        self.lblSecRest.setText(_translate("Dialog", "Section Rest: "))
        self.lblSecIdle.setText(_translate("Dialog", "Section Idle Time:"))
        self.lblInstrRest.setText(_translate("Dialog", "Instructor Rest: "))
        self.lblInstrLoad.setText(_translate("Dialog", "Instructor Load:"))
        self.lblLunch.setText(_translate("Dialog", "Lunch Break:"))
        self.lblMeet.setText(_translate("Dialog", "Meeting Pattern: "))
        self.groupProblems.setTitle(_translate("Dialog", "System Message"))
        self.lblTime.setText(_translate("Dialog", "Generation Time:"))
        self.lblCPU.setText(_translate("Dialog", "Average CPU Usage:"))
        self.lblMemory.setText(_translate("Dialog", "Average Mem Usage:"))


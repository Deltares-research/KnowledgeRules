# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewpage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import view_edit_tool_API
from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append("../../scripting_library/")
import autecology_xml


class UI_MainWindow(object):
	

	def setupUI(self, MainWindow):

		#start build up
		self.MainWindow = MainWindow

		self.MainWindow.setObjectName("MainWindow")
		self.MainWindow.resize(1121, 806)
		self.MainWindow.setMinimumSize(1121, 806)

		#See: https://stackoverflow.com/questions/16771894/python-nameerror-global-name-file-is-not-defined
		if getattr(sys, 'frozen', False):
			# The application is frozen
			self.path = os.path.realpath(sys.executable)
		else:
			# The application is not frozen
			# Change this bit to match where you store your data files:
			self.path = os.path.realpath(__file__)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)

		self.mainlayout = QtWidgets.QGridLayout(self.MainWindow)

		#Top button groupbox (box not shown)
		self.groupBox_1 = QtWidgets.QGroupBox()
		self.groupBox_1.setGeometry(QtCore.QRect(10, 5, 1081, 35))
		self.groupBox_1.setObjectName("groupBox")
		self.groupBox_1.setFlat(True)
		self.boxlayout_1 = QtWidgets.QHBoxLayout(self.groupBox_1)
		self.mainlayout.addWidget(self.groupBox_1)

		self.pushButton = QtWidgets.QPushButton()
		self.pushButton.setGeometry(QtCore.QRect(20, 10, 93, 28))
		self.pushButton.setFixedSize(93, 28)
		self.pushButton.setObjectName("pushButton")
		self.pushButton.clicked.connect(self.load_file)
		self.boxlayout_1.addWidget(self.pushButton)

		self.pushButton_2 = QtWidgets.QPushButton()
		self.pushButton_2.setGeometry(QtCore.QRect(120, 10, 93, 28))
		self.pushButton_2.setFixedSize(93, 28)
		self.pushButton_2.setObjectName("pushButton_2")
		self.pushButton_2.clicked.connect(self.new_file)
		self.boxlayout_1.addWidget(self.pushButton_2)

		self.pushButton_3 = QtWidgets.QPushButton()
		self.pushButton_3.setGeometry(QtCore.QRect(220, 10, 93, 28))
		self.pushButton_3.setFixedSize(93, 28)
		self.pushButton_3.setObjectName("pushButton_3")
		self.pushButton_3.clicked.connect(self.save_file)
		self.boxlayout_1.addWidget(self.pushButton_3)

		self.spacer_1 = QtWidgets.QSpacerItem(780, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.boxlayout_1.addSpacerItem(self.spacer_1)

		self.pushButton_4 = QtWidgets.QPushButton()
		self.pushButton_4.setGeometry(QtCore.QRect(1000, 10, 93, 28))
		self.pushButton_4.setFixedSize(93, 28)
		self.pushButton_4.setObjectName("pushButton_4")
		self.pushButton_4.clicked.connect(self.quit)
		self.boxlayout_1.addWidget(self.pushButton_4)

		#Lower information groupbox
		self.groupBox_2 = QtWidgets.QGroupBox()
		self.groupBox_2.setGeometry(QtCore.QRect(10, 50, 1081, 751))
		self.groupBox_2.setObjectName("groupBox")
		self.boxlayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
		self.mainlayout.addWidget(self.groupBox_2)

		self.scrollLayout = QtWidgets.QVBoxLayout()
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setLayout(self.scrollLayout)
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1079, 749))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		self.scrollArea = QtWidgets.QScrollArea()
		self.scrollArea.setGeometry(QtCore.QRect(10, 50, 1081, 751))
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.boxlayout_2.addWidget(self.scrollArea)

		
		self.label = QtWidgets.QLabel()
		self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.scrollLayout.addWidget(self.label)
		
		self.textBrowser = QtWidgets.QTextBrowser()
		self.textBrowser.setObjectName("textBrowser")
		self.textBrowser.setFixedSize(1030, 31)
		self.scrollLayout.addWidget(self.textBrowser)
		
		self.label_2 = QtWidgets.QLabel()
		self.label_2.setGeometry(QtCore.QRect(10, 90, 151, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		self.scrollLayout.addWidget(self.label_2)
		
		self.comboBox = QtWidgets.QComboBox()
		self.comboBox.setGeometry(QtCore.QRect(10, 110, 900, 22))
		self.comboBox.setObjectName("comboBox")
		self.scrollLayout.addWidget(self.comboBox)

		self.label_3 = QtWidgets.QLabel()
		self.label_3.setGeometry(QtCore.QRect(10, 150, 151, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_3.setFont(font)
		self.label_3.setObjectName("label_3")
		self.scrollLayout.addWidget(self.label_3)

		self.textBrowser_2 = QtWidgets.QTextBrowser()
		self.textBrowser_2.setGeometry(QtCore.QRect(10, 180, 900, 221))
		self.textBrowser_2.setObjectName("textBrowser_2")
		self.textBrowser_2.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.scrollLayout.addWidget(self.textBrowser_2)

		self.label_4 = QtWidgets.QLabel()
		self.label_4.setGeometry(QtCore.QRect(10, 420, 211, 21))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setObjectName("label_4")
		self.scrollLayout.addWidget(self.label_4)

		self.label_5 = QtWidgets.QLabel()
		self.label_5.setGeometry(QtCore.QRect(10, 450, 161, 16))
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setUnderline(True)
		self.label_5.setFont(font)
		self.label_5.setObjectName("label_5")
		self.scrollLayout.addWidget(self.label_5)

		self.comboBox_2 = QtWidgets.QComboBox()
		self.comboBox_2.setGeometry(QtCore.QRect(10, 480, 900, 22))
		self.comboBox_2.setObjectName("comboBox_2")
		self.scrollLayout.addWidget(self.comboBox_2)
		
		self.groupBox = QtWidgets.QGroupBox()
		self.groupBox.setGeometry(QtCore.QRect(10, 510, 900, 231))
		self.groupBox.setObjectName("groupBox")
		self.boxlayout = QtWidgets.QGridLayout(self.groupBox)
		self.scrollLayout.addWidget(self.groupBox)


		self.comboBox_3 = QtWidgets.QComboBox()
		self.comboBox_3.setGeometry(QtCore.QRect(0, 0, 100, 22))
		self.comboBox_3.setObjectName("comboBox_3")


		self.system_scrolllayout = QtWidgets.QVBoxLayout()		
		self.system_scrollwidget = QtWidgets.QWidget()
		self.system_scrollwidget.setLayout(self.system_scrolllayout)
		self.system_scroll = QtWidgets.QScrollArea()
		self.system_scroll.setWidgetResizable(True)
		self.system_scroll.setWidget(self.system_scrollwidget)
		self.boxlayout.addWidget(self.system_scroll)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)



	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton.setText(_translate("MainWindow", "Open"))
		self.pushButton_2.setText(_translate("MainWindow", "New"))
		self.pushButton_3.setText(_translate("MainWindow", "Save"))
		self.pushButton_4.setText(_translate("MainWindow", "Exit"))
		self.label.setText(_translate("MainWindow", "Subject"))
		self.label_2.setText(_translate("MainWindow", "Common name"))
		self.label_3.setText(_translate("MainWindow", "Description"))
		self.label_4.setText(_translate("MainWindow", "Dose-effect relations"))
		self.label_5.setText(_translate("MainWindow", "system selection"))
		self.groupBox.setTitle(_translate("MainWindow", "system : "))


	def load_file(self):

		#reset connections
		try:
			self.comboBox.currentIndexChanged.disconnect()
		except:
			pass

		try:
			self.comboBox_2.currentIndexChanged.disconnect()
		except:
			pass

		try:
			self.comboBox_3.currentIndexChanged.disconnect()
		except:
			pass


		#reset
		self.systemname = None
		self.systems = None
		self.cur_language = None
		self.cur_flowdiagram = None
		
		#load objects
		objAPI = view_edit_tool_API.API()
		AutXML = autecology_xml.AutecologyXML(None)	

		#load and refresh data
		self = objAPI.load_file(self)
		if(hasattr(self,"xmlroot")):
			(self, AutXML) = objAPI.refresh_data(self, AutXML)

			#set connections
			self.comboBox.currentIndexChanged.connect(lambda: objAPI.refresh_language(self, self.cur_language))
			self.comboBox_2.currentIndexChanged.connect(lambda: objAPI.refresh_group_data(self, AutXML, self.modeltypename, self.systemname, self.groupBox))
			self.comboBox_3.currentIndexChanged.connect(lambda: objAPI.refresh_flowdiagram(self, AutXML, self.modeltypename, self.systemname, self.cur_flowdiagram))

		return()

	def new_file(self):
		objAPI = view_edit_tool_API.API()
		objAPI.new_file(self)
		return()

	def save_file(self):
		objAPI = view_edit_tool_API.API()
		objAPI.save_file(self)
		return()

	def quit(self):
		objAPI = view_edit_tool_API.API()
		objAPI.quit(self)
		return()

	def refresh_data(self):
		objAPI = view_edit_tool_API.API()
		objAPI.refresh_data(self)
		return()		

	def refresh_group_data(self, cur_window):
		objAPI = view_edit_tool_API.API()
		objAPI.refresh_group_data(self,cur_window)
		return()		

class UI_StartWindow(object):

	def setupUI(self, StartWindow):
		
		self.StartWindow = StartWindow

		self.StartWindow.setObjectName("StartWindow")
		self.StartWindow.resize(1122, 700)

		#See: https://stackoverflow.com/questions/16771894/python-nameerror-global-name-file-is-not-defined
		if getattr(sys, 'frozen', False):
			# The application is frozen
			self.path = os.path.realpath(sys.executable)
		else:
			# The application is not frozen
			# Change this bit to match where you store your data files:
			self.path = os.path.realpath(__file__)

		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)

		self.groupBox = QtWidgets.QGroupBox(self.StartWindow)
		self.groupBox.setGeometry(QtCore.QRect(10, 10, 1102, 690))
		self.groupBox.setObjectName("groupBox")
		self.boxlayout = QtWidgets.QGridLayout(self.groupBox)


		self.label = QtWidgets.QLabel()
		self.label.setGeometry(QtCore.QRect(290, 20, 501, 61))
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setTextFormat(QtCore.Qt.AutoText)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.boxlayout.addWidget(self.label)
		self.label_2 = QtWidgets.QLabel()
		self.label_2.setGeometry(QtCore.QRect(290, 70, 501, 61))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(False)
		font.setWeight(50)
		self.label_2.setFont(font)
		self.label_2.setTextFormat(QtCore.Qt.AutoText)
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.label_2.setObjectName("label_2")
		self.boxlayout.addWidget(self.label_2)
		self.label_3 = QtWidgets.QLabel()
		self.label_3.setGeometry(QtCore.QRect(290, 110, 501, 61))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(False)
		font.setWeight(50)
		self.label_3.setFont(font)
		self.label_3.setTextFormat(QtCore.Qt.AutoText)
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName("label_3")
		self.boxlayout.addWidget(self.label_3)
		self.graphicsView = QtWidgets.QGraphicsView()
		self.graphicsView.setGeometry(QtCore.QRect(130, 170, 841, 421))
		self.graphicsView.setObjectName("graphicsView")
		self.boxlayout.addWidget(self.graphicsView)
		self.label_4 = QtWidgets.QLabel()
		self.label_4.setGeometry(QtCore.QRect(160, 600, 781, 16))
		self.label_4.setObjectName("label_4")
		self.boxlayout.addWidget(self.label_4)
		self.label_5 = QtWidgets.QLabel()
		self.label_5.setGeometry(QtCore.QRect(160, 620, 781, 16))
		self.label_5.setObjectName("label_5")
		self.boxlayout.addWidget(self.label_5)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self.StartWindow)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.StartWindow.setWindowTitle(_translate("StartWindow", "Dialog"))
		self.label.setText(_translate("StartWindow", "Autecology"))
		self.label_2.setText(_translate("StartWindow", "Data storage"))
		self.label_3.setText(_translate("StartWindow", "View & editting data tool"))
		self.label_4.setText(_translate("StartWindow", "© Stichting Deltares , this tool and the data fall under the GNU General Public License v3.0."))
		self.label_5.setText(_translate("StartWindow", "Please contact the original author of the tool M.P. Weeber if any questions arrises (marc.weeber at deltares.nl)"))


class UI_Application(object):

	def start_up(self):
		#needed to start the screens
		self.StartUp = QtWidgets.QDialog()
		self.StartUp.show()
	
	def run_startwindow(self):
		self.ui_startwindow= UI_StartWindow()
		self.StartWindow = QtWidgets.QDialog()
		self.ui_startwindow.setupUI(self.StartWindow)
		self.StartWindow.show()

	def run_mainwindow(self):
		self.StartWindow.close()
		self.ui_mainwindow= UI_MainWindow()
		self.MainWindow = QtWidgets.QDialog()
		self.MainWindow.setMinimumSize(1121, 806)
		flags = QtCore.Qt.WindowFlags()
		flags |= QtCore.Qt.Window
		flags |= QtCore.Qt.CustomizeWindowHint
		flags |= QtCore.Qt.WindowTitleHint
		flags |= QtCore.Qt.WindowMinimizeButtonHint
		flags |= QtCore.Qt.WindowMaximizeButtonHint
		flags |= QtCore.Qt.WindowCloseButtonHint
		self.MainWindow.setWindowFlags(flags)
		self.ui_mainwindow.setupUI(self.MainWindow)
		self.MainWindow.show()


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)

	#Start Window
	ui = UI_Application()
	ui.start_up()
	QtCore.QTimer.singleShot(0,ui.run_startwindow)
	QtCore.QTimer.singleShot(3000, ui.run_mainwindow)
	
	sys.exit(app.exec_())


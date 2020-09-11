'''
API
Autecology : View and edit tool

autor: Weeber
'''


import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
#import xml.etree.ElementTree as ET
#from xml.etree.ElementTree import ElementTree
from lxml import etree as ET
import autecology_xml
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import random
import sip


# # from PyQtWebEngine import QtWebEngineWidgets
from PyQt5 import QtWebEngineWidgets

class API:

	def clearLayout(self,cur_layout):
		def deleteItems(cur_layout):
			if cur_layout is not None:
				while cur_layout.count():
					item = cur_layout.takeAt(0)
					widget = item.widget()
					if widget is not None:
						widget.deleteLater()
					else:
						deleteItems(item.layout())
		deleteItems(cur_layout)

	def load_file(self, obj):
		qfd = QtWidgets.QFileDialog()
		(name, file_type) = QtWidgets.QFileDialog.getOpenFileName(qfd, 'Open File', obj.path, "XML files (*.xml)")
		try:
			root = ET.parse(name).getroot()
			obj.xmlroot = root
		except:
			print("No file loaded")
			pass
		return(obj)

	def new_file(self, obj):
		#TO BE DEVELOPED
		return()

	def save_file(self, obj):
		qfd = QtWidgets.QFileDialog()
		(name, file_type) = QtWidgets.QFileDialog.getSaveFileName(qfd, 'Save File', "","XML files (*.xml)")
		try:
			xmlfile = open(name,'w')
			tree = ET(obj.xmlroot)
			tree.write(xmlfile, encoding='unicode')
			xmlfile.close()
		except:
			print("No file saved")
			pass

	def quit(self, obj):
		sys.exit()


	def refresh_language(self, obj, override):
		'''
		Reload with a change of language
		'''
		
		#don't do anything when override is none
		if(override == None):
			return()

		#get value from combobox
		comboxvalue = obj.MainWindow.findChild(QtWidgets.QComboBox,obj.MainWindow.sender().objectName()).currentText()

		#combobox strip output
		name, cur_language = comboxvalue.split(" | ")
		obj.cur_language = cur_language
		
		#replace content information
		cur_contenttext = [td["description"] for td in obj.topicdescription if(td["language"] == obj.cur_language)][0]
		obj.textBrowser_2.setText(cur_contenttext)
		obj.textBrowser_2.setFixedHeight(obj.textBrowser_2.document().size().height() +\
			obj.textBrowser_2.contentsMargins().top() + obj.textBrowser_2.contentsMargins().bottom())

		#replace system information
		cur_systemtext = [syd["description"] for syd in obj.systemdescription if(syd["language"] == obj.cur_language)][0]
		obj.system_textBrowser.setText(cur_systemtext)
		obj.system_textBrowser.setFixedHeight(obj.system_textBrowser.document().size().height() +\
			obj.system_textBrowser.contentsMargins().top() + obj.system_textBrowser.contentsMargins().bottom())
		
		return()

	def refresh_flowdiagram(self, obj, xml_obj, modeltypename, systemname, override):
		'''
		Reload with a change of flow diagram
		'''

		#dont on anyting when overrride is none
		if(override == None):
			return()

		#get value from combobox
		comboboxvalue = obj.MainWindow.findChild(QtWidgets.QComboBox, obj.MainWindow.sender().objectName()).currentText()

		#delete widget
		obj.system_groupbox_1_layout.removeWidget(obj.fd_subframe_ready)
		sip.delete(obj.fd_subframe_ready)

		#retrieve flowdiagram
		fd_data = xml_obj._read_systemflowdiagram(modeltypename, systemname, comboboxvalue)
		fd_svg = xml_obj.create_flowdiagram_image(fd_data, output = None)
		fd_subframe = xml_obj.visualize_flowdiagram_image(fd_svg)

		obj.fd_subframe_ready = fd_subframe()

		#replace flow diagram image
		# self.clearLayout(obj.system_groupbox_1_layout)
		# obj.system_groupbox_1_layout = QtWidgets.QGridLayout()
		# obj.system_groupbox_1_layout.addWidget(obj.comboBox_3)
		obj.system_groupbox_1_layout.addWidget(obj.fd_subframe_ready)
		obj.fd_subframe_ready.update()
		obj.fd_subframe_ready.repaint()

		return()


	def refresh_data(self, obj, AutXML):
		'''
		Load a new data file
		'''

		#Default
		obj.cur_modeltype = "HSI"


		#reset
		obj.systemdescription = None

		#Set data
		AutXML.xmlroot = obj.xmlroot
		AutXML._scan()
		AutXML._scan_modeltype(obj.cur_modeltype)
		
		obj.systems = AutXML.systems
		
		if(AutXML.topic_name == AutXML.XMLconvention["topic_species"]):
			#get names
			obj.topic_name = AutXML.topic_name + " : " + AutXML.latinname
			obj.commonnames = AutXML.commonnames
			obj.subjectlink = AutXML.EoL_Link
		
		elif(AutXML.topic_name == AutXML.XMLconvention["topic_wfdind"]):
			#get names
			obj.topic_name = AutXML.topic_name
			obj.commonnames = AutXML.commonnames
			obj.subjectlink = None
		elif(AutXML.topic_name == AutXML.XMLconvention["topic_habitats"]):
			#get names
			obj.topic_name = AutXML.topic_name
			obj.commonnames = AutXML.commonnames
			obj.subjectlink = None

		else:
			raise ValueError("The topic '" + AutXML.topic_name + "'has not yet been enabled in the viewer.")

		#clear old items
		obj.comboBox.clear() 
		obj.comboBox_2.clear()
		obj.comboBox_3.clear() 

		#retrieve data
		obj.topicdescription = AutXML._read_topicdescription()

		#place topic name
		obj.textBrowser.setText(obj.topic_name)
		obj.textBrowser.setFixedWidth(1000)

		# obj.textBrowser_2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
		for nr, cn in enumerate(obj.commonnames):
			if(nr == 0):
				obj.cur_language = cn["language"]
			obj.comboBox.addItem(cn["name"] + " | " + cn["language"])

		for system in obj.systems:
			obj.comboBox_2.addItem(system)

		#place content information
		print(obj.cur_language)
		cur_contenttext = [td["description"] for td in obj.topicdescription if(td["language"] == obj.cur_language)][0]
		obj.textBrowser_2.setText(cur_contenttext)
		obj.textBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
		obj.textBrowser_2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		obj.textBrowser_2.setMinimumWidth(1000)
		obj.textBrowser_2.setAttribute(103)
		obj.textBrowser_2.show()
		obj.textBrowser_2.setFixedHeight(obj.textBrowser_2.document().size().height() +\
		obj.textBrowser_2.contentsMargins().top() + obj.textBrowser_2.contentsMargins().bottom())


		#update data
		obj.textBrowser.update()
		obj.comboBox.update()
		obj.textBrowser_2.update()
		obj.comboBox_2.update()

		#first setup
		modeltype = obj.cur_modeltype
		system = obj.systems[0]
		obj, AutXML = self.refresh_group_data(obj, AutXML, modeltype, system, obj.groupBox)

		return(obj, AutXML)

	def refresh_group_data(self, obj, xml_obj, modeltype, system, cur_window):
		'''
		Load system related data

		'''

		#clear previous layout
		self.clearLayout(obj.boxlayout)

		#set font
		font = QtGui.QFont()
		font.setPointSize(10)
		font.setBold(True)
		font.setWeight(75)
		_translate = QtCore.QCoreApplication.translate

		#Get system data (based on initialisation or change by combobox)
		if(hasattr(obj.MainWindow,"sender")):
			if(obj.MainWindow.sender().objectName() == "comboBox_2"):
				if(system == None):
					#connection called on initialisation
					return()
				else:
					#overwrite system with the indicated value
					system = obj.MainWindow.findChild(QtWidgets.QComboBox,obj.MainWindow.sender().objectName()).currentText()

		#get system data
		print("Topic :" + xml_obj.topic_name)
		print("System : " + system)
		
		xml_obj._scan_system(modeltype, system)

		obj.modeltypename = xml_obj.modeltypename
		obj.systemname = xml_obj.systemname
		obj.systemdescription = xml_obj._read_systemdescription(modeltype, system)


		#Make system description
		_translate = QtCore.QCoreApplication.translate
		system_label_1 = QtWidgets.QLabel(cur_window)
		system_label_1.setFont(font)
		system_label_1.setObjectName("label")
		system_label_1.setText(_translate("MainWindow", "System description:"))

		obj.system_textBrowser = QtWidgets.QTextBrowser(obj.scrollAreaWidgetContents)
		obj.system_textBrowser.setReadOnly(True)
		obj.system_textBrowser.setObjectName("textBrowser_2")
		
		cur_systemtext = [syd["description"] for syd in obj.systemdescription if(syd["language"] == obj.cur_language)][0]
		obj.system_textBrowser.setText(cur_systemtext)
		obj.system_textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
		obj.system_textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
		obj.system_textBrowser.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		obj.system_textBrowser.setFixedWidth(1000)
		obj.system_textBrowser.setAttribute(103)
		obj.system_textBrowser.show()
		obj.system_textBrowser.setFixedHeight(obj.system_textBrowser.document().size().height() +\
			obj.system_textBrowser.contentsMargins().top() + obj.system_textBrowser.contentsMargins().bottom())

		#Make system framework
		system_label_2 = QtWidgets.QLabel(cur_window)
		system_label_2.setFont(font)
		system_label_2.setObjectName("label")
		system_label_2.setText(_translate("MainWindow", "System flow diagram:"))

		obj.system_groupbox_1 = QtWidgets.QGroupBox(obj.scrollAreaWidgetContents)
		obj.system_groupbox_1.setGeometry(QtCore.QRect(0, 0, 1000, 211))
		obj.system_groupbox_1.setObjectName("flow diagram")
		obj.system_groupbox_1_layout = QtWidgets.QGridLayout()

		for fdname in xml_obj.flowdiagrams:
			obj.comboBox_3.addItem(fdname)

		obj.cur_flowdiagram = xml_obj.flowdiagrams[0]

		fd_data = xml_obj._read_systemflowdiagram(modeltype, system, obj.cur_flowdiagram)
		fd_svg = xml_obj.create_flowdiagram_image(fd_data, output = None)
		fd_subframe = xml_obj.visualize_flowdiagram_image(fd_svg)
		obj.fd_subframe_ready = fd_subframe()
		obj.fd_subframe_ready.repaint()
		obj.system_groupbox_1_layout.addWidget(obj.comboBox_3)
		obj.system_groupbox_1_layout.addWidget(obj.fd_subframe_ready)
		obj.system_groupbox_1.setLayout(obj.system_groupbox_1_layout)


		system_label_3 = QtWidgets.QLabel(cur_window)
		system_label_3.setFont(font)
		system_label_3.setObjectName("label")
		system_label_3.setText(_translate("MainWindow", "Knowledge rules:"))

		#Get number of knowledge rules and knowledge rule names
		obj.knowledgerulenr = xml_obj.knowledgeRulesNr
		obj.knowledgerulecat = xml_obj.knowledgeRulesCategories
		obj.knowledgerulenames = xml_obj.knowledgeRulesNames
		
		obj.boxlayout.addWidget(system_label_1)
		obj.boxlayout.addWidget(obj.system_textBrowser)
		obj.boxlayout.addWidget(system_label_2)
		obj.boxlayout.addWidget(obj.system_groupbox_1)
		obj.boxlayout.addWidget(system_label_3)

		#Loop over knowledge rules and produce plot and info
		obj.groupboxes = []
		for i, kr in enumerate(obj.knowledgerulenames):
			
			print(kr)

			#Implement a progress bar:
			kr_groupbox = QtWidgets.QGroupBox('kr_groupbox%i' % i)
			kr_groupboxlayout = QtWidgets.QGridLayout()
			
			font = QtGui.QFont()
			font.setPointSize(10)
			font.setBold(True)
			font.setWeight(75)

			kr_label1 = QtWidgets.QLabel('kr_label1_%i' % i)
			kr_label1.setFont(font)
			kr_label1.setObjectName("label")
			kr_label1.setText(_translate("MainWindow", kr))

			kr_groupboxlayout.addWidget(kr_label1)

			#Do different actions based on type of knowledge rule
			if(obj.knowledgerulecat[i] == xml_obj.XMLconvention["rc"]):

				rc_pixmap_widget = QtWidgets.QWidget(kr_groupbox)
				rc_pixmap_layout = QtWidgets.QVBoxLayout(rc_pixmap_widget)
				rc_tag = xml_obj.get_element_response_curve(modeltypename = modeltype, systemname = system, rcname = kr)
				rc_data = xml_obj.get_data_response_curve_data(rc_tag)		
				rc_fig, rc_axes = xml_obj.visualize_rc(rc_data)

				kr_groupbox._static_canvas = FigureCanvas(rc_fig)
				rc_pixmap_layout.addWidget(kr_groupbox._static_canvas)
				kr_groupbox._static_canvas.draw()
				rc_pixmap_widget.setFixedWidth(600)
				rc_pixmap_widget.setFixedHeight(600)

				kr_groupboxlayout.addWidget(rc_pixmap_widget)


			elif(obj.knowledgerulecat[i] == xml_obj.XMLconvention["fb"]):
				
				fb_tag = xml_obj.get_element_formula_based(modeltypename = modeltype, systemname = system, fbname = kr)
				fb_data = xml_obj.get_data_formula_based_data(fb_tag)
				fb_settings, fb_list = xml_obj.make_fb_first_parametersettings(fb_data)
				fb_result = xml_obj.calculate_fb(fb_data, parametersettings = fb_settings, variableparameter = fb_list)
				fb_subframe = xml_obj.visualize_fb_dynamic(fb_data,fb_result)

				
				fb_groupbox = QtWidgets.QGroupBox()
				fb_groupbox_layout = QtWidgets.QGridLayout()
				fb_subframe_ready = fb_subframe()
				fb_subframe_ready.show()
				fb_groupbox_layout.addWidget(fb_subframe_ready)
				fb_groupbox.setLayout(fb_groupbox_layout)

				#add descriptions
				font = QtGui.QFont()
				font.setPointSize(10)
				font.setUnderline(True)
				
				kr_label1 = QtWidgets.QLabel('kr_label1_%i' % i)
				kr_label1.setFont(font)
				kr_label1.setObjectName("label")
				kr_label1.setText(_translate("MainWindow", "Equation:"))

				kr_textBrowser_eq = QtWidgets.QTextBrowser()
				kr_textBrowser_eq.setReadOnly(True)
				kr_textBrowser_eq.setObjectName('kr_eqtext_%i' % i)
				kr_textBrowser_eq.setText(fb_data["equation_text"])
				kr_textBrowser_eq.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
				kr_textBrowser_eq.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
				kr_textBrowser_eq.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
				kr_textBrowser_eq.setFixedWidth(600)
				kr_textBrowser_eq.setFixedHeight(33)
				kr_textBrowser_eq.setAttribute(103)
				kr_textBrowser_eq.show()
				kr_textBrowser_eq.setFixedHeight(kr_textBrowser_eq.document().size().height() +\
					kr_textBrowser_eq.contentsMargins().top() + kr_textBrowser_eq.contentsMargins().bottom())


				kr_groupboxlayout.addWidget(fb_groupbox)
				kr_groupboxlayout.addWidget(kr_label1)
				kr_groupboxlayout.addWidget(kr_textBrowser_eq)


			elif(obj.knowledgerulecat[i] == xml_obj.XMLconvention["mr"]):

				mr_tag = xml_obj.get_element_multiple_reclassification(modeltypename = modeltype, systemname = system, mrname = kr)
				mr_data = xml_obj.get_data_multiple_reclassification_data(mr_tag)
				mr_dataframe, mr_headers = xml_obj.make_mr_dataframe(mr_data)
				mr_subframe = xml_obj.visualize_mr_table(mr_dataframe,mr_headers)

				
				mr_groupbox = QtWidgets.QGroupBox()
				mr_groupbox_layout = QtWidgets.QGridLayout()
				mr_subframe_ready = mr_subframe()
				mr_subframe_ready.show()
				mr_groupbox_layout.addWidget(mr_subframe_ready)
				mr_groupbox.setLayout(mr_groupbox_layout)
				mr_groupbox.setFixedHeight(mr_subframe_ready.size().height() +\
					mr_subframe_ready.contentsMargins().top() + mr_subframe_ready.contentsMargins().bottom())

				kr_groupboxlayout.addWidget(mr_groupbox)

				#TO BE CORRECTED AND FINISHED

			else:
				raise ValueError("type of knowledge rule not supported : " + str(obj.knowledgerulecat[i]))

			#add descriptions
			font = QtGui.QFont()
			font.setPointSize(10)
			font.setUnderline(True)

			kr_label2 = QtWidgets.QLabel('kr_label2_%i' % i)
			kr_label2.setFont(font)
			kr_label2.setObjectName("label")
			kr_label2.setText(_translate("MainWindow", "Statistics:"))
			
			kr_textBrowser_1 = QtWidgets.QTextBrowser()
			kr_textBrowser_1.setReadOnly(True)
			kr_textBrowser_1.setObjectName('kr_stattext_%i' % i)
			kr_textBrowser_1.setText(xml_obj.knowledgeRulesOutputStatistics[i][0])
			kr_textBrowser_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
			kr_textBrowser_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
			kr_textBrowser_1.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
			kr_textBrowser_1.setFixedWidth(600)
			kr_textBrowser_1.setFixedHeight(33)
			kr_textBrowser_1.setAttribute(103)
			kr_textBrowser_1.show()
			kr_textBrowser_1.setFixedHeight(kr_textBrowser_1.document().size().height() +\
				kr_textBrowser_1.contentsMargins().top() + kr_textBrowser_1.contentsMargins().bottom())

			kr_label3 = QtWidgets.QLabel('kr_label3_%i' % i)
			kr_label3.setFont(font)
			kr_label3.setObjectName("label")
			kr_label3.setText(_translate("MainWindow", "Units:"))

			kr_textBrowser_2 = QtWidgets.QTextBrowser()
			kr_textBrowser_2.setReadOnly(True)
			kr_textBrowser_2.setObjectName('kr_unittext_%i' % i)
			kr_textBrowser_2.setText(xml_obj.knowledgeRulesOutputUnits[i][0])
			kr_textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
			kr_textBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
			kr_textBrowser_2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
			kr_textBrowser_2.setFixedWidth(600)
			kr_textBrowser_2.setFixedHeight(33)
			kr_textBrowser_2.setAttribute(103)
			kr_textBrowser_2.show()
			kr_textBrowser_2.setFixedHeight(kr_textBrowser_2.document().size().height() +\
				kr_textBrowser_2.contentsMargins().top() + kr_textBrowser_2.contentsMargins().bottom())

			kr_groupboxlayout.addWidget(kr_label2)
			kr_groupboxlayout.addWidget(kr_textBrowser_1)
			kr_groupboxlayout.addWidget(kr_label3)
			kr_groupboxlayout.addWidget(kr_textBrowser_2)
			
			#add everything to the layout	
			kr_groupbox.setLayout(kr_groupboxlayout)
			obj.boxlayout.addWidget(kr_groupbox)
			
		return(obj, xml_obj)




		# # a figure instance to plot on
		# self.figure = plt.figure()

		# # this is the Canvas Widget that displays the `figure`
		# # it takes the `figure` instance as a parameter to __init__
		# self.canvas = FigureCanvas(self.figure)



		# #test
		# obj.test_label_1 = QtWidgets.QLabel(cur_window)
		# obj.test_label_1.setFont(font)
		# obj.test_label_1.setObjectName("label")
		# obj.test_label_2 = QtWidgets.QLabel(cur_window)
		# obj.test_label_2.setFont(font)
		# obj.test_label_2.setObjectName("label")
		# obj.test_label_3 = QtWidgets.QLabel(cur_window)
		# obj.test_label_3.setFont(font)
		# obj.test_label_3.setObjectName("label")
		# obj.test_label_4 = QtWidgets.QLabel(cur_window)
		# obj.test_label_4.setFont(font)
		# obj.test_label_4.setObjectName("label")
		# obj.test_label_6 = QtWidgets.QLabel(cur_window)
		# obj.test_label_6.setFont(font)
		# obj.test_label_6.setObjectName("label")
		# obj.test_label_7 = QtWidgets.QLabel(cur_window)
		# obj.test_label_7.setFont(font)
		# obj.test_label_7.setObjectName("label")
		# obj.test_label_8 = QtWidgets.QLabel(cur_window)
		# obj.test_label_8.setFont(font)
		# obj.test_label_8.setObjectName("label")
		# obj.test_label_9 = QtWidgets.QLabel(cur_window)
		# obj.test_label_9.setFont(font)
		# obj.test_label_9.setObjectName("label")
		# obj.test_combo_box_1 = QtWidgets.QComboBox(cur_window)
		# obj.test_combo_box_1.setGeometry(QtCore.QRect(10, 110, 761, 22))
		# obj.test_combo_box_1.setObjectName("comboBox")
		# obj.test_push_button_1 = QtWidgets.QPushButton(cur_window)
		# obj.test_push_button_1.setGeometry(QtCore.QRect(1000, 10, 93, 28))
		# obj.test_push_button_1.setObjectName("pushButton")
		# obj.test_combo_box_2 = QtWidgets.QComboBox(cur_window)
		# obj.test_combo_box_1.setGeometry(QtCore.QRect(10, 110, 761, 22))
		# obj.test_combo_box_1.setObjectName("comboBox")
		# obj.test_push_button_2 = QtWidgets.QPushButton(cur_window)
		# obj.test_push_button_2.setGeometry(QtCore.QRect(1000, 10, 93, 28))
		# obj.test_push_button_2.setObjectName("pushButton")
		
		# obj.test_line_edit_1 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_1.resize(200, 32)
		# obj.test_line_edit_2 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_2.resize(200, 32)
		# obj.test_line_edit_3 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_3.resize(200, 32)
		# obj.test_line_edit_4 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_4.resize(200, 32)
		# obj.test_line_edit_5 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_5.resize(200, 32)
		# obj.test_line_edit_6 = QtWidgets.QLineEdit(cur_window)
		# obj.test_line_edit_6.resize(200, 32)

		# obj.test_check_box_1 = QtWidgets.QCheckBox("check",cur_window)
		# obj.test_check_box_1.resize(320,40)
		# obj.test_check_box_2 = QtWidgets.QCheckBox("check",cur_window)
		# obj.test_check_box_2.resize(320,40)
		# obj.test_check_box_3 = QtWidgets.QCheckBox("check",cur_window)
		# obj.test_check_box_3.resize(320,40)

		# grid = QtWidgets.QGridLayout()

		# grid.addWidget(obj.test_label_1, 3, 0)
		# grid.addWidget(obj.test_label_2, 3, 2)
		# grid.addWidget(obj.test_label_3, 0, 0)
		# grid.addWidget(obj.test_label_4, 1, 0)
		# grid.addWidget(obj.test_label_6, 2, 0)
		# grid.addWidget(obj.test_label_7, 3, 4)
		# grid.addWidget(obj.test_label_8, 3, 6)
		# grid.addWidget(obj.test_label_9, 3, 8)

		# grid.addWidget(obj.test_line_edit_1, 0, 1, 1, 9)

		# obj.test_push_button_1.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
		# hlay1 = QtWidgets.QHBoxLayout()
		# hlay1.addWidget(obj.test_combo_box_1)		
		# hlay1.addWidget(obj.test_push_button_1)
		# grid.addLayout(hlay1, 1, 1, 1, 9)

		# obj.test_push_button_2.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
		# hlay2 = QtWidgets.QHBoxLayout()
		# hlay2.addWidget(obj.test_combo_box_2)
		# hlay2.addWidget(obj.test_push_button_2)
		# grid.addLayout(hlay2, 2, 1, 1, 9)

		# grid.addWidget(obj.test_line_edit_2, 3, 1)
		# grid.addWidget(obj.test_line_edit_3, 3, 3)
		# grid.addWidget(obj.test_line_edit_4, 3, 5)
		# grid.addWidget(obj.test_line_edit_5, 3, 7)
		# grid.addWidget(obj.test_line_edit_6, 3, 9)

		# grid.addWidget(obj.test_check_box_1, 0, 10)
		# grid.addWidget(obj.test_check_box_2, 1, 10)
		# grid.addWidget(obj.test_check_box_3, 2, 10)

		# obj.groupBox.setLayout(grid)
		# obj.groupBox.update()

		# return ()
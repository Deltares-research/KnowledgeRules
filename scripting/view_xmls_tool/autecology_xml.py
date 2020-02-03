'''
Autecology XML Python Toolbox
'''

import sys
import os
import copy
from lxml.etree import _Element as Element
from lxml import etree as ET
import pandas
import numpy as np
from asteval import Interpreter
from collections import OrderedDict

#static plots
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#interactive plots
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt5_visualization import LabeledSlider

#testing
import unittest

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------

class _File(object):
	"""
	Copyright to "d3d.py" library by Christophe Thiange (Deltares)

	Base class.

	f = _File("dir/subdir/root.ext)

	f.fullname  = "dir/subdir/root.ext"
	f.path	  = "dir/subdir"
	f.name	  = "root.ext"
	f.name_root = "root"
	f.name_ext  = "ext"
	"""

	def __init__(self, filename=None):
		self._fullname = filename
		self.path	  = None
		self.name	  = None
		self.name_root = None
		self.name_ext  = None
		if self.fullname is not None:
			self._fileinfo()

	@property
	def fullname(self):
		return self._fullname

	@fullname.setter
	def fullname(self, fullname):
		self.__init__(fullname)

	def _fileinfo(self):
		"""
		Set file info.
		"""
		if os.sep in self.fullname:
			s = self.fullname.split(os.sep)
			self.path = os.sep.join(s[:-1])
			self.name  = s[-1]
		else:
			self.path = "."
			self.name = self._fullname
		if '.' in self.name:
			s = self.name.split('.')
			self.name_root = '.'.join(s[:-1])
			self.name_ext  = s[ -1]
		else:
			self.name_root = self.name
			self.name_ext  = ''

	def dump(self, fileout=None):
		"""
		Dump file contents to csv.

		Only available if implemented in child classes.
		If filout is None, output file will be filename.dmp.
		"""
		raise NotImplementedError('This type of file cannot be dumped.')

class AutecologyXML(_File):

	def make_find(self, element_name_list):
		full_string = ""
		stop_slash = len(element_name_list)-1
		for nr, i in enumerate(element_name_list):
			full_string = full_string + self.xmlns +  i
			if(nr != stop_slash):
				full_string = full_string + "/"
			else:
				pass
		return(full_string)

	def __init__(self, filename):
		_File.__init__(self,filename)
		self.xmlroot = None
		self.xmlns = "http://www.wldelft.nl/fews"

		#scan
		self.topic_name = None
		self.EoL_ID = None
		self.EoL_Link = None 
		self.latinname = None
		self.commonnames = None
		self.modeltypes = None

		#scan_modeltype
		self.systems = None

		#scan_system
		self.systemname = None
		self.spatial_scope = None
		self.temporal_scope = None
		self.geonames_names = None 
		self.geonames_ids = None
		self.geonames_links = None
		self.StartDate = None
		self.EndDate = None
		self.knowledgeRulesNr = None
		self.knowledgeRulesCategorie = None
		self.knowledgeRulesDict = None
		self.knowledgeRulesStatistics = None
		self.knowledgeRulesUnits = None

		#XML build up
		self.XMLlayers = {}
		self.XMLlayers["layer1"] = "AutecologyXML"
		self.XMLlayers["layer1_1"] = "Topic"
		self.XMLlayers["layer1_2_alt1"] = "Autecology"
		self.XMLlayers["layer1_2_1"] = "ModelType"
		self.XMLlayers["layer1_2_1_1"] = "System"
		self.XMLlayers["layer1_2_1_1_1"] = "Scope"
		self.XMLlayers["layer1_2_1_1_2"] = "SystemDescription"
		self.XMLlayers["layer1_2_1_1_3"] = "SystemFlowDiagrams"
		self.XMLlayers["layer1_2_1_1_4"] = "KnowledgeRules"
#		self.XMLlayers["layer1_3"] = "FysicalCharacteristics"			#Not implemented (yet?)
#		self.XMLlayers["layer1_4"] = "Traits"			                #Not implemented (yet?)
		self.XMLlayers["layer1_5"] = "ContentDescription"
		self.XMLlayers["layer1_6"] = "Documentation"
		self.XMLlayers["layer1_7"] = "DataSources"

		#XML paths
		self.xmlns = "{" + self.xmlns + "}"
		topic_layers = ["layer1_1"]
		self.topic_path = self.make_find([self.XMLlayers[x] for x in topic_layers])
		modeltype_layers = ["layer1_2_alt1","layer1_2_1"]
		self.modeltype_path = self.make_find([self.XMLlayers[x] for x in modeltype_layers])
		self.system_path = self.make_find([self.XMLlayers["layer1_2_1_1"]])
		self.contentdescription_path = self.make_find([self.XMLlayers["layer1_5"]])
		self.systemscope_path_spec = self.make_find([self.XMLlayers["layer1_2_1_1_1"]])
		self.systemdescription_path_spec = self.make_find([self.XMLlayers["layer1_2_1_1_2"]])
		self.systemflowdiagram_path_spec = self.make_find([self.XMLlayers["layer1_2_1_1_3"]])
		self.system_path_spec = self.make_find([self.XMLlayers["layer1_2_1_1_4"]])

		#XML_specifics
		self.XMLconvention = {}
		self.XMLconvention["topic_species"] = "Species"
		self.XMLconvention["topic_wfdind"] = "WFDindicator"
		self.XMLconvention["modeltypekey"] = "name"
		self.XMLconvention["systemkey"] = "name"
		self.XMLconvention["rc"] = "ResponseCurve"
		self.XMLconvention["rckey"] = "name"
		self.XMLconvention["fb"] = "FormulaBased"
		self.XMLconvention["fbkey"] = "name"
		self.XMLconvention["-Infvalue"] = -999999.0
		self.XMLconvention["Infvalue"] = 999999.0
		self.XMLconvention["EoL_ID"] = "EoLpagenr"
		self.XMLconvention["GeoNames_ID"] = "GeoNames"

		#Code specifics
		self.XMLconvention["rc_dict_datatable"] = "rule"
		self.XMLconvention["fb_result"] = "result_calculation"

		self.XMLconvention["allowed_knowledgeRulesNames"] = [self.XMLconvention["rc"],self.XMLconvention["fb"]]


		#External specifics
		self.XMLconvention["EoL_Link_ID"] = "https://eol.org/pages/"
		self.XMLconvention["GeoNames_Link_ID"] = "https://www.geonames.org/"


		if((self.fullname is not None) and (self.name_ext == "xml")):
			self._readxml()

	def _readxml(self):
		self.xmlparse = ET.parse(self.fullname)
		self.xmlroot = self.xmlparse.getroot()
		
		self.namespaces = dict([
	    	node for _, node in ET.iterparse(
	        	self.fullname, events=['start-ns'])])
		for k,v in self.namespaces.copy().items():
			if k == '':
				self.namespaces[self.xmlns] = v
		return()

	def _writexml(self,filename):
		xmltext = ET.ElementTree(self.xmlroot)
		xmltext.write(filename)
		return()

	def check_xml_present(self):
		if(self.xmlroot == None):
			raise RuntimeError('No xml loaded yet, use "_readxml"')
		return()

	def check_modeltype_name(self,modeltypename):
		if(modeltypename not in self.modeltypes):
			if(self.modeltypes == None):
				raise RuntimeError('No scan loaded yet, use "_scan"')
			else:
				raise RuntimeError('System not existent and not present in self.modeltypes')
		return()

	def check_system_name(self,systemname):
		if(systemname not in self.systems):
			if(self.systems == None):
				raise RuntimeError('No scan loaded yet, use "_scan_model"')
			else:
				raise RuntimeError('System not existent and not present in self.systems')
		return()

	def check_element_numbers(self,element_list, expected, operator):
		operators = ["gt","eq","st"]

		if(operator not in operators):
			raise RuntimeError("Unexpected operator provided,accepted are " +\
			 ",".join(operators) + " .")

		if(operator == "gt"):
			if(expected < len(element_list)):
				pass
			else:
				raise RuntimeError("Lower or equal than " +str(expected) +" elements found." +\
					" Greater than expected")

		elif(operator == "eq"):
			if(expected == len(element_list)):
				pass
			else:
				raise RuntimeError("Lower or higher than " +str(expected) +" elements found."+\
					" Equal expected")

		elif(operator == "lt"):
			if(expected > len(element_list)):
				pass
			else:
				raise RuntimeError("Equal or higher than " +str(expected) +" elements found."+\
					" Lower than expected")

		else:
			RuntimeError("Invalid input")
		return()


	def find_element_by_name(self, root, name_key, name_value):
		#finds for exact name match
		element_list = [e for e in root if(name_value == e.get(name_key))]  
		return(element_list)

	def find_element_by_name_approximation(self, root, name_key, name_value):
		#finds for part of name match
		element_list = [e for e in root if(name_value in e.get(name_key))]  
		return(element_list)

	def get_element_topics(self):
		self.check_xml_present()
		type_tag_topic = self.xmlroot.find(self.topic_path)
		topic_elements = [topic for topic in type_tag_topic]
		return(topic_elements)

	def get_element_contentdescription(self):
		type_tag_cd = self.xmlroot.find(self.contentdescription_path)
		return(type_tag_cd)

	def get_element_modeltypes(self):
		self.check_xml_present()
		type_tag_mod = self.xmlroot.findall(self.modeltype_path)
		return(type_tag_mod)

	def get_element_modeltype(self,modeltypename):
		self.check_modeltype_name(modeltypename)
		type_tag_mod = self.get_element_modeltypes()
		type_tag_mod_list = self.find_element_by_name(type_tag_mod,\
							self.XMLconvention["modeltypekey"],modeltypename)
		self.check_element_numbers(type_tag_mod_list, expected = 1, operator = "eq")
		type_tag_modt = type_tag_mod_list[0]
		return(type_tag_modt)

	def get_element_systems(self, modeltypename):
		self.check_xml_present()
		type_tag_modt = self.get_element_modeltype(modeltypename)
		type_tag_sys = type_tag_modt.findall(self.system_path)
		return(type_tag_sys)

	def get_element_system(self, modeltypename, systemname):
		self.check_system_name(systemname)
		type_tag_sys = self.get_element_systems(modeltypename)
		type_tag_sys_list = self.find_element_by_name(type_tag_sys,\
							self.XMLconvention["systemkey"],systemname)
		self.check_element_numbers(type_tag_sys_list, expected = 1, operator = "eq")
		type_tag_syst = type_tag_sys_list[0]
		return(type_tag_syst)

	def get_element_scope(self, modeltypename, systemname):
		type_tag_syst = self.get_element_system(modeltypename, systemname)
		type_tag_scope = type_tag_syst.find(self.systemscope_path_spec)
		return(type_tag_scope)

	def get_element_systemdescription(self, modeltypename, systemname):
		type_tag_syst = self.get_element_system(modeltypename, systemname)
		type_tag_systemdescription = type_tag_syst.find(self.systemdescription_path_spec)
		return(type_tag_systemdescription)

	def get_element_systemflowdiagram(self, modeltypename, systemname):
		type_tag_syst = self.get_element_system(modeltypename, systemname)
		type_tag_systemflowdiagram = type_tag_syst.find(self.systemflowdiagram_path_spec)
		return(type_tag_systemflowdiagram)

	def get_element_knowledgerules(self,modeltypename, systemname):
		type_tag_syst = self.get_element_system(modeltypename, systemname)
		type_tag_krs = type_tag_syst.find(self.system_path_spec)
		return(type_tag_krs)

	def get_element_response_curve(self, modeltypename, systemname, rcname):
		type_tag_krs = self.get_element_knowledgerules(modeltypename, systemname)
		type_tag_rcs = type_tag_krs.findall(self.make_find([self.XMLconvention["rc"]]))
		type_tag_rc_list = self.find_element_by_name(type_tag_rcs,\
							self.XMLconvention["rckey"],rcname)
		
		#check whether response curve exists or exists multiple times
		if(len(type_tag_rc_list) == 0):
			raise ValueError("There is no repsponse curve named " + str(rcname) + " in ModelType " + str(modeltypename) +\
				" and System " + str(systemname) + " .")

		self.check_element_numbers(type_tag_rc_list, expected = 1, operator = "eq")
		type_tag_rc = type_tag_rc_list[0]
		return(type_tag_rc)

	def get_element_formula_based(self, modeltypename, systemname, fbname):
		type_tag_krs = self.get_element_knowledgerules(modeltypename, systemname)
		type_tag_fbs = type_tag_krs.findall(self.make_find([self.XMLconvention["fb"]]))
		type_tag_fb_list = self.find_element_by_name(type_tag_fbs,\
							self.XMLconvention["fbkey"],fbname)
		self.check_element_numbers(type_tag_fb_list, expected = 1, operator = "eq")
		type_tag_fb = type_tag_fb_list[0]
		return(type_tag_fb)

	def get_data_response_curve_data(self, rc_element):
		rule_dict = {}
		rule_dict["name"] = rc_element.get('name')
		rule_dict["KnowledgeruleCategorie"] = self.XMLconvention["rc"]
		rule_dict["type"] = rc_element.find(self.make_find(['type'])).text
		rule_dict["layername"] = rc_element.find(self.make_find(['layername'])).text
		rule_dict["unit"] = rc_element.find(self.make_find(['unit'])).text
		rule_dict["statistic"] = rc_element.find(self.make_find(['statistic'])).text

		parameter_list = []
		if(rule_dict["type"] == "scalar"):
			find_scalar = self.make_find(["valuesScalar","parameter"])
			column_names = rc_element.findall(find_scalar)[0].keys()
			for parameter in rc_element.findall(find_scalar):
				parameter_list.append([float(parameter.get("value")),float(parameter.get("HSI"))])
		elif(rule_dict["type"] == "categorical"):
			find_categorical = self.make_find(["valuesCategorical","parameter"])
			column_names = rc_element.findall(find_categorical)[0].keys()
			for parameter in rc_element.findall(find_categorical):
				parameter_list.append([str(parameter.get("cat")),float(parameter.get("HSI"))])
		elif(rule_dict["type"] == "ranges"):
			find_ranges = self.make_find(["valuesRanges","parameter"])
			column_names = rc_element.findall(find_ranges)[0].keys()
			for parameter in rc_element.findall(find_ranges):
				parameter_list.append([float(parameter.get("rangemin")),float(parameter.get("rangemax")),float(parameter.get("HSI"))])
		elif(rule_dict["type"] == "range / categorical"):
			find_rangecategorical = self.make_find(["valuesRangeCategorical","parameter"])
			column_names = rc_element.findall(find_rangecategorical)[0].keys()
			for parameter in rc_element.findall(find_rangecategorical):
				parameter_list.append([float(parameter.get("rangemin")),float(parameter.get("rangemax")),str(parameter.get("cat")),float(parameter.get("HSI"))])
		else:
			raise RuntimeError("type "+ rule_dict["type"] + " is not available.")

		rule_dict["rule"] = pandas.DataFrame(parameter_list, columns = column_names)
		return(rule_dict)

	def get_data_formula_based_data(self, fb_element):
		ToFormula = Interpreter()

		rule_dict = {}
		rule_dict["name"] = fb_element.get('name').replace('"','')
		rule_dict["KnowledgeruleCategorie"] = self.XMLconvention["fb"]
		# rule_dict["type"] = rc_element.find('type').text
		rule_dict["layername"] = fb_element.find(self.make_find(['layername'])).text.replace('"','')
		rule_dict["unit"] = fb_element.find(self.make_find(['unit'])).text.replace('"','')
		rule_dict["statistic"] = fb_element.find(self.make_find(['statistic'])).text.replace('"','')
		rule_dict["output"] = fb_element.find(self.make_find(['output'])).text.replace('"','')
		rule_dict["equation_text"] = fb_element.find(self.make_find(['equation'])).text.replace('"','').replace('^','**')
		# rule_dict["equation"] = ToFormula(rule_dict["equation_text"])

		rule_dict["parameters"] = [] 
		#Get the number of values under Parameteers
		fb_values_tags = fb_element.findall(self.make_find(["Parameters","valuesScalar"])) + \
						fb_element.findall(self.make_find(["Parameters","valuesConstant"])) 
		for values in fb_values_tags:
			parameter_dict = {}
			parameter_dict["dataname"] = values.get("dataname")
			parameter_dict["type"] = values.get("type")
			parameter_dict["unit"] = values.get("unit")

			#Get data per Values, assess the type and store it.
			parameter_list = []
			if(parameter_dict["type"] == "constant"):
				for parameter in values.findall(self.make_find(["parameter"])):
					parameter_list.append([str(parameter.get("constantset")), float(parameter.get("value"))])
			elif(parameter_dict["type"] == "scalar"):
				for parameter in values.findall(self.make_find(["parameter"])):
					parameter_list.append([float(parameter.get("min")), float(parameter.get("max"))])
			else:
				raise RuntimeError("type "+ parameter_dict["type"] + " is not available.")

			column_names = values.findall(self.make_find(["parameter"]))[0].keys()
			parameter_dict["data"] = pandas.DataFrame(parameter_list, columns = column_names)
			rule_dict["parameters"].append(parameter_dict)

		return(rule_dict)


	def make_fb_first_parametersettings(self, fb_data):
		parametersettings = {}
		for i, var in enumerate(fb_data["parameters"]):
			if(var["type"] == "scalar"):
				min_var = var["data"]["min"].iloc[0]
				if(i == 0):
					max_var = var["data"]["max"].iloc[0]
					stepsize = (max_var-min_var)/10
					variableparameter = {var["dataname"] : list(np.arange(min_var,max_var,stepsize))}
				
				parametersettings[var["dataname"]] = min_var

			elif(var["type"] == "constant"):
				first_convar_value = var["data"]["value"].iloc[0]
				if(i == 0):
					convar_value = var["data"]["value"].tolist()						
					variableparameter = {var["dataname"] : convar_value}

				parametersettings[var["dataname"]] = first_convar_value

			else:
				raise ValueError(" type of knowledge rule is not enabled :" + str(var["type"]))

		return(parametersettings,variableparameter)

	def calculate_fb(self, fb_data, parametersettings, variableparameter = None):
		#CALCULATION WITH ACCEPTING ONE LIST or ONLY SINGLE VALUES?

		#set up formula interpretation
		listparameter = False
		ToFormula = Interpreter()
		
		#check if parametersettings is complete
		fb_data_names = [value["dataname"] for value in fb_data["parameters"]]
		
		if(not(variableparameter == None)):
			if(len(list(variableparameter.keys())) == 1):
				variable_key = list(variableparameter.keys())[0]
				parametersettings[variable_key] = variableparameter[variable_key]
				listparameter = True
			else:
				raise ValueError("Only one parametersetting can be handed as a list")
		
		more_pr = [i for i in list(parametersettings.keys()) if(not (i in fb_data_names))]
		less_pr = [i for i in fb_data_names if(not (i in list(parametersettings.keys())))]
		if(len(more_pr) > 0):
			raise ValueError("To many or incorrect parametersettings were provided : " + str(more_pr))
		if(len(less_pr) > 0):
			raise ValueError("Missing parametersettings : " + str(less_pr))

		#collect the rules
		for	parametername in parametersettings.keys():
			if(listparameter == True and parametername == variable_key):
				continue

			#check if a string converts to float
			if(not str(parametersettings[parametername]).lstrip("-").replace('.','',1).isdigit()):
				raise ValueError("Value of parametersettings should be float or int : " + str(parametername))
			#fill formula dictionary
			ToFormula.symtable[parametername] = float(parametersettings[parametername])

		#calculate formula
		if(listparameter == False):
			parametersettings[self.XMLconvention["fb_result"]] = ToFormula(fb_data["equation_text"])
		elif(listparameter == True):
			result_calculation = []
			for element in variableparameter[variable_key]:
				#check if a string converts to float
				if(not str(element).lstrip("-").replace('.','',1).isdigit()):
					raise ValueError("Value of parametersettings should be float or int : " + str(parametername))
				
				#fill formula dictionary
				ToFormula.symtable[variable_key] = float(element)
				result_calculation.append(ToFormula(fb_data["equation_text"]))

			parametersettings[self.XMLconvention["fb_result"]] = result_calculation
		else:
			raise ValueError("listparameter can only be True of False")

		#Check on non-numeric results
		if(False in np.isfinite(result_calculation)):
			raise Warning("non-finite number returned from calculation, see if parameter ranges need to be limited")

		return(parametersettings)



	def get_fb_variable_and_result(self, fb_data, parametersettings):
		#initilize the class to get XMLconvention
		init_Aut = AutecologyXML(None)


		if(not(init_Aut.XMLconvention["fb_result"] in parametersettings)):
			raise ValueError("result has not been calculated, run self.calculate_fb first.")

		pset = copy.deepcopy(parametersettings)

		result = pset[init_Aut.XMLconvention["fb_result"]]
		pset.pop(init_Aut.XMLconvention["fb_result"], None)

		#Get variable list
		variable_key = None
		for key_entry, data_entry in pset.items():
			if(isinstance(data_entry,list)):
				variable_key = key_entry

		if(variable_key == None):
			raise ValueError("no variable for calculation has been found.")

		variable = pset[variable_key]
		pset.pop(variable_key, None)

		[variable_dict] = [value for value in fb_data["parameters"] if(value["dataname"] == variable_key)]

		return(result, variable, variable_dict)

	def _scan(self):

		#Get all topics
		topics = self.get_element_topics()
		topic_names =  list(child.tag.replace(self.xmlns,"") for child in topics)

		#Check if only one topic
		if(len(topics) != 1):
			raise ValueError("Only one topic element allowed.")

		#get only element
		topic = topics[0]
		topic_name = topic_names[0]

		if(topic_name == self.XMLconvention["topic_species"]):
			self.topic_name = self.XMLconvention["topic_species"]
			self.EoL_ID = topic.find(self.make_find([self.XMLconvention["EoL_ID"]])).text
			self.EoL_Link = self.XMLconvention["EoL_Link_ID"] + self.EoL_ID 
			self.latinname = topic.find(self.make_find(['LatName'])).text
			self.commonnames = [{"name" : cn.get("name"), "language" : cn.get("language")}\
								 for cn in topic.find(self.make_find(['CommonNames']))]
	
		elif(topic_name == self.XMLconvention["topic_wfdind"]):
			self.topic_name = self.XMLconvention["topic_wfdind"]
			self.commonnames = [{"name" : cn.get("name"), "language" : cn.get("language")}\
								 for cn in topic.find(self.make_find(['CommonNames']))]
		
		else:
			raise ValueError("Topic element is not yet available for interpretation : " + topic_name)
		
		#get modeltypes
		type_tag_mod = self.get_element_modeltypes()
		modeltypes_available = [e.get(self.XMLconvention["modeltypekey"]) for e in type_tag_mod]
		self.modeltypes = modeltypes_available

		return()

	def _scan_modeltype(self, modeltypename):							 
		type_tag_sys = self.get_element_systems(modeltypename)
		systems_available = [e.get(self.XMLconvention["systemkey"]) for e in type_tag_sys]
		self.systems = systems_available

		return()

	def _scan_system(self, modeltypename, systemname):

		#get systemname
		self.systemname = systemname

		#get scope
		self._scan_scope(modeltypename, systemname)



		return()

	def _scan_scope(self, modeltypename, systemname):
		self.spatial_scope = self._read_spatial_scope(modeltypename, systemname)
		self.temporal_scope = self._read_temporal_scope(modeltypename , systemname)

		#get spatial scope
		self.geonames_names = [ss["name"] for ss in self.spatial_scope] 
		self.geonames_ids = [ss["GeoNames_id"] for ss in self.spatial_scope]
		self.geonames_links = [XMLconvention["GeoNames_Link_ID"] + str(gid) for gid in self.geonames_ids]

		#get temporal scope
		self.StartDate = self.temporal_scope["StartDate"]
		self.EndDate = self.temporal_scope["EndDate"]
		
		return()

	def _scan_knowledgerules(self, modeltypename, systemname):

		krs_root = self.get_element_knowledgerules(modeltypename, systemname)
		
		#Store data
		self.systemname = systemname
		self.knowledgeRulesNr = len(list(child for child in krs_root)) 
		self.knowledgeRulesCategorie = list(child.tag.replace(self.xmlns,"") for child in krs_root)


		#Make dictonary of knowledge rules
		rule_overview = {}
		rule_overview["rules"] = {}
		for nr, child in enumerate(krs_root):
			if(self.knowledgeRulesCategorie[nr] == self.XMLconvention["rc"]):
				rule_dict = self.get_data_response_curve_data(child)
			elif(self.knowledgeRulesCategorie[nr] == self.XMLconvention["fb"]):
				rule_dict = self.get_data_formula_based_data(child)
			else:
				raise RuntimeError("type '" + str(self.knowledgeRulesCategorie[nr]) + "' not available in methods for data extraction.")
			rule_overview["rules"][child.get('name')] = rule_dict
		
		#Store data		
		self.knowledgeRulesDict = rule_overview
		self.knowledgeRulesNames = [value["name"].replace('"','') for key, value in self.knowledgeRulesDict["rules"].items()]
		self.knowledgeRulesStatistics = [value["statistic"].replace('"','') for key, value in self.knowledgeRulesDict["rules"].items()]
		self.knowledgeRulesUnits = [value["unit"].replace('"','') for key, value in self.knowledgeRulesDict["rules"].items()]

		return()

	def _scan_systemflowdiagrams(self, modeltypename, systemname):
		syfd_overview = []
		for syfd in self.get_element_systemflowdiagram(modeltypename, systemname):
			flow_diagram_name = syfd.get("name")
			from_overview = []
			for fromlink in syfd:
				name = fromlink.get("name")
				label = fromlink.find(self.make_find(["label"])).text
				equation = fromlink.find(self.make_find(["equation"])).text
				to = [tolink.text.replace('"','') for tolink in fromlink.findall(self.make_find(["To"]))]
				from_overview.append(OrderedDict([("From_name",name),("label",label),("equation",equation),("To_names",to)]))
			syfd_overview.append(OrderedDict([("diagram_name",flow_diagram_name),("Links",from_overview)]))

		#Store data
		self.flowdiagrams = [diagram["diagram_name"] for diagram in syfd_overview]
		self.flowdiagrams_lists = syfd_overview

		return()

	def _read_contentdescription(self):
		con_overview = [{"language" : con.get("language"), "description" : con.find(self.make_find(["text"])).text}\
										 for con in self.get_element_contentdescription()]
		return(con_overview)

	def _write_contentdescription(self, language, text):
		con_specific = [con for con in self.get_element_contentdescription() if(con.get("language") == language)]
		con_specific[0].find(self.make_find(["text"])).text = text
		return() 



	def _read_spatial_scope(self, modeltypename, systemname):
		scope_element = self.get_element_scope(modeltypename,systemname)
		
		#get scopes of relevance
		spatial_scope_element = scope_element.find(self.make_find(["SpatialScope"]))
		temporal_scope_element = scope_element.find(self.make_find(["TemporalScope"]))

		#extract spatial scope data
		spatial_scope = [{"name" : sp_scope.get("name"), "GeoNames_id" : sp_scope.get("id")}\
							for sp_scope in spatial_scope_element]
		return(spatial_scope)
		

	def _read_temporal_scope(self, modeltypename, systemname):
		scope_element = self.get_element_scope(modeltypename,systemname)
		
		#get scopes of relevance
		temporal_scope_element = scope_element.find(self.make_find(["TemporalScope"]))

		#extract temporal scope data
		startdate = temporal_scope_element.find(self.make_find(["StartDate"])).text
		enddate = temporal_scope_element.find(self.make_find(["EndDate"])).text
		temporal_scope = {"startdate" : startdate, "enddate" : enddate}

		return(temporal_scope)

	def _read_systemflowdiagram(self, modeltypename, systemname, diagramname):
		syfd_elements = self.get_element_systemflowdiagram(modeltypename, systemname)
		flow_diagram_names = [syfd.get("name") for syfd in syfd_elements]

		if(not(diagramname in flow_diagram_names)):
			raise RuntimeError("Flowdiagram '" + str(diagramname) + "' not available in modeltype '" +\
				str(modeltypename) + "' with system '" + str(systemname) + "' .")
			return()

		if(len([i for i, e in enumerate(flow_diagram_names) if e == diagramname]) != 1):
			raise RuntimeError("Flowdiagram '" + str(diagramname) + "' might occur multiple times in modeltype '" +\
				str(modeltypename) + "' with system '" + str(systemname) + "' .")
			return()

		syfd = syfd_elements[flow_diagram_names.index(diagramname)]
		flowdiagram_name = syfd.get("name")
		from_overview = []
		for fromlink in syfd:
			name = fromlink.get("name")
			label = fromlink.find(self.make_find(["label"])).text
			equation = fromlink.find(self.make_find(["equation"])).text
			to = [tolink.text.replace('"','') for tolink in fromlink.findall(self.make_find(["To"]))]
			from_overview.append(OrderedDict([("From_name",name),("label",label),("equation",equation),("To_names",to)]))
		flowdiagram = OrderedDict([("diagram_name",flowdiagram_name),("Links",from_overview)])
		
		return(flowdiagram)

	def _read_systemdescription(self, modeltypename, systemname):
		syd_overview = [{"language" : syd.get("language"),"description" : syd.find(self.make_find(["text"])).text}\
										 for syd in self.get_element_systemdescription(modeltypename, systemname)]
		return(syd_overview)

	def _write_systemdescription(self, modeltypename, systemname, language, text):
		syd_specific = [syd for syd in self.get_element_systemdescription(modeltypename, systemname) if(syd.get("language") == language)]
		syd_specific[0].find(self.make_find(["text"])).text = text
		return()



#-------------------------------------------------------------------------------
# Visualization
#-------------------------------------------------------------------------------
	
	def visualize_rc(self, rc_data):

		#collect the data
		data = rc_data["rule"]
		x_label = rc_data["name"] + " ("+ rc_data["unit"] +")"
		if(rc_data["type"] == "scalar" or rc_data["type"] == "categorical"):
			y_cname = data.columns[1]
			x_cname = data.columns[0]

			x_data = data[x_cname].to_numpy()
		
		elif(rc_data["type"] == "ranges"):
			minr_cname = data.columns[0]
			maxr_cname = data.columns[1]
			y_cname = data.columns[2]

			min_range_data = data[minr_cname].to_numpy()
			max_range_data = data[maxr_cname].to_numpy()

			min_range_data = np.where(min_range_data == self.XMLconvention["-Infvalue"], "-Inf", min_range_data)
			max_range_data = np.where(max_range_data == self.XMLconvention["Infvalue"], "Inf", max_range_data) 

			x_data = np.asarray([str(a) + " - " + str(b) for a,b in zip(min_range_data,max_range_data)])

		elif(rc_data["type"] == "range / categorical"):
			minr_cname = data.columns[0]
			maxr_cname = data.columns[1]
			y_cname = data.columns[3]
			x_cname = data.columns[2]
			
			min_range_data = data[minr_cname].to_numpy()
			max_range_data = data[maxr_cname].to_numpy()
			x_data = data[x_cname].to_numpy()
		
		else:
			raise RuntimeError("type '" + rc_data["type"] + "' not available.")

		y_data = data[y_cname].to_numpy()
		offset_y = (np.max(y_data) - np.min(y_data)) / 10
		
		#Set up a canvas
		width=5; height=4; dpi=100
		fig = Figure(figsize=(width, height), dpi=dpi)
		axes = fig.add_subplot(111)

		#Make type specific plots
		if(rc_data["type"] == "scalar"):
			offset_x = (np.max(x_data) - np.min(x_data)) / 10

			x_data = np.insert(x_data, 0, -99999.0)
			x_data = np.append(x_data, 99999.0)

			y_data = np.insert(y_data,0,y_data[0])
			y_data = np.append(y_data,y_data[-1])

			axes.plot(x_data,y_data,'-',lw=2)
			axes.set_xlim(np.min(data[x_cname].to_numpy()) - offset_x, np.max(data[x_cname].to_numpy()) + offset_x)
		
		elif((rc_data["type"] == "categorical") or (rc_data["type"] == "ranges") or\
			 (rc_data["type"] == "range / categorical")):
			x_pos = np.arange(len(x_data))
			axes.bar(x_pos, y_data, align='center', alpha=0.5)
			if((rc_data["type"] == "categorical") or (rc_data["type"] == "ranges")):
				axes.set_xticks(x_pos)
				axes.set_xticklabels([str(xval) for xval in x_data])
			elif(rc_data["type"] == "range / categorical"):
				min_range_data = np.where(min_range_data == self.XMLconvention["-Infvalue"], "-Inf", min_range_data)
				max_range_data = np.where(max_range_data == self.XMLconvention["Infvalue"], "Inf", max_range_data) 
				x_tick_labels = [str(b) + " - " + str(c) +"\n" + str(a) for a,b,c in zip(x_data,min_range_data,max_range_data)]
				axes.set_xticks(x_pos)
				axes.set_xticklabels(x_tick_labels)
			else:
				raise RuntimeError("type '" + rc_data["type"] + "' not available.")

		
		axes.set_ylim(np.min(data[y_cname].to_numpy()) -offset_y,np.max(data[y_cname].to_numpy()) + offset_y)
		axes.set_ylabel(y_cname +" (0.0 - 1.0)", fontsize=11)
		axes.set_xlabel(x_label, fontsize=11)
		axes.set_title(rc_data["name"], fontsize=13, weight=551)
		fig.set_tight_layout(True)
		
		#Make canvas manager
		dummy = plt.figure()
		new_manager = dummy.canvas.manager
		new_manager.canvas.figure = fig
		fig.set_canvas(new_manager.canvas)

		return(fig,axes)

	def visualize_fb_static(self, fb_data, parametersettings):
		#check if results is there
		
		result, variable, variable_dict = AutecologyXML.get_fb_variable_and_result(self, fb_data, parametersettings)

		#make plot based on data
		x_data = np.asarray(variable)
		offset_x = (np.max(x_data) - np.min(x_data)) / 10
		y_data = np.asarray(result)
		offset_y = (np.max(y_data) - np.min(y_data)) / 10
		
		x_label = variable_dict["dataname"] + " ("+ variable_dict["unit"] +")"
		
		#Set up a canvas
		width=5; height=4; dpi=100
		fig = Figure(figsize=(width, height), dpi=dpi)
		axes = fig.add_subplot(111)

		axes.plot(x_data,y_data,'-',lw=2)
		axes.set_xlim(np.min(x_data) - offset_x, np.max(x_data) + offset_x)
		axes.set_ylim(np.min(y_data) -offset_y,np.max(y_data) + offset_y)
		axes.set_ylabel(fb_data["output"] +" (" + fb_data["unit"] + ")", fontsize=11)
		axes.set_xlabel(x_label, fontsize=11)
		axes.set_title(fb_data["name"], fontsize=13, weight=551)
		fig.set_tight_layout(True)
		
		#Make canvas manager
		dummy = plt.figure()
		new_manager = dummy.canvas.manager
		new_manager.canvas.figure = fig
		fig.set_canvas(new_manager.canvas)

		return(fig,axes)

	def visualize_fb_dynamic(self, fb_data, parametersettings):
		#make the plot
		class SubWindow(QtWidgets.QWidget):
			def __init__(self, parent=None):
				super(SubWindow,self).__init__(parent)
				self.SubWindow_layout = QtWidgets.QGridLayout()

				self.create_plot_frame(fb_data,parametersettings)

				self.setLayout(self.SubWindow_layout)

			# def closeEvent(self, event):
			# 	event.ignore()

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

			def make_frame(self, fb_data, parametersettings):

				#initilize the class to get XMLconvention
				init_Aut = AutecologyXML(None)

				#rebuild the frame based on selected variable
				self.box = QtWidgets.QGroupBox()
				self.vbox = QtWidgets.QVBoxLayout()
			
				fb_box = QtWidgets.QGroupBox()
				self.fb_box_layout = QtWidgets.QGridLayout()

				fb_pixmap_widget = QtWidgets.QWidget(fb_box)
				fb_pixmap_layout = QtWidgets.QVBoxLayout(fb_pixmap_widget)

				#make plot
				fb_fig, fb_axes = AutecologyXML.visualize_fb_static(self, fb_data, parametersettings)
				self.fig = fb_fig
				self.axes = fb_axes
				
				#add plot to widget
				self.main_frame._dynamic_canvas = FigureCanvas(self.fig)
				self.main_frame._dynamic_canvas.setParent(self)
				self.fb_box_layout.addWidget(self.main_frame._dynamic_canvas)
				self.main_frame._dynamic_canvas.draw()
				self.fig.canvas.draw()
				self.main_frame._dynamic_canvas.setFixedWidth(500)
				self.main_frame._dynamic_canvas.setFixedHeight(500)
				
				self.fb_box_layout.addWidget(fb_pixmap_widget)
				fb_box.setLayout(self.fb_box_layout)

				#get the variable being shown
				result, variable, variable_dict = AutecologyXML.get_fb_variable_and_result(self, fb_data, parametersettings)
				
				comboBox = QtWidgets.QComboBox()
				comboBox.setObjectName("variable_box")
				comboBox.setMinimumWidth(200)
				comboBox.addItem(variable_dict["dataname"])
				
				#setup the layout
				sbox = QtWidgets.QVBoxLayout()

				for i, non_variable in enumerate(fb_data["parameters"]):
					if(non_variable["dataname"] == init_Aut.XMLconvention["fb_result"] or non_variable["dataname"] == variable_dict["dataname"]):
						pass
					else:
						comboBox.addItem(non_variable["dataname"])

						#Add dataproviders
						if(non_variable["type"] == "scalar"):
							slider_label = QtWidgets.QLabel(non_variable["dataname"] +" :")
							min_slide = non_variable["data"]["min"].iloc[0]
							max_slide = non_variable["data"]["max"].iloc[0]
							stepsize_slide = float((max_slide - min_slide)/10)
							slider = LabeledSlider(min_slide, max_slide, stepsize_slide, orientation = QtCore.Qt.Horizontal)
							slider.setObjectName(non_variable["dataname"])
							slider.setValue(parametersettings[non_variable["dataname"]])
							slider.setTracking(True)
							# slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
							print(parametersettings)
							slider.valueChanged.connect(lambda: self.on_draw(fb_data, parametersettings,["slider"]))

							#add to hbox
							sbox.addWidget(slider_label)
							sbox.addWidget(slider)


						elif(non_variable["type"] == "constant"):
							
							constant_box_label = QtWidgets.QLabel(non_variable["dataname"] + " :")
							constant_box = QtWidgets.QHBoxLayout()
							constant_box.setObjectName(non_variable["dataname"])
							
							for index, row_var in non_variable["data"].iterrows():
								tick_label = QtWidgets.QLabel(row_var["constantset"] +" :")
								tickbox = QtWidgets.QCheckBox()
								tickbox.setObjectName(row_var["constantset"])
								if(row_var["value"] == parametersettings[non_variable["dataname"]]):
									tickbox.setCheckState(QtCore.Qt.Checked)
									tickbox.setEnabled(False)
								else:
									tickbox.setCheckState(QtCore.Qt.Unchecked)

								tickbox.clicked.connect(lambda: self.on_draw(fb_data, parametersettings,["tickbox",constant_box.objectName()]))

								constant_box.addWidget(tick_label)
								constant_box.addWidget(tickbox)

							sbox.addWidget(constant_box_label)
							sbox.addLayout(constant_box)

				#set a connection for the combobox
				comboBox.currentIndexChanged.connect(lambda: self.on_draw(fb_data, parametersettings,["combobox"]))
								
				# Layout with box sizers
				hbox = QtWidgets.QHBoxLayout()
				hbox.addWidget(comboBox)
				hbox.setAlignment(comboBox, QtCore.Qt.AlignVCenter)
								
				self.vbox.addWidget(fb_box)
				self.vbox.addLayout(hbox)
				self.vbox.addLayout(sbox)

				self.box.setLayout(self.vbox)
				self.main_frame_layout.addWidget(self.box)

				return()


			def update(self, fb_data, parametersettings):

				#initilize the class to get XMLconvention
				init_Aut = AutecologyXML(None)

				#Clear plot
				self.fig.clf()
				plt.close(self.fig)
				self.clearLayout(self.fb_box_layout)
				self.main_frame._dynamic_canvas.draw()
				# self.main_frame._dynamic_canvas.update()


				#make plot
				fb_fig, fb_axes = AutecologyXML.visualize_fb_static(self, fb_data, parametersettings)
				self.fig = fb_fig
				self.axes = fb_axes
				self.fig.canvas.draw()
				
				#add plot to widget
				self.main_frame._dynamic_canvas = FigureCanvas(self.fig)
				self.main_frame._dynamic_canvas.setParent(self)
				self.fb_box_layout.addWidget(self.main_frame._dynamic_canvas)
				self.main_frame._dynamic_canvas.draw()
				self.fig.canvas.draw()
				self.main_frame._dynamic_canvas.setFixedWidth(500)
				self.main_frame._dynamic_canvas.setFixedHeight(500)

				#get the variable being shown
				result, variable, variable_dict = AutecologyXML.get_fb_variable_and_result(self, fb_data, parametersettings)
				
				#update combobox
				index = self.findChild(QtWidgets.QComboBox,"variable_box").findText(variable_dict["dataname"], QtCore.Qt.MatchFixedString)
				if(index >= 0):
					self.findChild(QtWidgets.QComboBox,"variable_box").setCurrentIndex(index)

				for i, non_variable in enumerate(fb_data["parameters"]):
					if(non_variable["dataname"] == init_Aut.XMLconvention["fb_result"] or non_variable["dataname"] == variable_dict["dataname"]):
						pass
					else:
						
						#Add dataproviders
						if(non_variable["type"] == "scalar"):
							
							 self.findChild(QtWidgets.QSlider,non_variable["dataname"]).setValue(parametersettings[non_variable["dataname"]])
							
						elif(non_variable["type"] == "constant"):
							
							for index, row_var in non_variable["data"].iterrows():
								if(row_var["value"] == parametersettings[non_variable["dataname"]]):
									self.findChild(QtWidgets.QCheckBox,row_var["constantset"]).setCheckState(QtCore.Qt.Checked)
									self.findChild(QtWidgets.QCheckBox,row_var["constantset"]).setEnabled(False)
								else:
									self.findChild(QtWidgets.QCheckBox,row_var["constantset"]).setCheckState(QtCore.Qt.Unchecked)
									self.findChild(QtWidgets.QCheckBox,row_var["constantset"]).setEnabled(True)

						else:
							raise ValueError("unsuported widgets")

				return()


			def on_pick(self, event):
				# The event received here is of the type
				# matplotlib.backend_bases.PickEvent
				#
				# It carries lots of information, of which we're using
				# only a small amount here.
				# 
				box_points = event.artist.get_bbox().get_points()
				msg = "You've clicked on a bar with coords:\n %s" % box_points
				
				QMessageBox.information(self, "Click!", msg)

			def create_plot_frame(self, fb_data, parametersettings):
			
				self.main_frame = QtWidgets.QWidget()
				self.main_frame_layout = QtWidgets.QVBoxLayout(self.main_frame)

				#make frame based on settings
				self.make_frame(fb_data, parametersettings)

				self.SubWindow_layout.addWidget(self.main_frame)

				return()

			def on_draw(self, fb_data, parametersettings, list_settings):
				""" Redraws the figure and remakes the framework
				"""

				#initilize the class to get XMLconvention
				init_Aut = AutecologyXML(None)

				#get current variable and results
				result, variable, variable_dict = AutecologyXML.get_fb_variable_and_result(self, fb_data, parametersettings)

				#remove current results and make fb_list
				parametersettings.pop(init_Aut.XMLconvention["fb_result"], None)
				fb_list = {variable_dict["dataname"] : variable}
				
				if(list_settings[0] == "combobox"):
					new_variable = self.findChild(QtWidgets.QComboBox,self.sender().objectName()).currentText()

					if(new_variable != variable_dict["dataname"]):
						#Remove old variable
						parametersettings.pop(variable_dict["dataname"], None)

						#Fill previous
						if(variable_dict["type"] == "scalar"): 
							parametersettings[variable_dict["dataname"]] = variable_dict["data"]["min"].iloc[0]
						elif(variable_dict["type"] == "constant"):
							parametersettings[variable_dict["dataname"]] = variable_dict["data"]["value"].iloc[0]
						else:
							raise ValueError("this type is not supported")
						
						[newvariable_dict] = [var for var in fb_data["parameters"] if(var["dataname"] == new_variable)]

						if(newvariable_dict["type"] == "scalar"):
							min_range = newvariable_dict["data"]["min"].iloc[0]
							max_range = newvariable_dict["data"]["max"].iloc[0]
							step_range = (max_range - min_range) / 10
							fb_list = {newvariable_dict["dataname"] : [number for number in np.arange(min_range, max_range, step_range)]}

						elif(newvariable_dict["type"] == "constant"):
							fb_list = {newvariable_dict["dataname"] : newvariable_dict["data"]["value"].tolist()}
						
						else:
							raise ValueError("this type is not supported")

					else:
						#just an update of the results needed
						pass

				elif(list_settings[0] == "slider"):
					parametersettings[self.sender().objectName()] = self.sender().value()

				elif(list_settings[0] == "tickbox"):
					[constant_dict] = [var for var in fb_data["parameters"] if(var["dataname"] == list_settings[1])]
					newvalue_const = float(constant_dict["data"][constant_dict["data"]["constantset"] == self.sender().objectName()]["value"])
					parametersettings[list_settings[1]] = newvalue_const					
				else:
					raise ValueError("unavailable command")

				#re-calculate the result
				fb_result = init_Aut.calculate_fb(fb_data, parametersettings, variableparameter = fb_list)		

				#make frame based on settings
				if(list_settings[0] == "combobox"):
					#clear self.vbox
					self.clearLayout(self.main_frame_layout)
					#remake the framework
					self.make_frame(fb_data, fb_result)
				else:
					#update the framework
					self.update(fb_data, fb_result)

				self.main_frame.update()

				return()
			

			def add_actions(self, target, actions):
				for action in actions:
					if action is None:
						target.addSeparator()
					else:
						target.addAction(action)

			def create_action(  self, text, slot=None, shortcut=None, 
							icon=None, tip=None, checkable=False):
				action = QtWidgets.QAction(text, self)
				if icon is not None:
					action.setIcon(QIcon(":/%s.png" % icon))
				if shortcut is not None:
					action.setShortcut(shortcut)
				if tip is not None:
					action.setToolTip(tip)
					action.setStatusTip(tip)
				if slot is not None:
					action.triggered.connect(slot)
				if checkable:
					action.setCheckable(True)
				return action

		return(SubWindow)


	def visualise_flowdiagram(self, flowdiagram):
		'''
		Visualisation performed by blockdiag.
		See documentation here:
		http://blockdiag.com/en/blockdiag
		See GitHub repository here:
		https://github.com/blockdiag/blockdiag
		'''


		#graph = pydot.Dot(graph_type='graph')
		source = ""
		source = source + "blockdiag { "
		source = source + "node_width = 300;"
		#source = source + "node_width = 40;"
		source = source + "span_width = 150;"
		#source = source + "span_width = 40;"

		source = source + "default_fontsize = 15;"

		for links_from in flow_diagram['Links']:
			from_name = links_from["From_name"]

			#add from link
			source = source + from_name + " [label = '" + links_from["label"] + "', shape = roundedbox];"
			
			for nr, link_to in enumerate(links_from["To_names"]):
				to_name = link_to
			#	edge = pydot.Edge(from_name,to_name)
			#	graph.add_edge(edge)
				if(nr == 0):
					source = source + from_name + " -> " + to_name + " [label = '" + links_from['equation'] + "', fontsize = 11];"
				else:
					source = source + from_name + " -> " + to_name + ";"

		source = source + "}" 

		#graph.write_png('example1_graph.png')
		tree = parser.parse_string(source)
		diagram = builder.ScreenNodeBuilder.build(tree)
		draw = drawer.DiagramDraw("SVG", diagram, filename = "flowdiagram.svg")
		#draw = drawer.DiagramDraw("PNG", diagram, filename = "flowdiagram.png")

		draw.draw()
		draw.save()



		return()


	def show_interactive_plot(self, SubWindow):

		class mainwindow(QtWidgets.QMainWindow):
			def __init__(self, parent=None):
				super(mainwindow,self).__init__(parent)
				label = QtWidgets.QLabel("Main Window",  self)
				self.groupbox = QtWidgets.QGroupBox()
				self.groupbox_layout = QtWidgets.QGridLayout()
				self.createsASubwindow()
				self.groupbox_layout.addWidget(self.mySubwindow)
				self.groupbox.setLayout(self.groupbox_layout)
				self.setCentralWidget(self.groupbox)


			def createsASubwindow(self):
	   			self.mySubwindow=SubWindow()
	   			#make pyqt items here for your subwindow
	   			#for example self.mySubwindow.button=QtGui.QPushButton(self.mySubwindow)

	   			self.mySubwindow.show()



		app = QtWidgets.QApplication(sys.argv)
		mainWin = mainwindow()
		mainWin.show()
		sys.exit(app.exec_())

		return()






################################################################################
#																			  #
#								UNIT TESTS									#
#																			  #
################################################################################

def restore_builtin_open():
	""" Restore original builtin function open(). """
	__builtins__.__dict__['open'] = BUILTIN_FUNCTION_OPEN

class Test_File(unittest.TestCase):

	def setUp(self):
		self.f = _File()

class TestAutecologyXML_any(unittest.TestCase):

	def setUp(self):
		# mock XML file
		xmltest = AutecologyXML(filename = "AutecologyXMLtest.xml")
		self.xmltest = xmltest

	def tearDown(self):
		restore_builtin_open()

	def test_readxml(self):
		self.assertTrue(isinstance(self.xmltest.fullname, str))
		self.xmltest._readxml()
		self.assertTrue(isinstance(self.xmltest.xmlroot, Element))

	def test_scan(self):
		self.xmltest._scan()
		self.assertTrue(isinstance(self.xmltest.latinname,str))
		self.assertTrue(isinstance(self.xmltest.commonnames,list))
		self.assertTrue(isinstance(self.xmltest.commonnames[0],dict))
		self.assertTrue(len(self.xmltest.commonnames[0].keys()),2)
		self.assertTrue(list(self.xmltest.commonnames[0].keys())[0],"language")
		self.assertTrue(list(self.xmltest.commonnames[0].keys())[1],"name")
		self.assertTrue(isinstance(self.xmltest.modeltypes,list))
		
	def test_scan_modeltype(self):
		self.xmltest._scan()
		self.xmltest._scan_modeltype(self.xmltest.modeltypes[0])
		self.assertTrue(isinstance(self.xmltest.systems,list))


	def test__read_contentdescription(self):
		spd_overview = self.xmltest._read_contentdescription()
		self.assertTrue(isinstance(spd_overview,list))
		self.assertTrue(isinstance(spd_overview[0],dict))
		self.assertTrue(len(spd_overview[0].keys()),2)
		self.assertTrue(list(spd_overview[0].keys())[0],"language")
		self.assertTrue(list(spd_overview[0].keys())[1],"description")

	def test_scan_system(self):
		pass
		#TO BE FILLED

	def test_scan_knowledgerules(self):
		self.xmltest._scan()
		#test per modeltype
		for cur_modeltype in self.xmltest.modeltypes:
			self.xmltest._scan_modeltype(cur_modeltype)
			#test per system
			for cur_system in self.xmltest.systems:
				self.xmltest._scan_knowledgerules(modeltypename = cur_modeltype, systemname = cur_system)
				self.assertTrue(isinstance(self.xmltest.systemname, str),"Error occurs at system :" + cur_system)
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesNr,int),"Error occurs at system :" + cur_system)
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesCategorie,list),"Error occurs at system :" + cur_system) 
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesDict,dict),"Error occurs at system :" + cur_system) 
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesNames,list),"Error occurs at system :" + cur_system)
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesStatistics,list),"Error occurs at system :" + cur_system)
				self.assertTrue(isinstance(self.xmltest.knowledgeRulesUnits,list),"Error occurs at system :" + cur_system)
				self.assertTrue(all(elem in self.xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
										in self.xmltest.knowledgeRulesCategorie),"Error occurs at system :" + cur_system)
		

	def test_read_systemdescription(self):
		test_language = "ENG"
		newtext = '''TestNew
TESTNEW'''
		self.xmltest._scan()
		#test per modeltype
		for cur_modeltype in self.xmltest.modeltypes:
			self.xmltest._scan_modeltype(cur_modeltype)
			#test per system
			for cur_system in self.xmltest.systems:
				syd_overview = self.xmltest._read_systemdescription(modeltypename = cur_modeltype, systemname = cur_system)
				sys_text = [sys["description"] for sys in syd_overview if(sys["language"] == test_language)][0]
				self.assertTrue(isinstance(sys_text,str),"Error occurs at system :" + cur_system +\
															", with language : " + test_language)
				self.xmltest._write_systemdescription(modeltypename = cur_modeltype, systemname = cur_system, language = test_language, text = newtext)
				syd_overview2 = self.xmltest._read_systemdescription(modeltypename = cur_modeltype, systemname = cur_system)
				sys_text2 = [sys2["description"] for sys2 in syd_overview2 if(sys2["language"] == test_language)][0]
				self.assertTrue(isinstance(sys_text2,str),"Error occurs at system :" + cur_system)		

	def test_get_response_curve(self):
		self.xmltest._scan()
		#test per modeltype
		for cur_modeltype in self.xmltest.modeltypes:
			self.xmltest._scan_modeltype(cur_modeltype)
			#test per system
			for cur_system in self.xmltest.systems:
				self.xmltest._scan_knowledgerules(modeltypename = cur_modeltype, systemname = cur_system)
				allrc = self.xmltest.knowledgeRulesNames
				alltypes = self.xmltest.knowledgeRulesCategorie
				for cur_rc, cur_type in zip(allrc,alltypes):
					if(cur_type == "ResponseCurve"):
						rc_tag = self.xmltest.get_element_response_curve(modeltypename = cur_modeltype, systemname = cur_system, rcname = cur_rc)	
						self.assertTrue(isinstance(rc_tag,Element))
						rc_data = self.xmltest.get_data_response_curve_data(rc_tag)
						self.assertTrue(isinstance(rc_data, dict))
						self.assertTrue(self.xmltest.XMLconvention["rc_dict_datatable"] in rc_data)
						self.assertTrue(isinstance(rc_data[self.xmltest.XMLconvention["rc_dict_datatable"]],pandas.core.frame.DataFrame))

	def test_plot_response_curve(self):
		self.xmltest._scan()
		#test per modeltype
		for cur_modeltype in self.xmltest.modeltypes:
			self.xmltest._scan_modeltype(cur_modeltype)
			#test per system
			for cur_system in self.xmltest.systems:
				self.xmltest._scan_knowledgerules(modeltypename = cur_modeltype, systemname = cur_system)
				allrc = self.xmltest.knowledgeRulesNames
				alltypes = self.xmltest.knowledgeRulesCategorie
				for cur_rc, cur_type in zip(allrc,alltypes):
					if(cur_type == "ResponseCurve"):
						rc_tag = self.xmltest.get_element_response_curve(modeltypename = cur_modeltype, systemname = cur_system, rcname = cur_rc)	
						rc_data = self.xmltest.get_data_response_curve_data(rc_tag)
						fig, axes = self.xmltest.visualize_rc(rc_data)
						self.assertTrue(np.array_equal(fig.get_size_inches()*fig.dpi, np.asarray([500.0,400.0]))) #size in dpi
						self.assertTrue(isinstance(axes.get_title(),str))
						self.assertTrue(isinstance(axes.get_ylabel(),str))
						self.assertTrue(isinstance(axes.get_xlabel(),str))
						self.assertTrue(len(axes.get_xticks()) > 2)
						self.assertTrue(len(axes.get_yticks()) > 2)
						#TEST NUMBER OF SUBPLOTS
						#TEST PLOT TYPES
						#TEST AXES TICK MARKS CONTENT

class TestAutecologyXML_testxml(unittest.TestCase):

	def setUp(self):
		# mock XML file
		xmltest = AutecologyXML(filename = "AutecologyXMLtest.xml")
		self.xmltest = xmltest

	def tearDown(self):
		restore_builtin_open()

	def test_readxml(self):
		self.assertEqual(self.xmltest.fullname, "AutecologyXMLtest.xml")
		self.xmltest._readxml()
		self.assertTrue(isinstance(self.xmltest.xmlroot,Element))

	def test_scan(self):
		self.xmltest._scan()
		self.assertEqual(self.xmltest.latinname, "Testus testus")
		self.assertEqual(self.xmltest.commonnames[0]["language"], "ENG")
		self.assertEqual(self.xmltest.commonnames[0]["name"], "Test name")
		self.assertEqual(self.xmltest.modeltypes, ["HSI"])

	def test_scan_modeltype(self):
		self.xmltest._scan()
		self.xmltest._scan_modeltype(self.xmltest.modeltypes[0])
		self.assertEqual(self.xmltest.systems, ["testsystem"])

	def test__read_contentdescription(self):
		spd_overview = self.xmltest._read_contentdescription()
		testtext = '''Test
	Test'''
		self.assertEqual(spd_overview[0]["description"],testtext)

	def test_scan_knowledgerules(self):
		self.xmltest._scan()
		self.xmltest._scan_modeltype(self.xmltest.modeltypes[0])
		
		#test first system
		self.xmltest._scan_knowledgerules(modeltypename = self.xmltest.modeltypes[0], systemname = self.xmltest.systems[0])
		self.assertEqual(self.xmltest.systemname, "testsystem","Error occurs at system :" + self.xmltest.systems[0])
		self.assertEqual(self.xmltest.knowledgeRulesNr,5,"Error occurs at system :" + self.xmltest.systems[0])
		self.assertEqual(self.xmltest.knowledgeRulesCategorie,["ResponseCurve","ResponseCurve","ResponseCurve",\
														"ResponseCurve","FormulaBased"],"Error occurs at system :" + self.xmltest.systems[0]) 
		# self.assertTrue(isinstance(self.xmltest.knowledgeRulesDict,dict),"Error occurs at model :" + cur_model) 
		self.assertEqual(self.xmltest.knowledgeRulesNames,["Chloride","Soil","SiltFraction",\
													"WaterdepthLakes","P_chara_extinction"],"Error occurs at model :" + self.xmltest.systems[0])
		self.assertEqual(self.xmltest.knowledgeRulesStatistics,["minimum","average","average","average","none"],\
													"Error occurs at system :" + self.xmltest.systems[0])
		self.assertEqual(self.xmltest.knowledgeRulesUnits,['g/l','soil','silt fraction / description','m','-'],\
													"Error occurs at system :" + self.xmltest.systems[0])
		self.assertTrue(all(elem in self.xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
								in self.xmltest.knowledgeRulesCategorie),"Error occurs at system :" + self.xmltest.systems[0])
	
	def test_read_write_systemdescription(self):
		test_language = "ENG"
		testtext = '''Test
TEST'''
		newtext = '''TestNew
TESTNEW'''
		self.xmltest._scan()
		self.xmltest._scan_modeltype(self.xmltest.modeltypes[0])
		#test first system
		syd_overview = self.xmltest._read_systemdescription(modeltypename = self.xmltest.modeltypes[0], systemname = self.xmltest.systems[0])
		self.assertEqual(syd_overview[0]["description"],testtext,"Error occurs at system :" + self.xmltest.systems[0])	
		self.xmltest._write_systemdescription(modeltypename = self.xmltest.modeltypes[0], systemname = self.xmltest.systems[0], language = test_language, text = newtext)
		syd_overview2 = self.xmltest._read_systemdescription(modeltypename = self.xmltest.modeltypes[0], systemname = self.xmltest.systems[0])
		self.assertEqual(syd_overview2[0]["description"],newtext,"Error occurs at system :" + self.xmltest.systems[0])	
			


	def test_get_response_curve(self):
		pass
		#TO BE FILLED


	def test_plot_response_curve(self):
		pass
		#TO BE FILLED


def _run_unittests():
	global BUILTIN_FUNCTION_OPEN
	BUILTIN_FUNCTION_OPEN = __builtins__.__dict__['open']
	restore_builtin_open()
	unittest.main()

if __name__ == '__main__':
	_run_unittests()

# xmltest = AutecologyXML("examples/Anguilla anguilla.xml")
# xmltest = AutecologyXML("examples/Dreissena_polymorpha.xml")
# xmltest._readxml()
# xmltest._scan()
# print(xmltest.latinname)
# print(xmltest.models)

# xmltest._scan_knowledgerules("adult")
# print(xmltest.knowledgeRulesCategorie)
# print(xmltest.knowledgeRulesStatistics)

# print(xmltest._read_speciesdescription())
# print(xmltest._read_modeldescription("adult"))

#This is an example.

#It contains a new text.

#Lets see if it works.
#'''
#xmltest._write_modeldescription("adult",new_text_example)

#print(xmltest._read_modeldescription("adult"))

#xmltest._writexml("examples/test.xml")

#rc_tag = xmltest.get_element_response_curve(modelname = "adult", rcname = "Acidity")
#rc_tag = xmltest.get_element_response_curve(modelname = "adult", rcname = "Soil")
# rc_tag = xmltest.get_element_response_curve(modelname = "adult", rcname = "SiltFraction")
# rc_tag = xmltest.get_element_response_curve(modelname = "adult", rcname = "WaterdepthLakes")
# rc_data = xmltest.get_data_response_curve_data(rc_tag)
# fig, axes = xmltest.visualize_rc(rc_data)
# plt.show()
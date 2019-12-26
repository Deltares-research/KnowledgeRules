from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *

from log4net import LogManager as _LogManager

import os # for reading paths
import csv # for reading and writing *.csv files
#from lxml import etree as ET #NOT AVAILABLE FOR DELTASHELL
#import pandas #NOT AVAILABLE FOR DELTASHELL
import xml.etree.ElementTree as ET # for reading and writing *.xml files
from collections import OrderedDict 

_AutecologyXMLLogger = _LogManager.GetLogger("AutecologyXMLFunctions")

def make_find(element_name_list):
	#configuration
	xmlns = "{http://www.wldelft.nl/fews}"

	#make find
	full_string = ""
	stop_slash = len(element_name_list)-1
	for nr, i in enumerate(element_name_list):
		full_string = full_string + xmlns +  i
		if(nr != stop_slash):
			full_string = full_string + "/"
		else:
			pass
	return(full_string)


def make_flowdiagram_dict(root,systemname):
	#1. read the species and system specific flowdiagrams

	#configuration
	modeltypename = "HSI"
	
	# get system type tag
	type_tag_modeltype = root.findall(make_find(["Autecology","ModelType"]))
	type_tag_applicable_modeltype = [f for f in type_tag_modeltype if(modeltypename in f.get("name"))]
	type_tag_system = type_tag_applicable_modeltype[0].findall(make_find(["System"]))
	type_tag_applicable_system = [e for e in type_tag_system if(systemname in e.get('name'))]
	system_root = type_tag_applicable_system[0]

	# get system flow diagrams type tag
	type_tag_systemflowdiagram = system_root.find(make_find(["SystemFlowDiagrams"]))

	#0. Make flow diagram structures
	syfd_overview = []
	for syfd in type_tag_systemflowdiagram:
		flow_diagram_name = syfd.get("name")
		from_overview = []
		for fromlink in syfd:
			fromname = fromlink.get("name")
			label = fromlink.find(make_find(["label"])).text
			equation = fromlink.find(make_find(["equation"])).text
			to = [tolink.text.replace('"','') for tolink in fromlink.findall(make_find(["To"]))]
			from_overview.append(OrderedDict([("from", fromname),("label",label),("equation",equation),("to",to)]))
		syfd_overview.append(OrderedDict([("name",flow_diagram_name),("structure",from_overview)]))

	return(syfd_overview)

def make_knowledgerules_dict(root,systemname):
	# 1 . read the species specific information and response curves

	#configuration
	XMLconvention = {}
	XMLconvention["rc"] = "ResponseCurve"
	XMLconvention["fb"] = "FormulaBased"
	modeltypename = "HSI"

	# get species type tag
	type_tag_species =  root.findall(make_find(["Topic","Species"]))
	species_root = type_tag_species[0]

	# get system type tag
	type_tag_modeltype = root.findall(make_find(["Autecology","ModelType"]))
	type_tag_applicable_modeltype = [f for f in type_tag_modeltype if(modeltypename in f.get("name"))]
	type_tag_system = type_tag_applicable_modeltype[0].findall(make_find(["System"]))
	type_tag_applicable_system = [e for e in type_tag_system if(systemname in e.get('name'))]
	system_root = type_tag_applicable_system[0]

	# 1. Make repsonse curves dictionary
	autecology_overview = {}
	autecology_overview["EoLCode"] = species_root.find(make_find(['EoLpagenr'])).text
	autecology_overview["latinname"] = species_root.find(make_find(['LatName'])).text
	autecology_overview["commonname"] = species_root.find(make_find(['CommonNames'])).text
	autecology_overview["systemname"] = system_root.get('name')
	autecology_overview["knowledgerules"] = {}

	kr_dict = {}
	for rc_element in system_root.findall(make_find(["KnowledgeRules","ResponseCurve"])):
		_AutecologyXMLLogger.Info("Processing Response Curve : " + rc_element.get('name'))

		response_curve_dict = {}
		response_curve_dict["name"] = rc_element.get('name').replace('"','')
		response_curve_dict["KnowledgeruleCategorie"] = XMLconvention["rc"]
		response_curve_dict["type"] = rc_element.find(make_find(['type'])).text.replace('"','')
		response_curve_dict["layername"] = rc_element.find(make_find(['layername'])).text.replace('"','')
		response_curve_dict["unit"] = rc_element.find(make_find(['unit'])).text.replace('"','')
		response_curve_dict["statistic"] = rc_element.find(make_find(['statistic'])).text.replace('"','')

		parameter_list = []
		if(response_curve_dict["type"] == "scalar"):
			find_scalar = make_find(["valuesScalar","parameter"])
			column_names = rc_element.findall(find_scalar)[0].keys()
			for parameter in rc_element.findall(find_scalar):
				parameter_list.append([float(parameter.get("value")),float(parameter.get("HSI"))])
		elif(response_curve_dict["type"] == "categorical"):
			find_categorical = make_find(["valuesCategorical","parameter"])
			column_names = rc_element.findall(find_categorical)[0].keys()
			for parameter in rc_element.findall(find_categorical):
				parameter_list.append([str(parameter.get("cat")),float(parameter.get("HSI"))])
		elif(response_curve_dict["type"] == "ranges"):
			find_ranges = make_find(["valuesRanges","parameter"])
			column_names = rc_element.findall(find_ranges)[0].keys()
			for parameter in rc_element.findall(find_ranges):
				parameter_list.append([float(parameter.get("rangemin")),float(parameter.get("rangemax")),float(parameter.get("HSI"))])
		elif(response_curve_dict["type"] == "range / categorical"):
			find_rangecategorical = make_find(["valuesRangeCategorical","parameter"])
			column_names = rc_element.findall(find_rangecategorical)[0].keys()
			for parameter in rc_element.findall(find_rangecategorical):
				parameter_list.append([float(parameter.get("rangemin")),float(parameter.get("rangemax")),str(parameter.get("cat")),float(parameter.get("HSI"))])
		else:
			_AutecologyXMLLogger.Error("type "+ response_curve_dict["type"] + " is not available.")
			return()

		response_curve_dict["rule"] = parameter_list  #NO PANDAS AVAILABLE
		kr_dict[response_curve_dict["name"]] = response_curve_dict

	for fb_element in system_root.findall(make_find(["KnowledgeRules","FormulaBased"])):
		_AutecologyXMLLogger.Info("Processing Formula Based : " + fb_element.get('name'))

		formula_based_dict = {}
		formula_based_dict["name"] = fb_element.get('name').replace('"','')
		formula_based_dict["KnowledgeruleCategorie"] = XMLconvention["fb"]
		# formula_based_dict["type"] = rc_element.find('type').text.replace('"','')
		formula_based_dict["layername"] = fb_element.find(make_find(['layername'])).text.replace('"','')
		formula_based_dict["unit"] = fb_element.find(make_find(['unit'])).text.replace('"','')
		formula_based_dict["statistic"] = fb_element.find(make_find(['statistic'])).text.replace('"','')
		formula_based_dict["output"] = fb_element.find(make_find(['output'])).text.replace('"','')
		formula_based_dict["equation_text"] = fb_element.find(make_find(['equation'])).text.replace('"','').replace('^','**')
		

		formula_based_dict["parameters"] = [] 
		#Get the number of values under Parameteers
		fb_values_tags = fb_element.findall(make_find(["Parameters","valuesScalar"])) + \
						fb_element.findall(make_find(["Parameters","valuesConstant"])) 
		for values in fb_values_tags:
			parameter_dict = {}
			parameter_dict["dataname"] = values.get("dataname")
			parameter_dict["type"] = values.get("type")
			parameter_dict["unit"] = values.get("unit")

			#Get data per Values, assess the type and store it.
			parameter_list = []
			if(parameter_dict["type"] == "constant"):
				for parameter in values.findall(make_find(["parameter"])):
					parameter_list.append([str(parameter.get("constantset")), float(parameter.get("value"))])
			elif(parameter_dict["type"] == "scalar"):
				for parameter in values.findall(make_find(["parameter"])):
					parameter_list.append([float(parameter.get("min")), float(parameter.get("max"))])
			else:
				_AutecologyXMLLogger.Error("type "+ parameter_dict["type"] + " is not available.")
				return()

			column_names = values.findall(make_find(["parameter"]))[0].keys()
			parameter_dict["data"] = parameter_list #NO PANDAS AVAILABLE
			formula_based_dict["parameters"].append(parameter_dict)
			kr_dict[formula_based_dict["name"]] = formula_based_dict

	#store all in one dictonary
	autecology_overview["knowledgerules"] = kr_dict
	return(autecology_overview)


def get_flow_diagram_structure(flow_diagram_overview, flow_diagram_name):
	diagram = [struct["structure"] for struct in flow_diagram_overview if(struct["name"] == flow_diagram_name)]
	if(len(diagram) == 0):
		_AutecologyXMLLogger.Error("No flow diagram structure found with the name :" + flow_diagram_name + ".")
		return()
	else:
		structure = OrderedDict()
		for fromlink in diagram[0]:
			structure[fromlink["from"]] = fromlink["to"]

	return(structure)

def get_flow_diagram_equations(flow_diagram_overview,flow_diagram_name):
	diagram = [struct["structure"] for struct in flow_diagram_overview if(struct["name"] == flow_diagram_name)]
	if(len(diagram) == 0):
		_AutecologyXMLLogger.Error("No flow diagram structure found with the name :" + flow_diagram_name + ".")
		return()
	else:
		equations = OrderedDict()
		for fromlink in diagram[0]:
			equations[fromlink["from"]] = fromlink["equation"]

	return(equations)

def make_hyrarchical_model_structure(structure):
	#2. Setup model structure
	### !!! NEEDS TO BE AUTOMISED BASED ON FlowDiagram
	model_list = []
	HSI_list = []
	for nr, key in enumerate(structure.keys()):

		if(nr == 0):
			# Create main composite model
			model_list.append(CreateModel(HabitatModelType.CompositeModel))
			model_list[0].Name = key
		else:
			# Create composite model and add to main
			model_list.append(CreateModel(HabitatModelType.CompositeModel))
			model_list[nr].Name = key
			model_list[0].Activities.Add(model_list[nr])

			#make formula based calculation
			HSI_list.append(CreateModel(HabitatModelType.FormuleBased))
			HSI_list[nr-1].Name = "HSI_" + model_list[nr].Name
			HSI_list[nr-1].InputGridCoverages.Clear() # Remove default grid 
			HSI_list[nr-1].Formulas.Clear() # remove output grid

	# Add main model to project
	AddToProject(model_list[0])
	return((model_list, HSI_list))


def make_knowledgerule_models(structure,response_curves_overview, model_list):
	#3. fill composite models with hsi models
	knowledgerules_list = []
	for nr2, knwlrl2 in enumerate(response_curves_overview.keys()):

		# All these model types can be added in the 'CreateModel' function below
		knwlrl_categorie2 = response_curves_overview[knwlrl2]["KnowledgeruleCategorie"]
		if(knwlrl_categorie2 == "ResponseCurve"):
			if(response_curves_overview[knwlrl2]["type"] == "scalar"):

				# Create linear reclassification models
				knowledgerules_list.append(CreateModel(HabitatModelType.BrokenLinearReclassification))
				knowledgerules_list[nr2].Name = knwlrl2
				knowledgerules_list[nr2].InputGridCoverages.Clear()

				#add to correct model
				for nr, key in enumerate(structure.keys()):
					if(knowledgerules_list[nr2].Name in structure[key]):
						model_list[nr].Activities.Add(knowledgerules_list[nr2])

			else:
				_AutecologyXMLLogger.Warn("Current responsecurve type is not yet available :" +\
						autecology_dict["knowledgerules"][knwlrl2]["type"])

		elif(knwlrl_categorie2 == "FormulaBased"):
			knowledgerules_list.append(CreateModel(HabitatModelType.FormuleBased))
			knowledgerules_list[nr2].Name = knwlrl2
			knowledgerules_list[nr2].InputGridCoverages.Clear()
			knowledgerules_list[nr2].Formulas.Clear()

		else:
			_AutecologyXMLLogger.Warn("Current knowledge rule categorie is not yet available :" +\
						knwlrl_categorie2)

	return(knowledgerules_list)

def add_HSI_collection_models(structure, model_list, HSI_list):
	#4. add  hsi models per sub folder
	for nr, key in enumerate(structure.keys()):
		if(nr == 0):
			continue
		else:	
			model_list[nr].Activities.Add(HSI_list[nr-1])

	return((model_list,HSI_list))

def fill_knowledgerule_models(InputDir, response_curves_overview, knowledgerules_list):
	#5. fill  hsi models
	input_list = []	
	for nr3, knwlrl3 in enumerate(knowledgerules_list):

		#load input if file exists (currently only ASCI files)
		knwlrl_layername3 = response_curves_overview[knwlrl3.Name]["layername"]
		knwlrl_categorie3 =  response_curves_overview[knwlrl3.Name]["KnowledgeruleCategorie"]
		if(os.path.exists(os.path.join(InputDir, knwlrl_layername3 + ".asc"))):
			input_list.append(ImportMapFromFile(os.path.join(InputDir, knwlrl_layername3 + ".asc")))
			knowledgerules_list[nr3].InputGridCoverages.Add(input_list[nr3])
		else:
			input_list.append(CreateEmptyMap())
			knowledgerules_list[nr3].InputGridCoverages.Add(input_list[nr3])
			_AutecologyXMLLogger.Warn("Automatic layer loading failed : " + knwlrl_layername3 + ".asc "+\
						  " not found for knowledgerule " + knwlrl3.Name + ". Load layer manually or remove rule.")

		#load knowledge rule to HSI model
		if(knwlrl_categorie3 == "ResponseCurve"):
			if(response_curves_overview[knwlrl3.Name]["type"] == "scalar"):
				for line in response_curves_overview[knwlrl3.Name]["rule"]:
					#add scalar value and HSI value
					AddBrokenLinearReclassificationRow(knowledgerules_list[nr3], line[0], line[1])

			else:
				_AutecologyXMLLogger.Warn("Current responsecurve type is not yet available :" +\
						autecology_dict["knowledgerules"][knwlrl3.Name]["type"] + ". "+\
						"Classification was not added")


		elif(knwlrl_categorie3 == "FormulaBased"):
			_AutecologyXMLLogger.Error("Current knowledge rule categorie is not yet available :" +\
						knwlrl_categorie3 + ". "+\
						"Classification was not added")

		else:
			_AutecologyXML.Warn("Current knowledge rule categorie is not yet available :" +\
						knwlrl_categorie3)

	return((knowledgerules_list, input_list))

def run_knowledgerule_models(knowledgerules_list):
	#6. run  hsi models
	for nr4, knwlrl4 in enumerate(knowledgerules_list):
		RunModel(knowledgerules_list[nr4],True)
		knowledgerules_list[nr4].OutputGridCoverages[0].Name = knwlrl4.Name + "_hsi"
	return(knowledgerules_list)

def connect_and_run_hyrarchical_structure(structure, equations, HSI_list, knowledgerules_list):
	#7. connect submodels (current situation is that always the minimum of all HSI will be taken)
	HSI_equation = []
	for nr5, revhsimodel5 in enumerate(reversed(HSI_list)):

		# Redirect output of submodels as input to new model
		origin_model_name = revhsimodel5.Name.replace("HSI_","")
		
		for submodel in structure[origin_model_name]:
			for nr6, knwlrl5 in enumerate(knowledgerules_list):
				if(knwlrl5.Name == submodel):
					revhsimodel5.InputGridCoverages.Add(CreateEmptyMap()) # add new map to formula based model

		countnr = 0
		for submodel in structure[origin_model_name]:
			for nr6, knwlrl5 in enumerate(knowledgerules_list):
				if(knwlrl5.Name == submodel):
					if(countnr == 0): 
						LinkMaps(knwlrl5, knwlrl5.Name + "_hsi", revhsimodel5, "Grid")
					else:
						LinkMaps(knwlrl5, knwlrl5.Name + "_hsi", revhsimodel5, "Grid_" + str(countnr))
					countnr = countnr + 1

		if(equations[origin_model_name] == "min"):
			HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5, "min("+ ",".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ")"))
		elif(equations[origin_model_name] == "max"):
			HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5, "max("+ ",".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ")"))
		else:
			_AutecologyXML.Warn("Current equation for HSI model structure is not yet available :" +\
						equations[origin_model_name])
		
		revhsimodel5.Formulas.Add(HSI_equation[nr5])
		RunModel(revhsimodel5, True)

	return(HSI_list)

def export_model_results(OutputDir, HSI_list):
	#8. Export submodel results
	for nr6, revhsimodel6 in enumerate(reversed(HSI_list)):
		origin_model_name = revhsimodel6.Name.replace("_hsi","")
		WriteToAsc(revhsimodel6.OutputGridCoverages[0], os.path.join(OutputDir, origin_model_name + "_HSI.asc"))
	return()
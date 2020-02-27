from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *

from log4net import LogManager as _LogManager

import os # for reading paths
import csv # for reading and writing *.csv files
import copy #for deepcopy
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

def get_data_layer(layer_element):

	layer_dict = {}
	layer_dict["layername"] = layer_element.get('name').replace('"','')
	layer_dict["parameter_cat"] = layer_element.find(make_find(['parameter_cat'])).text.replace('"','')
	layer_dict["layer_filename"] = layer_element.find(make_find(['layer_filename'])).text.replace('"','')
	layer_dict["unit"] = layer_element.find(make_find(['unit'])).text.replace('"','')
	layer_dict["statistic"] = layer_element.find(make_find(['statistic'])).text.replace('"','')
	layer_dict["description"] = layer_element.find(make_find(['description'])).text.replace('"','')

	return(layer_dict)

def get_data_layers(sp_kr_element,element_find):
	layers = OrderedDict()	
	for layer in sp_kr_element.findall(element_find):
		layer_dict = get_data_layer(layer)
		layers[layer_dict["layername"]] = layer_dict

	return(layers)


def make_flowdiagram_dict(root,systemname):
	#1. read the species and system specific flowdiagrams

	#configuration
	modeltypename = "HSI"
	
	# get system type tag
	type_tag_modeltype = root.findall(make_find(["Autecology","ModelType"]))
	type_tag_applicable_modeltype = [f for f in type_tag_modeltype if(modeltypename in f.get("name"))]
	type_tag_system = type_tag_applicable_modeltype[0].findall(make_find(["System"]))
	type_tag_applicable_system = [e for e in type_tag_system if(systemname in e.get("name"))]
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
	XMLconvention["mr"] = "MultipleReclassification"
	modeltypename = "HSI"

	# get species type tag
	type_tags =  root.findall(make_find(["Topic","Species"])) +  root.findall(make_find(["Topic","WFDIndicator"])) +\
		 root.findall(make_find(["Topic","Habitats"]))

	type_tag_root =  type_tags[0]
	
	# get system type tag
	type_tag_modeltype = root.findall(make_find(["Autecology","ModelType"]))
	type_tag_applicable_modeltype = [f for f in type_tag_modeltype if(modeltypename in f.get("name"))]
	type_tag_system = type_tag_applicable_modeltype[0].findall(make_find(["System"]))
	type_tag_applicable_system = [e for e in type_tag_system if(systemname in e.get('name'))]
	system_root = type_tag_applicable_system[0]

	# 1. Make repsonse curves dictionary
	autecology_overview = {}
	if(type_tag_root.tag == make_find(["Species"])):
		autecology_overview["Topic"] = "Species"
		autecology_overview["EoLCode"] = type_tag_root.find(make_find(['EoLpagenr'])).text
		autecology_overview["latinname"] = type_tag_root.find(make_find(['LatName'])).text
	elif(type_tag_root.tag == make_find(["WFDIndicator"])):
		autecology_overview["Topic"] = "WFDIndicator"
		pass
	elif(type_tag_root.tag == make_find(["Habitats"])):
		autecology_overview["Topic"] = "Habitats"
		pass
	autecology_overview["commonnames"] = [{"name" : cn.get("name"), "language" : cn.get("language")}\
								 for cn in type_tag_root.find(make_find(['CommonNames']))]
	
	autecology_overview["systemname"] = system_root.get('name')
	autecology_overview["knowledgerules"] = {}

	kr_dict = {}
	for rc_element in system_root.findall(make_find(["KnowledgeRules","ResponseCurve"])):
		_AutecologyXMLLogger.Info("Processing Response Curve : " + rc_element.get('name'))

		
		Content = rc_element.find(make_find(["Content"]))
		
		response_curve_dict = {}
		response_curve_dict["name"] = rc_element.get('name').replace('"','')
		response_curve_dict["KnowledgeruleCategorie"] = XMLconvention["rc"]
		response_curve_dict["type"] = Content.find(make_find(['type'])).text.replace('"','')
		#get input layers
		find_inputLayers = make_find(["inputLayers","layer"])
		response_curve_dict["inputLayers"] = get_data_layers(rc_element, find_inputLayers) 
		#get output layers
		find_outputLayers = make_find(["outputLayers","layer"])
		response_curve_dict["outputLayers"] = get_data_layers(rc_element, find_outputLayers) 

		parameter_list = []
		if(response_curve_dict["type"] == "scalar"):
			find_scalar = make_find(["valuesScalar","parameter"])
			column_names = Content.findall(find_scalar)[0].keys()
			for parameter in Content.findall(find_scalar):
				parameter_list.append([float(parameter.get("input")),float(parameter.get("output"))])
		elif(response_curve_dict["type"] == "categorical"):
			find_categorical = make_find(["valuesCategorical","parameter"])
			column_names = Content.findall(find_categorical)[0].keys()
			for parameter in Content.findall(find_categorical):
				parameter_list.append([float(parameter.get("input")), str(parameter.get("input_cat")),\
					float(parameter.get("output")), str(parameter.get("output_cat"))])
		elif(response_curve_dict["type"] == "ranges"):
			find_ranges = make_find(["valuesRanges","parameter"])
			column_names = Content.findall(find_ranges)[0].keys()
			for parameter in Content.findall(find_ranges):
				parameter_list.append([float(parameter.get("rangemin_input")), float(parameter.get("rangemax_input")),\
					float(parameter.get("output"))])
		elif(response_curve_dict["type"] == "range / categorical"):
			find_rangecategorical = make_find(["valuesRangeCategorical","parameter"])
			column_names = Content.findall(find_rangecategorical)[0].keys()
			for parameter in Content.findall(find_rangecategorical):
				parameter_list.append([float(parameter.get("rangemin_input")), float(parameter.get("rangemax_input")),\
				 	str(parameter.get("input_cat")), float(parameter.get("output")), str(parameter.get("output_cat"))])
		else:
			_AutecologyXMLLogger.Error("type "+ str(response_curve_dict["type"]) + " is not available.")
			return()

		response_curve_dict["rule"] = parameter_list  #NO PANDAS AVAILABLE
		kr_dict[response_curve_dict["name"]] = response_curve_dict

	for fb_element in system_root.findall(make_find(["KnowledgeRules","FormulaBased"])):
		_AutecologyXMLLogger.Info("Processing Formula Based : " + fb_element.get('name'))

		Content = fb_element.find(make_find(["Content"]))

		formula_based_dict = {}
		formula_based_dict["name"] = fb_element.get('name').replace('"','')
		formula_based_dict["KnowledgeruleCategorie"] = XMLconvention["fb"]
		formula_based_dict["equation_text"] = Content.find(make_find(['equation'])).text.replace('"','').replace('^','**')
		#get input layers
		find_inputLayers = make_find(["inputLayers","layer"])
		formula_based_dict["inputLayers"] = get_data_layers(fb_element, find_inputLayers) 
		#get output layers
		find_outputLayers = make_find(["outputLayers","layer"])
		formula_based_dict["outputLayers"] = get_data_layers(fb_element, find_outputLayers) 
		

		formula_based_dict["parameters"] = [] 
		#Get the number of values under Parameteers
		fb_values_tags = Content.findall(make_find(["Parameters","valuesScalar"])) + \
						Content.findall(make_find(["Parameters","valuesConstant"])) 
		for values in fb_values_tags:
			parameter_dict = {}
			parameter_dict["layername"] = values.get("layername")
			parameter_dict["type"] = values.get("type")

			#Get data per Values, assess the type and store it.
			parameter_list = []
			if(parameter_dict["type"] == "constant"):
				for parameter in values.findall(make_find(["parameter"])):
					parameter_list.append([float(parameter.get("input")), str(parameter.get("input_cat")), float(parameter.get("output"))])
			elif(parameter_dict["type"] == "scalar"):
				for parameter in values.findall(make_find(["parameter"])):
					parameter_list.append([float(parameter.get("min_input")), float(parameter.get("max_input"))])
			else:
				_AutecologyXMLLogger.Error("type "+ str(parameter_dict["type"]) + " is not available.")
				return()

			column_names = values.findall(make_find(["parameter"]))[0].keys()
			parameter_dict["data"] = parameter_list #NO PANDAS AVAILABLE
			formula_based_dict["parameters"].append(parameter_dict)

		kr_dict[formula_based_dict["name"]] = formula_based_dict

	for mr_element in system_root.findall(make_find(["KnowledgeRules","MultipleReclassification"])):
		_AutecologyXMLLogger.Info("Processing Multiple Reclassification : " + mr_element.get('name'))

		Content = mr_element.find(make_find(["Content"]))

		multiple_reclassifiation_dict = {}
		multiple_reclassifiation_dict["name"] = mr_element.get('name').replace('"','')
		multiple_reclassifiation_dict["KnowledgeruleCategorie"] = XMLconvention["mr"]
		#get input layers
		find_inputLayers = make_find(["inputLayers","layer"])
		multiple_reclassifiation_dict["inputLayers"] = get_data_layers(mr_element, find_inputLayers) 
		#get output layers
		find_outputLayers = make_find(["outputLayers","layer"])
		multiple_reclassifiation_dict["outputLayers"] = get_data_layers(mr_element, find_outputLayers) 
		

		multiple_reclassifiation_dict["parameters"] = [] 
		#Get the number of values under Parameteers
		mr_values_tags = Content.findall(make_find(["Parameters","valuesRangeCategorical"]))
		
		for values in mr_values_tags:
			parameter_dict = {}
			parameter_dict["layername"] = values.get("layername")
			parameter_dict["type"] = values.get("type")

			parameter_list = []
			if(parameter_dict["type"] == "range / categorical"):
				for parameter in values.findall(make_find(["parameter"])):
					parameter_list.append([float(parameter.get("rangemin_input")), float(parameter.get("rangemax_input")),\
						str(parameter.get("input_cat")), float(parameter.get("output")), str(parameter.get("output_cat"))])

			else:
				_AutecologyXMLLogger.Error("type "+ str(parameter_dict["type"]) + " is not available.")
				return()

			column_names = values.findall(make_find(["parameter"]))[0].keys()
			parameter_dict["data"] = parameter_list #NO PANDAS AVAILABLE
			multiple_reclassifiation_dict["parameters"].append(parameter_dict)
			
		
		kr_dict[multiple_reclassifiation_dict["name"]] = multiple_reclassifiation_dict


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

def make_hyrarchical_model_structure(topic_name, structure,equations):
	#2. Setup model structure
	### !!! NEEDS TO BE AUTOMISED BASED ON FlowDiagram
	model_list = []
	HSI_list = []
	build_struct = {}
	struct_index = {}

	# Create main composite model
	model_list.append(CreateModel(HabitatModelType.CompositeModel))
	model_list[0].Name = topic_name

	count_HSI_nr = 0

	for nr, key in enumerate(structure.keys()):
		build_struct[key] = structure[key]		
		struct_index[key] = nr + 1
		if(nr == 0):
			# Create composite model and add to main
			model_list.append(CreateModel(HabitatModelType.CompositeModel))
			model_list[nr + 1].Name = key
			model_list[0].Activities.Add(model_list[nr + 1])

		else:
			#get higher composite model
			index_list = [struct_index[build_key] for build_key in build_struct.keys() if(key in build_struct[build_key])]
			if(len(index_list) != 1):
				_AutecologyXMLLogger.Error("Doubling flow diagram structure found with the name :" + key + ".")
				return()

			#get index
			index_comp = index_list[0]

			# Create composite model and add to main
			model_list.append(CreateModel(HabitatModelType.CompositeModel))
			model_list[nr + 1].Name = key
			model_list[index_comp].Activities.Add(model_list[nr + 1])

		#make formula based calculation
		if(equations[key] == "knowledge_rule"):
			continue
		else:
			HSI_list.append(CreateModel(HabitatModelType.FormuleBased))
			HSI_list[count_HSI_nr].Name = "HSI_" + model_list[nr + 1].Name
			HSI_list[count_HSI_nr].InputGridCoverages.Clear() # Remove default grid 
			HSI_list[count_HSI_nr].Formulas.Clear() # remove output grid

			count_HSI_nr = count_HSI_nr + 1

	# Add main model to project
	AddToProject(model_list[0])
	return((model_list, HSI_list))


def make_knowledgerule_models(structure,response_curves_overview, model_list):
	#3. fill composite models with hsi models
	knowledgerules_list = []
	
	#get model names
	structure_to_names = []
	for key, value in structure.items():
		structure_to_names = structure_to_names + value
	
	#subset response_curves_overview
	subset_knowledge_rules_overview = OrderedDict((k, response_curves_overview[k]) for k\
		 in structure_to_names if k in response_curves_overview)

	#loop over response curves overview
	for nr2, knwlrl2 in enumerate(subset_knowledge_rules_overview.keys()):

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
						model_list[nr + 1].Activities.Add(knowledgerules_list[nr2])

			elif((response_curves_overview[knwlrl2]["type"] == "categorical") or\
				(response_curves_overview[knwlrl2]["type"] == "ranges") or\
				(response_curves_overview[knwlrl2]["type"] == "range / categorical")):
				# Create linear reclassification models
				knowledgerules_list.append(CreateModel(HabitatModelType.MultiTableReclassification))
				knowledgerules_list[nr2].Name = knwlrl2
				knowledgerules_list[nr2].InputGridCoverages.Clear()

				#add to correct model
				for nr, key in enumerate(structure.keys()):
					if(knowledgerules_list[nr2].Name in structure[key]):
						model_list[nr + 1].Activities.Add(knowledgerules_list[nr2])

			else:
				_AutecologyXMLLogger.Error("Current responsecurve type is not yet available :" +\
						str(response_curves_overview[knwlrl2]["type"]))

		elif(knwlrl_categorie2 == "FormulaBased"):
			knowledgerules_list.append(CreateModel(HabitatModelType.FormuleBased))
			knowledgerules_list[nr2].Name = knwlrl2
			knowledgerules_list[nr2].InputGridCoverages.Clear()
			knowledgerules_list[nr2].Formulas.Clear()

			#add to correct model
			for nr, key in enumerate(structure.keys()):
				if(knowledgerules_list[nr2].Name in structure[key]):
					model_list[nr + 1].Activities.Add(knowledgerules_list[nr2])

		elif(knwlrl_categorie2 == "MultipleReclassification"):
			knowledgerules_list.append(CreateModel(HabitatModelType.MultiTableReclassification))
			knowledgerules_list[nr2].Name = knwlrl2
			knowledgerules_list[nr2].InputGridCoverages.Clear()
			
			#add to correct model
			for nr, key in enumerate(structure.keys()):
				if(knowledgerules_list[nr2].Name in structure[key]):
					model_list[nr + 1].Activities.Add(knowledgerules_list[nr2])

		else:
			_AutecologyXMLLogger.Error("Current knowledge rule categorie is not yet available :" +\
						knwlrl_categorie2)

	return(knowledgerules_list)

def add_HSI_collection_models(structure, equations, model_list, HSI_list):
	#4. add  hsi models per sub folder
	count_HSI_nr = 0
	for nr, key in enumerate(structure.keys()):
		if(equations[key] == "knowledge_rule"):
			continue
		else:
			model_list[nr + 1].Activities.Add(HSI_list[count_HSI_nr])
			count_HSI_nr = count_HSI_nr + 1

	return((model_list,HSI_list))

def fill_knowledgerule_models(InputDir, response_curves_overview, knowledgerules_list):
	#5. fill  hsi models
	input_list = []
	output_list = []	

	count_input = 0
	count_output = 0

	output_dict = OrderedDict()

	#reverse list to run lowest level input first
	revknowledgerules_list = list(reversed(knowledgerules_list))
	for nr3, revknwlrl3 in enumerate(revknowledgerules_list):

		#get knowledgerule categorie
		knwlrl_categorie3 =  response_curves_overview[revknwlrl3.Name]["KnowledgeruleCategorie"]

		#load input if file exists (currently only ASCI files)
		inputlayers = response_curves_overview[revknwlrl3.Name]["inputLayers"]
		outputlayers = response_curves_overview[revknwlrl3.Name]["outputLayers"]
		
		#collected all outputlayers created for potential input in next model
		outputnames = [rn for rn in output_dict.keys()]
		
		#Create input layers
		for nr, layername in enumerate(inputlayers.keys()):
			layer_details = inputlayers[layername]
			knwlrl_layerfilename3 = layer_details["layer_filename"]


			if(layername in outputnames):
				#load layer from previous calculation
				index_nr = outputnames.index(layername)
				input_list.append(CreateEmptyMap())
				revknowledgerules_list[nr3].InputGridCoverages.Add(input_list[count_input])

			elif(os.path.exists(os.path.join(InputDir, knwlrl_layerfilename3 + ".asc"))):
				#load layer from ascii file
				input_list.append(ImportMapFromFile(os.path.join(InputDir, knwlrl_layerfilename3 + ".asc")))
				revknowledgerules_list[nr3].InputGridCoverages.Add(input_list[count_input])

			else:
				#leave layer empty
				input_list.append(CreateEmptyMap())
				revknowledgerules_list[nr3].InputGridCoverages.Add(input_list[count_input])
				_AutecologyXMLLogger.Warn("Automatic layer loading failed : " + str(knwlrl_layerfilename3) + ".asc "+\
							  " not found for knowledgerule " + str(revknwlrl3.Name) + ". Load layer manually or remove rule.")

			
			revknowledgerules_list[nr3].InputGridCoverages[nr].Name = "_" +  layername

			#Link layers if already in outputs
			if(layername in outputnames):
				for nr_made, knrl_made in enumerate(revknowledgerules_list):
					for nr_outputgrid_made, outputgrid_made in enumerate(knrl_made.OutputGridCoverages):
						if(outputgrid_made.Name == revknowledgerules_list[nr3].InputGridCoverages[nr].Name):
							LinkMaps(revknowledgerules_list[nr_made],\
							 revknowledgerules_list[nr_made].OutputGridCoverages[nr_outputgrid_made].Name,\
							 revknowledgerules_list[nr3],\
							 revknowledgerules_list[nr3].InputGridCoverages[nr].Name)

			count_input = count_input + 1

		#load knowledge rule to HSI model
		if(knwlrl_categorie3 == "ResponseCurve"):
			if(response_curves_overview[revknwlrl3.Name]["type"] == "scalar"):
				for line in response_curves_overview[revknwlrl3.Name]["rule"]:
					#add scalar value and HSI value
					AddBrokenLinearReclassificationRow(revknowledgerules_list[nr3], float(line[0]), float(line[1]))

			elif(response_curves_overview[revknwlrl3.Name]["type"] == "categorical"):
				for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["rule"]):
					
					#create range input
					if(nr4 == 0):
						make_string = "<" + str(line[0]) + ", "+ str(line[0]) + "]"
					else:
						make_string = "<" + str(line[0]) + ", "+ str(line[0]) + "]"

					#add range / categorical value and HSI value	 
					AddMultiTableReclassificationRow(revknowledgerules_list[nr3], [make_string], float(line[2]), description = str(line[2]))

			elif(response_curves_overview[revknwlrl3.Name]["type"] == "ranges"):
				for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["rule"]):
					
					#create range input
					if(nr4 == 0):
						make_string = "[" + str(line[0]) + ", "+ str(line[1]) + "]"
					else:
						make_string = "<" + str(line[0]) + ", "+ str(line[1]) + "]"

					#add range / categorical value and HSI value	 
					AddMultiTableReclassificationRow(revknowledgerules_list[nr3], [make_string], float(line[2]), description = str(""))

			elif(response_curves_overview[revknwlrl3.Name]["type"] == "range / categorical"):
				for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["rule"]):
					
					#create range input
					if(nr4 == 0):
						make_string = "[" + str(line[0]) + ", "+ str(line[1]) + "]"
					else:
						make_string = "<" + str(line[0]) + ", "+ str(line[1]) + "]"

					#add range / categorical value and HSI value	 
					AddMultiTableReclassificationRow(revknowledgerules_list[nr3], [make_string], float(line[3]), description = str(line[2]))

			else:
				_AutecologyXMLLogger.Warn("Current responsecurve type is not yet available :" +\
						response_curves_overview[revknwlrl3.Name]["type"] + ". "+\
						"Classification was not added")


		elif(knwlrl_categorie3 == "FormulaBased"):
			
			#only for formula based a output grid is directly needed
			cur_output_layer_name = response_curves_overview[revknwlrl3.Name]["outputLayers"].keys()[0]
			
			equation_text =  response_curves_overview[revknwlrl3.Name]["equation_text"]
			revknowledgerules_list[nr3].Formulas.Add(CreateEquation(cur_output_layer_name, revknowledgerules_list[nr3], str(equation_text)))
			
			for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["parameters"]):
				if(line["type"] == "scalar"):
					pass
				elif(line["type"] == "constant"):
					_AutecologyXMLLogger.Warn("Current formulabased type is not yet available :" +\
						str(line["type"]) + ". "+\
						"Manual translation is required")

				else:
					_AutecologyXMLLogger.Warn("Current formulabased type is not yet available :" +\
						str(line["type"]) + ". "+\
						"Classification was not added")

		elif(knwlrl_categorie3 == "MultipleReclassification"):
			#check if all are range / categorical and collect unique output nrs
			output_values = []
			output_values_df = []
			for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["parameters"]):
				if(line["type"] == "range / categorical"):					
					for subline in line["data"]:
						output_values.append([subline[3],str(subline[4])])
				else:
					_AutecologyXMLLogger.Warn("Current multiplereclassification type is not yet available :" +\
						str(line["type"]) + ". "+\
						"Classification was not added")
			
			#make unique list
			output_values_ls = []
			for output in output_values:
				if(output not in output_values_ls):
					output_values_ls.append(output)

			output_values_df = copy.deepcopy(output_values_ls)
			for nr_ls, value_ls in enumerate(output_values_ls):
				for nr4, line in enumerate(response_curves_overview[revknwlrl3.Name]["parameters"]):
					in_subline = False
					for subline in line["data"]:
						if(value_ls[0] == subline[3]):
							make_string = "<" + str(subline[0]) + ", "+ str(subline[1]) + "]"
							output_values_df[nr_ls].append(make_string)
							
							in_subline = True

					if(in_subline == False):
						make_string = "<,>"
						output_values_df[nr_ls].append(make_string)

					if(len(output_values_df[nr_ls]) != (nr4+3)):
						_AutecologyXMLLogger.Warn("Current multiplereclassification has more values added than current column itteration : Column is " +\
						str(line["layername"]) + ", Values added are "+ str(output_values_df[nr_ls]) + " . "+\
						"Classification was not added")
						return()

			for input_line in output_values_df:
				#add range / categorical value and HSI value
				reclassification_settings = input_line[2:len(input_line)]	 
				AddMultiTableReclassificationRow(revknowledgerules_list[nr3], reclassification_settings, input_line[0], description = input_line[1])


		else:
			_AutecologyXMLLogger.Warn("Current knowledge rule categorie is not yet available :" +\
						str(knwlrl_categorie3))


		#Create output layer
		for nr, layername in enumerate(outputlayers.keys()):
			layer_details = outputlayers[layername]
			knwlrl_layerfilename3 = layer_details["layer_filename"]
			knwlrl_categorie3 =  response_curves_overview[revknwlrl3.Name]["KnowledgeruleCategorie"]

			if(len(revknowledgerules_list[nr3].OutputGridCoverages) > 0 and nr == 0):
				output_list.append(revknowledgerules_list[nr3].OutputGridCoverages[nr])
			else:
				output_list.append(CreateEmptyMap())
				revknowledgerules_list[nr3].OutputGridCoverages.Add(output_list[count_output])
				
			revknowledgerules_list[nr3].OutputGridCoverages[nr].Name = "_" + layername

			output_dict[layername] = str(revknowledgerules_list[nr3].OutputGridCoverages[nr].Name)

			count_output = count_output + 1



	#re-reverse knowledgerules_list
	knowledgerules_list = list(reversed(revknowledgerules_list))

	return((knowledgerules_list, input_list, output_list))
	
def run_knowledgerule_models(knowledgerules_list):
	#6. run  hsi models

	#reverse list to run lowest level input first
	revknowledgerules_list = list(reversed(knowledgerules_list)) 
	for nr4, revknwlrl4 in enumerate(revknowledgerules_list):

		#run the model
		RunModel(revknowledgerules_list[nr4],True)

	#re-reverse knowledgerules_list
	knowledgerules_list = list(reversed(revknowledgerules_list))

	return(knowledgerules_list)

def connect_hyrarchical_structure(structure, equations, HSI_list, knowledgerules_list):
	#7. connect submodels (current situation is that always the minimum of all HSI will be taken)
	
	complete_model_list = knowledgerules_list
	HSI_equation = []
	for nr5, revhsimodel5 in enumerate(reversed(HSI_list)):

		# Redirect output of submodels as input to new model
		origin_model_name = revhsimodel5.Name.replace("HSI_","")
		
		for submodel in structure[origin_model_name]:
			for nr6, cmknwlrl5 in enumerate(complete_model_list):
				if(cmknwlrl5.Name.replace("HSI_","") == submodel):
					revhsimodel5.InputGridCoverages.Add(CreateEmptyMap()) # add new map to formula based model

		countnr = 0
		for submodel in structure[origin_model_name]:
			for nr6, cmknwlrl5 in enumerate(complete_model_list):
				if(cmknwlrl5.Name.replace("HSI_","") == submodel):
					if(countnr == 0): 
						LinkMaps(cmknwlrl5, cmknwlrl5.OutputGridCoverages[0].Name, revhsimodel5, "Grid")
					else:
						LinkMaps(cmknwlrl5, cmknwlrl5.OutputGridCoverages[0].Name, revhsimodel5, "Grid_" + str(countnr))
					countnr = countnr + 1

		if(equations[origin_model_name] == "min"):
			HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5, "min("+ ",".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ")"))
		elif(equations[origin_model_name] == "max"):
			HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5, "max("+ ",".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ")"))
		elif(equations[origin_model_name] == "average"):
			HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5,  "(" + " + ".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ") / " + str(len(revhsimodel5.InputGridCoverages))))
		#elif(equations[origin_model_name] == "geometric_average"):
		#	HSI_equation.append(CreateEquation(revhsimodel5.Name, revhsimodel5, "areaaverage("+ ",".join([str(i) for i in revhsimodel5.InputGridCoverages])+ ")"))
		else:
			_AutecologyXMLLogger.Warn("Current equation for HSI model structure is not yet available :" +\
						equations[origin_model_name])
		
		revhsimodel5.Formulas.Add(HSI_equation[nr5])

		complete_model_list.append(revhsimodel5)

	return(HSI_list)

def run_hyrarchical_structure(HSI_list, equations):
	for revhsimodel6 in reversed(HSI_list):
		# get model name
		origin_model_name = revhsimodel6.Name.replace("HSI_","")
		if(equations[origin_model_name] != "knowledge_rule"):
			RunModel(revhsimodel6, True)
		else:
			_AutecologyXMLLogger.Warn("Current equation for HSI model structure is not yet available :" +\
						equations[origin_model_name])
		

	return(HSI_list)

def export_model_results(OutputDir, HSI_list, equations):
	#8. Export submodel results
	for nr7, revhsimodel7 in enumerate(reversed(HSI_list)):
		# get model name
		origin_model_name = revhsimodel7.Name.replace("HSI_","")
		if(equations[origin_model_name] != "knowledge_rule"):
			WriteToAsc(revhsimodel7.OutputGridCoverages[0], os.path.join(OutputDir, origin_model_name + "_HSI.asc"))
		else:
			_AutecologyXMLLogger.Warn("Current equation for HSI model structure is not yet available :" +\
						equations[origin_model_name])			

	return()
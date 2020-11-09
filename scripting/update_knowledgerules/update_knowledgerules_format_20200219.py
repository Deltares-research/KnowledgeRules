'''
Update all XMLS according to the new format

Changes are:

Structural changes:
	inputLayers, Content, outputLayers

layer :
	parameter_cat (added)
	layername -> layer_filename

Parameters
	valuesScalar (FormulaBased)
	@attribute dataname -> layername
	@attribute type (removed)
	@attribute unit (removed)
	min -> min_input
	max -> max_input

	valuesConstant (FormulaBased)
	@attribute dataname -> layername
	@attribute type (removed)
	@attribute unit (removed)
	input (added)
	constantset -> input_cat	
	value -> output

	valuesRangeCategorical (ResponseCurve, FormulaBased and MultiReclassification)
	@attribute name -> layername
	rangemin -> rangemin_input
	rangemax -> rangemax_input
	cat ->      input_cat
	HSI -> output
	output_cat (added)

ContentDescription -> TopicDescription

'''


import os
from lxml import etree
import sys
import shutil


sys.path.append("../scripting_library")
from autecology_xml import AutecologyXML


#INITIALISE

#path to "_knowledgerules"dir
path_kr_dir = "../../_knowledgerules/"

#path to update "_knowledgerules" dir
path_newkr_dir = "../../_new_knowledgerules/"

#path to XSD schema
path_xsd = "../../XMLSchema/AutecologyXML.xsd"

list_skip = ["Vegetationtypes_Northen_Delta.xml","Dreissena_polymorpha.xml","Chara spp.xml"]


def validate(xml_path: str, xsd_path: str) -> bool:
	'''
	Example taking from this Stackoverflow answer:
	https://stackoverflow.com/questions/299588/validating-with-an-xml-schema-in-python
	'''
	xmlschema_doc = etree.parse(xsd_path)
	xmlschema = etree.XMLSchema(xmlschema_doc)

	xml_doc = etree.parse(xml_path)
	result = xmlschema.validate(xml_doc)

	return result

#start log
log = []
nr_xmls = 0
log.append(["---Update log for KnowledgeRules xmls---"])
log.append([""])

#if the new dir does not exist, make it
if(os.path.isdir(path_newkr_dir)):
	pass
else:
	os.mkdir(path_newkr_dir)

#get all level1 dirs and loop over them
log.append(["- Structure and number of files"])
level1_dirs = [cur_dir for cur_dir in os.listdir(path_kr_dir) \
	if(os.path.isdir(os.path.join(path_kr_dir,cur_dir)))]
	
for level1_dir in level1_dirs :
	log.append(["  /"+ level1_dir])
	#get all level2 dirs and loop over them
	path_l1_dir = os.path.join(path_kr_dir,level1_dir) 
	level2_dirs = [cur_dir for cur_dir in os.listdir(path_l1_dir) \
		if(os.path.isdir(os.path.join(path_l1_dir,cur_dir)))] 

	#if the new subdir does not exist, make it
	if(os.path.isdir(os.path.join(path_newkr_dir, level1_dir))):
		pass
	else:
		os.mkdir(os.path.join(path_newkr_dir, level1_dir))


	for level2_dir in level2_dirs:
		log.append(["      /"+ level2_dir])
		#get all xml files in a level2 dir and loop over them		
		path_l2_dir = os.path.join(path_l1_dir,level2_dir) 
		xmls_l2_dir = [file for file in os.listdir(path_l2_dir) if(file.endswith(".xml"))]


		#if the new subdir does not exist, make it
		if(os.path.isdir(os.path.join(path_newkr_dir, level1_dir,level2_dir))):
			pass
		else:
			os.mkdir(os.path.join(path_newkr_dir, level1_dir,level2_dir))

		for xml_file in xmls_l2_dir:
			#add data to the log and count xmls
			path_xml_file = os.path.join(path_l2_dir,xml_file)

			if(xml_file in list_skip):
				shutil.copyfile(path_xml_file,os.path.join(path_newkr_dir, level1_dir,level2_dir, xml_file))
				continue


			log.append(["        /"+ xml_file])
			nr_xmls = nr_xmls + 1

			#load the xml file
			try:
				xmltest = AutecologyXML(filename = path_xml_file)
				xmltest._readxml()
			except:
				log.append(["XML could not be read with AutecologyXML : " + path_xml_file]) 
				continue

			#Replace text ContentDescription -> TopicDescription
			for element in xmltest.xmlroot.iter(xmltest.make_find(['ContentDescription'])):
				element.tag = 'TopicDescription'

			#update response curve elements
			#LOOP OVER ALL RESPONSE CURVES THEN SPECIFY FOR TYPE OF KNOWLEDGE RULE (CONTENT DIFFERENT)
			# NUMER OF INPUT LAYERS DIFFERENT
			knowledge_rule_element = xmltest.xmlroot.findall(xmltest.make_find(["Autecology","ModelType","System","KnowledgeRules"]))
			if(len(knowledge_rule_element) > 1):
				log.append(["XML has multiple systems : " + path_xml_file])
				continue 
			
			knowledge_rules_elements = knowledge_rule_element[0].findall(xmltest.make_find(['ResponseCurve'])) + knowledge_rule_element[0].findall(xmltest.make_find(['FormulaBased'])) + \
				knowledge_rule_element[0].findall(xmltest.make_find(['MultiReclassification']))

			
			for element in knowledge_rules_elements:
				
				#get data
				data_name = element.get("name")
				data_layer_name = element.find(xmltest.make_find(['layername'])).text
				data_unit = element.find(xmltest.make_find(['unit'])).text
				data_statistic = element.find(xmltest.make_find(['statistic'])).text
				data_description = element.find(xmltest.make_find(['description'])).text
				elem_author = element.find(xmltest.make_find(['author']))
				elem_date = element.find(xmltest.make_find(['date']))
				elem_references = element.find(xmltest.make_find(['references']))

				if(element.tag == xmltest.make_find(["ResponseCurve"])):
					data_type = element.find(xmltest.make_find(['type'])).text
					elem_values = element.findall(xmltest.make_find(['valuesScalar'])) + element.findall(xmltest.make_find(['valuesCategorical'])) + \
						element.findall(xmltest.make_find(['valuesRanges'])) + element.findall(xmltest.make_find(['valuesRangeCategorical']))

				if(element.tag == xmltest.make_find(["FormulaBased"])):
					elem_equation = element.find(xmltest.make_find(['equation']))
					data_output = element.find(xmltest.make_find(['output'])).text
					elem_parameters = element.find(xmltest.make_find(['Parameters']))

				if(element.tag == xmltest.make_find(["MultiReclassification"])):
					#not applicable for this conversion
					#as none has been setup yet
					log.append(["Unexpected MultiReclassification translated : " + path_xml_file])


				#create main elements
				inputLayers = etree.Element("inputLayers")
				Content = etree.Element("Content")
				outputLayers = etree.Element("outputLayers")

				if(element.tag == xmltest.make_find(["ResponseCurve"])):
					nr_input_layers = 1
				if(element.tag == xmltest.make_find(["FormulaBased"])):
					nr_input_layers = len(elem_parameters.getchildren())
					new_elem_Parameters = etree.Element("Parameters")

				#loop for inputlayers
				for i in range(1,nr_input_layers + 1):

					if(element.tag == xmltest.make_find(["ResponseCurve"])):
						elem_values = elem_values[0]
					else:
						elem_values = elem_parameters[i-1]
						data_name = elem_values.get("dataname")
						temp_type = elem_values.get("type")
						data_unit = elem_values.get("unit")

						if(temp_type == "constant"):
							data_unit = "categories"
							data_statistic = "average"

					#add info inputlayers
					layer_in_name = data_name
					layer_in = etree.Element("layer", name = layer_in_name)

					in_parameter_cat = etree.Element("parameter_cat")
					in_layer_filename = etree.Element("layer_filename")
					in_unit = etree.Element("unit")
					in_statistic = etree.Element("statistic")
					in_description = etree.Element("description")

					in_parameter_cat.text = "TOBEFILLED"
					in_layer_filename.text = layer_in_name
					in_unit.text = data_unit
					in_statistic.text = data_statistic
					in_description.text = "TOBEFILLED"

					layer_in.append(in_parameter_cat)
					layer_in.append(in_layer_filename)
					layer_in.append(in_unit)
					layer_in.append(in_statistic)
					layer_in.append(in_description)

					inputLayers.append(layer_in)



					#rewrite transformation layers
					if(elem_values.tag == xmltest.make_find(["valuesScalar"]) and element.tag == xmltest.make_find(["ResponseCurve"])):
						new_elem_values =  etree.Element("valuesScalar")
						for temp in elem_values.getchildren():
							input_val = temp.get("value")
							output_val = temp.get("HSI")
							etree.SubElement(new_elem_values, "parameter", input = input_val, output = output_val)

					if(elem_values.tag == xmltest.make_find(["valuesCategorical"]) and element.tag == xmltest.make_find(["ResponseCurve"])):
						new_elem_values =  etree.Element("valuesCategorical")
						for nr, temp in enumerate(elem_values.getchildren()):
							input_val = nr + 1
							input_cat_val = temp.get("cat")
							output_val = temp.get("HSI")
							output_cat_val = ""
							etree.SubElement(new_elem_values, "parameter", input = str(input_val), input_cat = str(input_cat_val),\
														output = str(output_val), output_cat = str(output_cat_val))


					if(elem_values.tag == xmltest.make_find(["valuesRanges"]) and element.tag == xmltest.make_find(["ResponseCurve"])):
						new_elem_values =  etree.Element("valuesRanges")
						for nr, temp in enumerate(elem_values.getchildren()):
							input_min_val = temp.get("rangemin")
							input_max_val = temp.get("rangemax")
							output_val = temp.get("HSI")
							etree.SubElement(new_elem_values, "parameter", rangemin_input = str(input_min_val), rangemax_input = str(input_max_val),\
														output = str(output_val))

					
					if(elem_values.tag == xmltest.make_find(["valuesRangeCategorical"]) and element.tag == xmltest.make_find(["ResponseCurve"])):
						new_elem_values =  etree.Element("valuesRangeCategorical")
						for nr, temp in enumerate(elem_values.getchildren()):
							input_min_val = temp.get("rangemin")
							input_max_val = temp.get("rangemax")
							input_cat_val = temp.get("cat")
							output_val = temp.get("HSI")
							output_cat_val = ""
							etree.SubElement(new_elem_values, "parameter", rangemin_input = str(input_min_val), rangemax_input = str(input_max_val),\
														input_cat = str(input_cat_val), output = str(output_val), output_cat = str(output_cat_val))

					if(elem_values.tag == xmltest.make_find(["valuesScalar"]) and element.tag == xmltest.make_find(["FormulaBased"])):
						new_elem_values =  etree.Element("valuesScalar", layername = layer_in_name, type = "scalar")
						temp = elem_values.getchildren()[0]
						input_min_val = temp.get("min")
						input_max_val = temp.get("max")
						etree.SubElement(new_elem_values, "parameter", min_input = str(input_min_val), max_input = str(input_max_val))


					if(elem_values.tag == xmltest.make_find(["valuesConstant"]) and element.tag == xmltest.make_find(["FormulaBased"])):
						new_elem_values =  etree.Element("valuesConstant", layername = layer_in_name, type = "constant")
						for nr, temp in enumerate(elem_values.getchildren()):
							input_val = nr + 1
							input_cat_val = temp.get("constantset")
							output_val = temp.get("value")
							etree.SubElement(new_elem_values, "parameter", input = str(input_val), input_cat = str(input_cat_val), output = str(output_val))
							

					if(element.tag == xmltest.make_find(["FormulaBased"])):
						new_elem_Parameters.append(new_elem_values)



				#add info Content
				content_type = etree.Element("type")
				content_description = etree.Element("description")
				
				if(element.tag == xmltest.make_find(["ResponseCurve"])):
					content_type.text = data_type
				content_description.text = data_description

				if(element.tag == xmltest.make_find(["ResponseCurve"])):
					Content.append(content_type)
				Content.append(content_description)
				Content.append(elem_author)
				Content.append(elem_date)
				Content.append(elem_references)
				if(element.tag == xmltest.make_find(["ResponseCurve"])):
					Content.append(new_elem_values)
				if(element.tag == xmltest.make_find(["FormulaBased"])):
					Content.append(elem_equation)
					Content.append(new_elem_Parameters)

				#add info outputlayers
				#only one output layer for now
				layer_out_name = "HSI_" + data_name
				layer_out = etree.Element("layer", name = layer_out_name)
				
				out_parameter_cat = etree.Element("parameter_cat")
				out_layer_filename = etree.Element("layer_filename")
				out_unit = etree.Element("unit")
				out_statistic = etree.Element("statistic")
				out_description = etree.Element("description")

				out_parameter_cat.text = "HSI"
				out_layer_filename.text = layer_out_name
				out_unit.text = "factor"
				out_statistic.text = "average"
				out_description.text = "TOBEFILLED"

				layer_out.append(out_parameter_cat)
				layer_out.append(out_layer_filename)
				layer_out.append(out_unit)
				layer_out.append(out_statistic)
				layer_out.append(out_description)

				outputLayers.append(layer_out)

				for child in list(element):
					element.remove(child)

				element.insert(0,inputLayers)
				element.insert(1,Content)
				element.insert(2,outputLayers)


			#write xml
			if(os.path.isfile(os.path.join(path_newkr_dir, level1_dir,level2_dir,xml_file))):
				#overwrite file
				xmltest._writexml(os.path.join(path_newkr_dir, level1_dir,level2_dir,xml_file))
			else:
				#wrie new file
				xmltest._writexml(os.path.join(path_newkr_dir, level1_dir,level2_dir,xml_file))

			log.append(["Done : " + path_xml_file])


log.append([" Total number of XMLs : " + str(nr_xmls)])
log.append([""])
log.append(["END LOG"])


#write the log
log_txt =  open("log.txt","w")
log_txt.writelines("%s\n" % line[0] for line in log)
log_txt.close()

print("Done.")
#do for each knowledge rule:
#If response curve

	
#if FormulaBased








#rename ContentDescription to TopicDescription
#first tag
#end tag
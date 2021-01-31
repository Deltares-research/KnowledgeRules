'''
Update all XMLS according to the new format

Changes are:

Structural changes:
	inputLayers, outputLayers

layer :
	parameter_name (added) -> entry = layer name
	period (added) -> default : Undefined
	position (added) -> default : Undefined

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
path_xsd = "../../xmlschema/AutecologyXML.xsd"

list_skip = []


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

			#update response curve elements
			#LOOP OVER ALL RESPONSE CURVES THEN SPECIFY FOR TYPE OF KNOWLEDGE RULE (CONTENT DIFFERENT)
			# NUMER OF INPUT LAYERS DIFFERENT
			system_knowledge_rule_elements = xmltest.xmlroot.findall(xmltest.make_find(["Autecology","ModelType","System","KnowledgeRules"]))
			if(len(system_knowledge_rule_elements) > 1):
				log.append(["XML has multiple systems : " + path_xml_file])
			
			#loop through systems
			for knowledge_rule_element in system_knowledge_rule_elements: 
			
				knowledge_rules_elements = knowledge_rule_element.findall(xmltest.make_find(['ResponseCurve'])) + knowledge_rule_element.findall(xmltest.make_find(['FormulaBased'])) + \
					knowledge_rule_element.findall(xmltest.make_find(['MultipleReclassification']))

				#Loop through the knowledge rules
				for element in knowledge_rules_elements:
				
					layers = element.findall(xmltest.make_find(['inputLayers','layer'])) + element.findall(xmltest.make_find(['outputLayers','layer']))
					#Loop through the layers
					for layer in layers: 
						
						#get data
						layer_name = layer.get("name")
						layer_parameter_cat = layer.find(xmltest.make_find(['parameter_cat']))
						layer_filename = layer.find(xmltest.make_find(['layer_filename']))
						layer_unit = layer.find(xmltest.make_find(['unit']))
						layer_statistic = layer.find(xmltest.make_find(['statistic']))
						layer_description = layer.find(xmltest.make_find(['description']))

						
						#create (new) layer characteristics
						new_layer_parameter_name = etree.Element("parameter_name")
						new_layer_parameter_cat = etree.Element("parameter_cat")
						new_layer_period = etree.Element("period")
						new_layer_position = etree.Element("position")
						new_layer_unit = etree.Element("unit")
						new_layer_statistic = etree.Element("statistic")
						new_layer_filename = etree.Element("layer_filename")
						new_layer_description = etree.Element("description")

						#change layer characteristics wording from where TOBEFILLED to Undefined:
						if(layer_parameter_cat.text == "TOBEFILLED"):
							layer_parameter_cat.text = "Undefined"
						if(layer_unit.text == "TOBEFILLED"):
							layer_unit.text = "Undefined"
						if(layer_unit.text == "TOBEFILLED"):
							layer_unit.text = "Undefined"
						if(layer_statistic.text == "TOBEFILLED"):
							layer_statistic.text = "Undefined"
						if(layer_filename.text == "TOBEFILLED"):
							layer_filename.text = "Undefined"
						if(layer_description.text == "TOBEFILLED"):
							layer_description.text = "Undefined"

						#Fill new layer structure
						new_layer_parameter_name.text = layer_name
						new_layer_parameter_cat.text = layer_parameter_cat.text
						new_layer_period.text = "Undefined"
						new_layer_position.text = "Undefined"
						new_layer_unit.text = layer_unit.text
						new_layer_statistic.text = layer_statistic.text
						new_layer_filename.text = layer_filename.text
						new_layer_description.text = layer_description.text

						
						#empty the original layer
						for child in list(layer):
							layer.remove(child)

						#fill original layer with new structure
						layer.insert(0,new_layer_parameter_name)
						layer.insert(1,new_layer_parameter_cat)
						layer.insert(2,new_layer_period)
						layer.insert(3,new_layer_position)
						layer.insert(4,new_layer_unit)
						layer.insert(5,new_layer_statistic)
						layer.insert(6,new_layer_filename)
						layer.insert(7,new_layer_description)


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
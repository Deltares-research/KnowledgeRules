'''
Validate KnowledgeRules XMLs based on schema
and write a log on findings
'''

import os
from lxml import etree
import sys


sys.path.append("../scripting_library")
from autecology_xml import AutecologyXML


#INITIALISE

#path to "_knowledgerules"dir
path_kr_dir = "../../_knowledgerules/"

#path to XSD schema
path_xsd = "../../xmlschema/AutecologyXML.xsd"


layer_csv_full_trace = [["Overall_Topic_1", "Overall_Topic_2", "Topic_name", "ModelType",\
 "System", "KnowledgeRule", "Layername", "parameter_cat", "layer_filename", "unit", "statistic", "description"]]
layer_csv_parameters = [["Layername", "parameter_cat", "layer_filename", "unit", "statistic", "description","Count"]]
layer_csv            = [["Layername", "parameter_cat", "layer_filename", "unit", "statistic", "description"]]

#start log

#start log
log = []
validation_log = []
nr_xmls = 0
log.append(["---Quarry log for KnowledgeRules xmls---"])
log.append([""])

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

	#write part
	x1 = [level1_dir]

	for level2_dir in level2_dirs:
		log.append(["      /"+ level2_dir])
		#get all xml files in a level2 dir and loop over them		
		path_l2_dir = os.path.join(path_l1_dir,level2_dir) 
		xmls_l2_dir = [file for file in os.listdir(path_l2_dir) if(file.endswith(".xml"))]
		
		#write part
		x2 = [level2_dir]

		for xml_file in xmls_l2_dir:
			#add data to the log and count xmls
			path_xml_file = os.path.join(path_l2_dir,xml_file)
			log.append(["        /"+ xml_file])
			nr_xmls = nr_xmls + 1


			#write part
			x3 = [xml_file]

			#load the xml file
			try:
				xmltest = AutecologyXML(filename = path_xml_file)
				xmltest._readxml()
				xmltest._scan()
			except:
				validation_log.append(["XML could not be read with AutecologyXML : " + path_xml_file]) 
				continue

			for cur_modeltype in xmltest.modeltypes:
				#check scan of XML modeltypes
				try:
					xmltest._scan_modeltype(cur_modeltype)
				except:
					validation_log.append(["XML ModelType could not be scanned with AutecologyXML. File : " + path_xml_file +\
										   " with ModelType " + str(cur_modeltype)]) 
					continue

				#write part
				x4 = [cur_modeltype]
				
				for cur_system in xmltest.systems:
					try:
						xmltest._scan_knowledgerules(cur_modeltype, cur_system)
					except:
						validation_log.append(["XML Knowledgerules could not be scanned with AutecologyXML. File : " + path_xml_file +\
										   " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)]) 
						continue

					#write part
					x5 = [cur_system]

					#loop through all knowledge rules
					for key, value in xmltest.knowledgeRulesDict["rules"].items():

						#add KnowlegdeRule
						x6 = [key]

						for inlayer_name, inlayer in value["inputLayers"].items():

							#"Layername", "parameter_cat", "layer_filename", "unit", "statistic", "description"
							layername = inlayer_name
							parameter_cat = inlayer["parameter_cat"]
							layer_filename = inlayer["layer_filename"]
							unit = inlayer["unit"]
							statistic = inlayer["statistic"]
							description = inlayer["description"]


							#write part
							x7 = [layername, parameter_cat, layer_filename, unit, statistic, description]


							#add all together
							layer_csv_full_trace.append(x1+x2+x3+x4+x5+x6+x7)

							#add just parameter credentials and count the amount of occurance
							if(x7 not in layer_csv):
								layer_csv.append(x7)
								layer_csv_parameters.append(x7 + [str(1)])
							else:
								line_nr = layer_csv.index(x7)
								layer_csv_parameters[line_nr][6] = str(int(layer_csv_parameters[line_nr][6]) + 1)



						for outlayer_name, outlayer in value["outputLayers"].items():

							#"Layername", "parameter_cat", "layer_filename", "unit", "statistic", "description"
							layername = outlayer_name
							parameter_cat = outlayer["parameter_cat"]
							layer_filename = outlayer["layer_filename"]
							unit = outlayer["unit"]
							statistic = outlayer["statistic"]
							description = outlayer["description"]


							#write part
							x7 = [layername, parameter_cat, layer_filename, unit, statistic, description]


							#add all together
							layer_csv_full_trace.append(x1+x2+x3+x4+x5+x6+x7)

							#add just parameter credentials and count the amount of occurance
							if(x7 not in layer_csv):
								layer_csv.append(x7)
								layer_csv_parameters.append(x7 + [str(1)])
							else:
								line_nr = layer_csv.index(x7)
								layer_csv_parameters[line_nr][6] = str(int(layer_csv_parameters[line_nr][6]) + 1)


log.append([" Total number of XMLs : " + str(nr_xmls)])
log.append([""])
log.append(["- Validation"])

#finish the validation log
if(len(validation_log) == 0):
	log.append([" All xmls validated succesfully!"])
else:
	log = log + validation_log

log.append([""])
log.append(["END LOG"])

#write querry layers overview
querry_layers_overview_csv =  open("querry_full_layers_overview.csv","w")
querry_layers_overview_csv.writelines("%s\n" % ";".join(line) for line in layer_csv_full_trace)
querry_layers_overview_csv.close()

#write querry parameters overview
querry_parameters_overview_csv =  open("querry_full_parameters_overview.csv","w")
querry_parameters_overview_csv.writelines("%s\n" % ";".join(line) for line in layer_csv_parameters)
querry_parameters_overview_csv.close()


#write the log
log_txt =  open("log.txt","w")
log_txt.writelines("%s\n" % line[0] for line in log)
log_txt.close()

print("Done.")

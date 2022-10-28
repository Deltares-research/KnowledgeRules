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
path_xsd = "../../XMLSchema/AutecologyXML.xsd"


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
validation_log = []
nr_xmls = 0
log.append(["---Validation log for KnowledgeRules xmls---"])
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


	for level2_dir in level2_dirs:
		log.append(["      /"+ level2_dir])
		#get all xml files in a level2 dir and loop over them		
		path_l2_dir = os.path.join(path_l1_dir,level2_dir) 
		xmls_l2_dir = [file for file in os.listdir(path_l2_dir) if(file.endswith(".xml"))]
		for xml_file in xmls_l2_dir:
			#add data to the log and count xmls
			path_xml_file = os.path.join(path_l2_dir,xml_file)
			log.append(["        /"+ xml_file])
			nr_xmls = nr_xmls + 1
			
			#validate the xml file and log if incorrect
			try:
				val_res = validate(path_xml_file, path_xsd)
				#check validation
				if(val_res):
					pass
				else:	
					validation_log.append(["Not valid : " + path_xml_file])
			except:
				validation_log.append(["Not valid : " + path_xml_file])
				continue

			#load the xml file
			try:
				xmltest = AutecologyXML(filename = path_xml_file)
				xmltest._readxml()
				xmltest._scan()
			except:
				validation_log.append(["XML could not be read with AutecologyXML : " + path_xml_file]) 
				continue

			#CHECK languages Names and descriptions
			cur_species_commonnames = xmltest.commonnames
			cur_species_commonname_LANG = sorted([line["language"] for line in cur_species_commonnames])
			cur_species_descriptions = xmltest._read_topicdescription()
			cur_species_description_LANG = sorted([line["language"] for line in cur_species_descriptions])

			if(cur_species_commonname_LANG != cur_species_description_LANG):
				miss_common_name = (set(cur_species_description_LANG).difference(cur_species_commonname_LANG))
				miss_species_description =  (set(cur_species_commonname_LANG).difference(cur_species_description_LANG))
				if(len(miss_common_name) != 0):
					validation_log.append(["Missing language in SpeciesDescription :" +  str(miss_common_name) +". File : " + path_xml_file])
				elif(len(miss_species_description) != 0):
					validation_log.append(["Missing language in CommonNames :", str(miss_species_description) +". File : " + path_xml_file])
				else:
					validation_log.append(["Someting wrong between languages SpeciesDescription and CommonNames, please investigate : " + path_xml_file])
			
			for cur_modeltype in xmltest.modeltypes:
				#check scan of XML modeltypes
				try:
					xmltest._scan_modeltype(cur_modeltype)
				except Exception as e:
					validation_log.append(["XML ModelType could not be scanned with AutecologyXML. File : " + path_xml_file +\
										   " with ModelType " + str(cur_modeltype)]) 
					validation_log.append([e])
					validation_log.append([""])
					continue

				for cur_system in xmltest.systems:
					try:
						xmltest._scan_knowledgerules(cur_modeltype, cur_system)
					except Exception as e:
						validation_log.append(["XML Knowledgerules could not be scanned with AutecologyXML. File : " + path_xml_file +\
										   " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)]) 
						validation_log.append([e])
						validation_log.append([""])
						continue

					#check if languages are correct
					cur_system_description = xmltest._read_systemdescription(cur_modeltype, cur_system)
					cur_system_description_LANG = sorted([line["language"] for line in cur_system_description])

					if(cur_species_commonname_LANG != cur_system_description_LANG):
						miss_common_name = (set(cur_system_description_LANG).difference(cur_species_commonname_LANG))
						miss_system_description =  (set(cur_species_commonname_LANG).difference(cur_system_description_LANG))
						if(len(miss_common_name) != 0):
							validation_log.append(["Missing language in SystemDescription :" +  str(miss_common_name) +". File : " + path_xml_file +\
												  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])
						elif(len(miss_system_description) != 0):
							validation_log.append(["Missing language in CommonNames and/or SpeciesDescription : " +  str(miss_system_description) +". File : " + path_xml_file +\
												  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])
						else:
							validation_log.append(["Someting wrong between languages SpeciesDescription, CommonNames and SystemDescription, please investigate. File : " + path_xml_file +\
												  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])
					
					#check if no reoccuring names for knowledge rules
					if(len(xmltest.knowledgeRulesNames) != len(set(xmltest.knowledgeRulesNames))):
						seen = set()
						not_uniq = []
						for name in xmltest.knowledgeRulesNames:
								if(not name in seen):
									seen.add(name)
								else:
									not_uniq.append(name)	
						
						validation_log.append(["Duplicated Knowledge rule names in ResponseCurve, FormulaBased or other :" +  str(not_uniq) +". File : " + path_xml_file +\
											  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])
						
					#check if the flow diagram is correct
					xmltest._scan_systemflowdiagrams(cur_modeltype,cur_system)
					if(len(xmltest.flowdiagrams) > 0 ):
						for cur_flowdiagram in xmltest.flowdiagrams:
							flowdiagram_dict = xmltest._read_systemflowdiagram(cur_modeltype, cur_system, cur_flowdiagram)
							flowdiagram_links = flowdiagram_dict["Links"]

							#check if To in flowdiagram or knowledge rule names
							for nr_fl, flow_link in enumerate(flowdiagram_links):
								#possible to links
								pos_from_links = [x["From_name"] for x in flowdiagram_links[nr_fl:]]
								pos_to_names = pos_from_links + xmltest.knowledgeRulesNames

								#check if valid (all to links are possible)
								if(not(set(flow_link["To_names"]).issubset(set(pos_to_names)))):
									not_present = set(flow_link["To_names"]) - set(pos_to_names)
									validation_log.append(["Following flowdiagram element is not valid, check the To links : From = " +  flow_link["From_name"] +\
											  "; To's invalid = " + str(not_present) + ". File : " + path_xml_file +\
											  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])

					else:
						validation_log.append(["No flowdiagrams present :" +  not_uniq +". File : " + path_xml_file +\
											  " with ModelType " + str(cur_modeltype) + " and System " + str(cur_system)])


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

#write the log
log_txt =  open("log.txt","w")
log_txt.writelines("%s\n" % line[0] for line in log)
log_txt.close()

print("Done.")


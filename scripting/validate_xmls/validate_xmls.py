'''
Validate KnowledgeRules XMLs based on schema
and write a log on findings
'''

import os
from lxml import etree

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


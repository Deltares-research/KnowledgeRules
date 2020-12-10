'''
Update all XMLS according to the new format

Changes are:

<AutecologyXML xmlns="http://www.wldelft.nl/fews" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.wldelft.nl/fews ../../../XMLSchema/AutecologyXML.xsd">
To
<AutecologyXML xmlns="https://github.com/Deltares/KnowledgeRules" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://github.com/Deltares/KnowledgeRules ../../../xmlschema/AutecologyXML.xsd">

'''


import os
from lxml import etree
import lxml.builder
import sys
import shutil
import copy

sys.path.append("../scripting_library")
from autecology_xml import AutecologyXML


#INITIALISE
old_dbchangelog = 'xmlns="http://www.wldelft.nl/fews"'
new_dbchangelog = 'xmlns="https://github.com/Deltares/KnowledgeRules"'
old_xsi = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
new_xsi = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
old_Schemalocation = 'xsi:schemaLocation="http://www.wldelft.nl/fews ../../../XMLSchema/AutecologyXML.xsd"'
new_Schemalocation = 'xsi:schemaLocation="https://github.com/Deltares/KnowledgeRules ../../../xmlschema/AutecologyXML.xsd"'

#path to "_knowledgerules"dir
path_kr_dir = "../../_knowledgerules/"

#path to update "_knowledgerules" dir
path_newkr_dir = "../../_new_knowledgerules/"

#path to XSD schema
path_xsd = "../../XMLSchema/AutecologyXML.xsd"

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


			#Make a new element with the right buildup
			xmltextfile = open(path_xml_file,'r', encoding="utf8")
			xmltext = xmltextfile.read()
			xmltextfile.close()

			xmltext = xmltext.replace(old_dbchangelog,new_dbchangelog)
			xmltext = xmltext.replace(old_xsi,new_xsi)
			xmltext = xmltext.replace(old_Schemalocation,new_Schemalocation)
			
			new_file_path = os.path.join(path_newkr_dir, level1_dir,level2_dir,xml_file)

			newxmltextfile = open(new_file_path,'w', encoding="utf8")
			newxmltextfile.write(xmltext)
			newxmltextfile.close()

			#load the xml file
			try:
				xmltest = AutecologyXML(filename = new_file_path)
				xmltest._readxml()
			except:
				log.append(["XML could not be read at beginning with AutecologyXML : " + path_xml_file]) 
				continue


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
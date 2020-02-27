import sys
sys.path.append("..")

from autecology_xml import AutecologyXML

xmltest = AutecologyXML(filename = "../../../_knowledgerules/Habitats/Vegetation_associations/Vegetationtypes_Northen_Delta.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_topicdescription()
print(type(testext))
xmltest._scan_modeltype("HSI")
xmltest._scan_knowledgerules(modeltypename = "HSI", systemname = "biesbosch_area")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
									in xmltest.knowledgeRulesNames))
print(xmltest.systemname)
print(xmltest.knowledgeRulesNr)
print(xmltest.knowledgeRulesCategorie)
print(xmltest.knowledgeRulesNames)
print(xmltest.XMLconvention["allowed_knowledgeRulesNames"])

#TO DO: CREATE TABLE OUT OF MultipleReclassification



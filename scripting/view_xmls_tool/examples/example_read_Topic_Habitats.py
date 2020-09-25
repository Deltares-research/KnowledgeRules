import sys
sys.path.append("..")
sys.path.append('..\\source')

from autecology_xml import AutecologyXML
from matplotlib import pyplot as plt

xmltest = AutecologyXML(filename = "../../../_knowledgerules/Habitats/Vegetation_associations/Vegetationtypes_Northern_Delta.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
print(xmltest.topic_name)
print(xmltest.commonnames)

xmltest._scan_modeltype("HSI")
print(xmltest.modeltypename)
print(xmltest.systems)

xmltest._scan_knowledgerules(modeltypename = xmltest.modeltypename, systemname = xmltest.systems[0])
print(xmltest.XMLconvention["allowed_knowledgeRulesCategories"])
print(xmltest.knowledgeRulesNames)
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesCategories"] for elem \
									in xmltest.knowledgeRulesCategories))


print("Done.")
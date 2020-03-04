import sys
sys.path.append("..")
sys.path.append('..\\source')

from autecology_xml import AutecologyXML
from matplotlib import pyplot as plt

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
xmltest = AutecologyXML(filename = "../../../tool_adapters/Deltares_Habitat/examples/Plecoglossus_altivelis.xml")

xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_topicdescription()
print(type(testext))
xmltest._scan_modeltype("HSI")
#xmltest._scan_knowledgerules(systemname = "adult")
xmltest._scan_knowledgerules(modeltypename = "HSI", systemname = "adult")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
									in xmltest.knowledgeRulesNames))
print(xmltest.knowledgeRulesCategorie)
print(xmltest.XMLconvention["allowed_knowledgeRulesNames"])
flowdiagram = xmltest._read_systemflowdiagrams(modeltypename = "HSI", systemname = "adult")
print(flowdiagram)
print(flowdiagram[0]["name"])
print(flowdiagram[0]["Links"])



import sys
from matplotlib import pyplot as plt


sys.path.append("../")
from autecology_xml import AutecologyXML


xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax_carbo.xml")
#xmltest = AutecologyXML(filename = "../../../tool_adapters/Deltares_Habitat/examples/Plecoglossus_altivelis.xml")

xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_topicdescription()
print(type(testext))
xmltest._scan_modeltype("HSI")
#xmltest._scan_knowledgerules(systemname = "adult")
xmltest._scan_knowledgerules(modeltypename = "HSI", systemname = "adult")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesCategories"] for elem \
									in xmltest.knowledgeRulesCategories))
print(xmltest.knowledgeRulesNames)
print(xmltest.knowledgeRulesCategories)
print(xmltest.XMLconvention["allowed_knowledgeRulesCategories"])
xmltest._scan_systemflowdiagrams(modeltypename = "HSI", systemname = "adult")
print(xmltest.flowdiagrams)

print(xmltest.flowdiagrams_list[0]['diagram_name'])
print(xmltest.flowdiagrams_list[0]['Links'])
print(xmltest.flowdiagrams_list[0]['Links'][0]['From_name'])
print(xmltest.flowdiagrams_list[0]['Links'][0]['To_names'])



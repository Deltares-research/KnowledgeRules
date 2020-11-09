import sys
from matplotlib import pyplot as plt

sys.path.append("../")
from autecology_xml import AutecologyXML



#xmltest = AutecologyXML(filename = "../../../_knowledgerules/WFD_indicators/ecological_status/Macrofauna_in_beken_en_kleine_rivieren.xml")
#xmltest = AutecologyXML(filename = "../../../_knowledgerules/WFD_indicators/ecological_indicators/Aquatic_plants_total_coverage.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/WFD_indicators/ecological_indicators/Filamentous_algae.xml")
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
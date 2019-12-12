import sys
sys.path.append("..")

from autecology_xml import AutecologyXML
from matplotlib import pyplot as plt

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Molluscs/Dreissena_polymorpha.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_speciesdescription()
print(type(testext))
#xmltest._scan_knowledgerules(systemname = "adult")
xmltest._scan_knowledgerules(systemname = "adult")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
									in xmltest.knowledgeRulesNames))
print(xmltest.knowledgeRulesCategorie)
print(xmltest.XMLconvention["allowed_knowledgeRulesNames"])
#rc_tag = xmltest.get_element_response_curve(systemname = "adult", rcname = "Afstand tot moeras")
rc_tag = xmltest.get_element_response_curve(systemname = "adult", rcname = "Soil")
print(rc_tag)
rc_data = xmltest.get_data_response_curve_data(rc_tag)
print(rc_data)
print(type(rc_data))
print(type(rc_data["rule"]))

fig, axes = xmltest.visualize_rc(rc_data)

plt.draw()
plt.show()
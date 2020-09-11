import sys
sys.path.append("..")
sys.path.append('..\\source')

from autecology_xml import AutecologyXML
from matplotlib import pyplot as plt

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Molluscs/Dreissena_polymorpha.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Gallinago_gallinago.xml")

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
#rc_tag = xmltest.get_element_response_curve(modeltypename = "HSI", systemname = "adult", rcname = "afstand_tot_moeras")
#rc_tag = xmltest.get_element_response_curve(modeltypename = "HSI", systemname = "adult", rcname = "substrate_type")
rc_tag = xmltest.get_element_response_curve(modeltypename = "HSI", systemname = "adult", rcname = "water_storage_capacity")
print(rc_tag)
rc_data = xmltest.get_data_response_curve_data(rc_tag)
print(rc_data)
print(type(rc_data))
print(type(rc_data["rule"]))

fig, axes = xmltest.visualize_rc(rc_data)

plt.draw()
plt.show()
import sys
sys.path.append("..")
sys.path.append('..\\source')

from autecology_xml import AutecologyXML

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Molluscs/Dreissena_polymorpha.xml")
#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Macrophytes/Nitellopsis obtusa.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Macrophytes/Myriophyllum_spicatum.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))

xmltest._scan()
print(xmltest.topic_name)
print(xmltest.EoL_ID)
print(xmltest.EoL_Link)
print(xmltest.latinname)
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
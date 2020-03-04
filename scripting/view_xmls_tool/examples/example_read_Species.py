import sys
sys.path.append("..")
sys.path.append('..\\source')

from autecology_xml import AutecologyXML

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Molluscs/Dreissena_polymorpha.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
print(xmltest.topic_name)
print(xmltest.EoL_ID)
print(xmltest.EoL_Link)
print(xmltest.latinname)
print(xmltest.commonnames)

print("Done.")
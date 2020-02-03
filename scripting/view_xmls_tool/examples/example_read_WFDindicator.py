import sys
sys.path.append("..")

from autecology_xml import AutecologyXML
from matplotlib import pyplot as plt

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/WFD_indicators/ecological_status/Macrofauna_in_beken_en_kleine_rivieren.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
print(xmltest.topic_name)
print(xmltest.commonnames)
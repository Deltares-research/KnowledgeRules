import sys
import pandas


sys.path.append("../")
from autecology_xml import AutecologyXML


xmltest = AutecologyXML(filename = "../../../_knowledgerules/Habitats/Vegetation_associations/Vegetationtypes_Northern_Delta.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_topicdescription()
print(type(testext))
xmltest._scan_modeltype("HSI")
xmltest._scan_knowledgerules(modeltypename = "HSI", systemname = "biesbosch_area")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesCategories"] for elem \
									in xmltest.knowledgeRulesCategories))
print(xmltest.systemname)
print(xmltest.knowledgeRulesNr)
print(xmltest.knowledgeRulesCategories)
print(xmltest.knowledgeRulesNames)
print(xmltest.XMLconvention["allowed_knowledgeRulesCategories"])

#TO DO: CREATE TABLE OUT OF MultipleReclassification
mr_element = xmltest.get_element_multiple_reclassification(modeltypename = "HSI", systemname = "biesbosch_area", mrname = "vegetation_classification")
mr_data = xmltest.get_data_multiple_reclassification_data(mr_element)
(mr_dataframe,mr_dataframe_headers) = xmltest.make_mr_dataframe(mr_data)

frame = xmltest.visualize_mr_table(mr_dataframe, mr_dataframe_headers)
xmltest.show_PyQt_plot(frame)

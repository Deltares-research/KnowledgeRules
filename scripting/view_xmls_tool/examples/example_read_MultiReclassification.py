import sys
sys.path.append("..")
sys.path.append('..\\source')

import pandas

from autecology_xml import AutecologyXML

xmltest = AutecologyXML(filename = "../../../_knowledgerules/Habitats/Vegetation_associations/Vegetationtypes_Northen_Delta.xml")
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
print(xmltest.knowledgeRulesCategorie)
print(xmltest.knowledgeRulesNames)
print(xmltest.XMLconvention["allowed_knowledgeRulesNames"])

#TO DO: CREATE TABLE OUT OF MultipleReclassification
mr_element = xmltest.get_element_multiple_reclassification(modeltypename = "HSI", systemname = "biesbosch_area", mrname = "vegetationtypes_without_grazing")
mr_data = xmltest.get_data_multiple_reclassification_data(mr_element)

#print(mr_data)
print("")
#print(mr_data["parameters"])

def make_table(mr_data):
	for nr, cur_par in enumerate(mr_data["parameters"]):
		df_current_rule = cur_par["data"]
		
		#Currently enabled for type "range / categorical"
		if(cur_par["type"] == "range / categorical"):
			#If boolean change table input
			if(cur_par["unit"] == "boolean"):
				df_current_rule["input"] = df_current_rule["rangemax_input"]
			else:
				df_current_rule["input"] = df_current_rule["rangemin_input"].astype(str) + " - "+ df_current_rule["rangemax_input"].astype(str)
		
		else:
			raise ValueError("Table visualisation not enabled yet for other than input type 'range / categorical'")

		df_current_rule_subset = df_current_rule[["output_cat","output","input"]].copy()
		df_current_rule_subset.columns = ["output_cat","output",cur_par["layername"]]
		
		if(nr == 0):
			df_total_rule = df_current_rule_subset
		
			#store headers for later
			df_total_rule_headers = {"header" : [mr_data["name"],"",cur_par["layername"]], "unit" : ["str","output id",cur_par["unit"]]}
		else:
			df_total_rule = df_total_rule.merge(df_current_rule_subset, on = ["output_cat","output"], how = "outer")
			df_total_rule_headers["header"].append(cur_par["layername"])
			df_total_rule_headers["unit"].append(cur_par["unit"])

	#sort the data
	df_total_rule = df_total_rule.sort_values(by=["output"])
	
	return(df_total_rule, df_total_rule_headers)

(mr_dataframe, mr_dataframe_dict) = make_table(mr_data)

print(mr_dataframe_dict["header"])
print(mr_dataframe_dict["unit"])
print(mr_dataframe.iloc[0:5,:])

frame = xmltest.visualize_mr_table(mr_dataframe, mr_dataframe_dict)
xmltest.show_PyQt_plot(frame)

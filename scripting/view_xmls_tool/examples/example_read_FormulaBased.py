import sys
sys.path.append("..")

from autecology_xml import AutecologyXML

xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Macrophytes/Chara spp.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
testext = xmltest._read_topicdescription()
print(type(testext))
xmltest._scan_modeltype("HSI")
xmltest._scan_knowledgerules(modeltypename = "HSI", systemname = "ijsselmeergebied_doorzicht")
print(all(elem in xmltest.XMLconvention["allowed_knowledgeRulesNames"] for elem \
									in xmltest.knowledgeRulesNames))
print(xmltest.knowledgeRulesCategorie)
print(xmltest.XMLconvention["allowed_knowledgeRulesNames"])
fb_tag = xmltest.get_element_formula_based(modeltypename = "HSI", systemname = "ijsselmeergebied_doorzicht", fbname = "P_chara_visibility")
fb_data = xmltest.get_data_formula_based_data(fb_tag)

print(fb_data)
print(fb_data['parameters'])
print(fb_data['parameters'][0]['data'])
print(type(fb_data))

fb_settings = {'deelgebied' : 1.154566, 'diepte_zom' : 0.35, 'doorzicht' : 3.0, 'strijklengte' : 0}
fb_list = {'diepte_zom' : [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]}
fb_list = {'doorzicht' : [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]}

fb_settings, fb_list = xmltest.make_fb_first_parametersettings(fb_data)
fb_result = xmltest.calculate_fb(fb_data, fb_settings, variableparameter = fb_list)

fb_result

fig, axes = xmltest.visualize_fb_static(fb_data, fb_result)
frame = xmltest.visualize_fb_dynamic(fb_data,fb_result)
xmltest.show_PyQt_plot(frame)



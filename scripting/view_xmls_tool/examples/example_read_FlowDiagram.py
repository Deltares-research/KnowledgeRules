import sys
sys.path.append("..")

from autecology_xml import AutecologyXML

#xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Birds/Phalacrocorax carbo.xml")
xmltest = AutecologyXML(filename = "../../../_knowledgerules/species/Molluscs/Dreissena_polymorpha.xml")
xmltest._readxml()
print(type(xmltest.xmlroot))
xmltest._scan()
xmltest._scan_modeltype(modeltypename = "HSI")
xmltest._scan_system(modeltypename = "HSI", systemname = "adult")
xmltest._scan_systemflowdiagrams(modeltypename = "HSI", systemname = "adult")
print(xmltest.flowdiagrams)
print(xmltest.flowdiagrams_list)

#Create a specific flow diagram
flowdiagram = xmltest._read_systemflowdiagram(modeltypename = "HSI", systemname = "adult", diagramname ="livingarea_stagnant_waters" )
svg_str = xmltest.create_flowdiagram_image(flowdiagram, output = None)

#show in PyQt
subwindow_flowdiagram = xmltest.visualize_flowdiagram_image(svg_str)
xmltest.show_PyQt_plot(subwindow_flowdiagram)

print("Done.")
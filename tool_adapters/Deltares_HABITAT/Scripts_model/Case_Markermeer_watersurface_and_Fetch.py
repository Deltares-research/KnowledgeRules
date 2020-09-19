# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

import os # for reading paths
#from lxml import etree as ET #NOT AVAILABLE FOR DELTASHELL
import xml.etree.ElementTree as ET # for reading and writing *.xml files
from collections import OrderedDict 

# set location of input maps and output 
WorkDir = "d:\\Projects\\Habitat\\Model_tester\\" 
print("Workdirectory : " + WorkDir)

#Model
model_name = "Markermeer"
InputDir = WorkDir + "invoerfiles\\invoerkaarten\\Markermeer"
KnowledgeRuleDir = WorkDir + "invoerfiles\\kennisregels\\"
OutputDir = WorkDir + "OutputMaps\\"


#region WATERSURFACE
#Give knowledge rule characteristics
kr_file = "parameters\\Watersurface.xml"
topic_name = "Watersurface"
system_to_model = "ijsselmeergebied"
flow_diagram ="watersurface_summer"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion

#region FETCH
#Give knowledge rule characteristics
kr_file = "parameters\\Fetch.xml"
topic_name = "Fetch"
system_to_model = "ijsselmeergebied"
flow_diagram ="fetch"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
#endregion
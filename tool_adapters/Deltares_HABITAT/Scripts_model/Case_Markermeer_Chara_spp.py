# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

# set location of input maps and output 
WorkDir = "d:\\Projects\\Habitat\\Model_tester\\" 
print("Workdirectory : " + WorkDir)

#Model
model_name = "Markermeer"
InputDir = WorkDir + "invoerfiles\\invoerkaarten\\Markermeer\\"
KnowledgeRuleDir = WorkDir + "invoerfiles\\kennisregels\\"
OutputDir = WorkDir + "OutputMaps\\"

#region VISIBILITY
#Give knowledge rule characteristics

kr_file = "parameters\\Light_extinction.xml"
topic_name = "Visibility"
system_to_model = "ijsselmeergebied"
flow_diagram ="visibility"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion

#region WATERSURFACE
#Give knowledge rule characteristics
kr_file = "parameters\\Watersurface.xml"
topic_name = "Watersurface"
system_to_model = "ijsselmeergebied"
flow_diagram ="watersurface_summer"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
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

#region Chara spp model
kr_file = "species\\Chara_spp.xml"
topic_name = "Chara spp"
system_to_model = "Markermeer"
flow_diagram ="chara_presence_visibility"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
#endregion
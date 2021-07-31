# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

# set location of input maps and output 
WorkDir = "d:\\Projects\\Habitat\\KnowledgeRules\\"                  #Where is your workdirectory?
print("Workdirectory : " + WorkDir)

#Model
model_name = "Markermeer"
InputDir = WorkDir + "tool_adapters\\Deltares_HABITAT\\example_maps\\Lake_Marken\\"
KnowledgeRuleDir = WorkDir + "_knowledgerules\\"
OutputDir = WorkDir + "OutputMaps\\"

#region VISIBILITY
#Give knowledge rule characteristics

kr_file = "parameters\\water_quality\\Light_extinction.xml"           #which cause-effect model needs to be used?
topic_name = "Visibility"                                             #what is the topic name for that model?
system_to_model = "ijsselmeergebied"                                  #which System in that model should be used?
flow_diagram ="visibility"                                            #which Flowdiagram in that model should be used?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion

#region WATERSURFACE
#Give knowledge rule characteristics
kr_file = "parameters\\hydrodynamics\\Watersurface.xml"               #which cause-effect model needs to be used?
topic_name = "Watersurface"                                           #what is the topic name for that model?
system_to_model = "ijsselmeergebied"                                  #which System in that model should be used?
flow_diagram ="watersurface_summer"                                   #which Flowdiagram in that model should be used?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
#endregion

#region FETCH
#Give knowledge rule characteristics
kr_file = "parameters\\hydrodynamics\\Fetch.xml"                      #which cause-effect model needs to be used?
topic_name = "Fetch"                                                  #what is the topic name for that model?
system_to_model = "ijsselmeergebied"                                  #which System in that model should be used?
flow_diagram ="fetch"                                                 #which Flowdiagram in that model should be used?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
#endregion

#region Chara spp model
kr_file = "species\\Macrophytes\\Chara_spp.xml"                       #which cause-effect model needs to be used?
topic_name = "Chara spp"                                              #what is the topic name for that model?
system_to_model = "Markermeer"                                        #which System in that model should be used?
flow_diagram ="chara_presence_visibility"                             #which Flowdiagram in that model should be used?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram, topic_model_list)
#endregion
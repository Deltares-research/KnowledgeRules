# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

# set location of input maps and output 
WorkDir = "d:\\Projects\\check_outs\\KnowledgeRules_development\\"      #Where is your workdirectory?
print("Workdirectory : " + WorkDir)

#region Aju cause-and-effect model
kr_file = "species\\Fish\\Plecoglossus_altivelis.xml"    #which cause-effect model needs to be used?
topic_name = "Ayu"                                       #what is the topic name for that model?
system_to_model = "Tenryuu river"                        #which System in that model should be used?
flow_diagram ="Ayu_Spawning"                             #which Flowdiagram in that model should be used?
#endregiond

#region Model Q150
model_name = "Tenryuu river_Q150"                           #What is the name of your model?										
InputDir = WorkDir + "tool_adapters\\Deltares_HABITAT\\example_maps\\Tenryuu_river\\Q150\\"   #Where are the input maps to be used?
KnowledgeRuleDir = WorkDir + "_knowledgerules\\"            #Where are the cause-effect models to be used?
OutputDir = WorkDir + "OutputMaps\\"                        #Where should output be written?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion

#region Model Q900
model_name = "Tenryuu river_Q900"                           #What is the name of your model?
InputDir = WorkDir + "tool_adapters\\Deltares_HABITAT\\example_maps\\Tenryuu_river\\Q900\\"   #Where are the input maps to be used?
KnowledgeRuleDir = WorkDir + "_knowledgerules\\"            #Where are the cause-effect models to be used?
OutputDir = WorkDir + "OutputMaps\\"                        #Where should output be written?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion
# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

# set location of input maps and output 
WorkDir = "d:\\Projects\\Habitat\\KnowledgeRules\\"           #Where is your workdirectory?
print("Workdirectory : " + WorkDir)

#Model
model_name = "Tenryuu river"
InputDir = WorkDir + "tool_adapters\\Deltares_HABITAT\\example_maps\\Tenryuu_river\\standard_maps\\"
KnowledgeRuleDir = WorkDir + "_knowledgerules\\"
OutputDir = WorkDir + "OutputMaps\\"

#region Aju model
kr_file = "species\\Fish\\Plecoglossus_altivelis.xml"         #which cause-effect model needs to be used?
topic_name = "Ayu"                                            #what is the topic name for that model?
system_to_model = "Tenryuu river"                             #which System in that model should be used?
flow_diagram ="Ayu_habitat_stepped"                           #which Flowdiagram in that model should be used?

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion
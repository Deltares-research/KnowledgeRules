# Test script for setting up an automated HABITAT model

#refrom Libraries.HabitatFunctions import *
from Libraries.StandardFunctions import *
from Libraries.HabitatFunctions import *
from Libraries.AutecologyXMLFunctions import *

# set location of input maps and output 
WorkDir = "d:\\Projects\\Habitat\\Model_tester\\" 
print("Workdirectory : " + WorkDir)

#Model
model_name = "Tenryuu river"
InputDir = WorkDir + "invoerfiles\\invoerkaarten\\Japan\\"
KnowledgeRuleDir = WorkDir + "invoerfiles\\kennisregels\\"
OutputDir = WorkDir + "OutputMaps\\"

#region Aju model
kr_file = "species\\Plecoglossus_altivelis.xml"
topic_name = "Ayu"
system_to_model = "adult"
flow_diagram ="Ayu_habitat_stepped"

#Create knowledge rule in HABITAT
topic_model_list = create_and_run_model_from_XML(KnowledgeRuleDir, InputDir,\
	model_name, topic_name, kr_file, system_to_model, flow_diagram)
#endregion


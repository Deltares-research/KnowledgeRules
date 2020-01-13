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
os.chdir("d:\\Projects\\Habitat\\Marc_Project_v3\\") 
print("Workdirectory : " + os.getcwd())

InputDir = "Test_invoerfiles\\Maps\\"
KnowledgeRuleDir = "Test_invoerfiles\\Response curves\\"
OutputDir = "OutputMaps\\"

kr_file = "Plecoglossus_altivelis.xml"
system_to_model = "adult"
flow_diagram ="Ayu_habitat"

#endregion



#region Read XML knowledge rule file
#1 . read the species specific information and response curves
root = ET.parse(os.path.join(KnowledgeRuleDir,kr_file)).getroot()
flow_diagram_overview = make_flowdiagram_dict(root,system_to_model)
autecology_overview = make_knowledgerules_dict(root, system_to_model)
response_curves_overview = autecology_overview["knowledgerules"]

#print species name
print("Content : " + autecology_overview["latinname"])
print("System : " + autecology_overview["systemname"])

#end region

#region Setup model structure (currently 2 layers allowed)
#2. Setup model structure
structure = get_flow_diagram_structure(flow_diagram_overview, flow_diagram)
equations = get_flow_diagram_equations(flow_diagram_overview, flow_diagram)
(model_list,HSI_list) = make_hyrarchical_model_structure(structure)
#endregion


#region Create HSI models
#3. fill composite models with hsi models
# there are several types of models: 
    #1. FormulaBased
    #2. BrokenLinearReclassification    
    #3. SpatialStatistics
    #4. TableReclassification
    #5. MultiTableReclassification
knowledgerules_list = make_knowledgerule_models(structure, response_curves_overview, model_list)



#end region

#region add HSI summarisation models
#4. add  hsi models per sub folder
(model_list, HSI_list) = add_HSI_collection_models(structure, model_list, HSI_list)

#endregion

#region Fill HSI models
#5. fill  hsi models
# there are several types of models: 
    #1. FormulaBased
    #2. BrokenLinearReclassification    
    #3. SpatialStatistics
    #4. TableReclassification
    #5. MultiTableReclassification
(knowledgerules_list, input_list) = fill_knowledgerule_models(InputDir, response_curves_overview, knowledgerules_list)

#endregion


#region Fill HSI models
#6. run  hsi models
knowledgerules_list = run_knowledgerule_models(knowledgerules_list)

#region Fill HSI models
#7. connect submodels (current situation is that always the minimum of all HSI will be taken)
model_list = connect_and_run_hyrarchical_structure(structure, equations, HSI_list, knowledgerules_list)

#region Export output to file
#8. Export submodel results
export_model_results(OutputDir, HSI_list)

#endregion


#ExportToFile(str(Spawning_hsi.OutputGridCoverages[0]), Spawning_hsi, os.path.join(OutputDir + "Spawning_HSI.asc"))
#ExportToFile(str(Egg_incubation_hsi.OutputGridCoverages[0]), Egg_incubation_hsi, os.path.join(OutputDir + "Egg_Incubation_HSI.asc"))


# go through all the formula based models and remove the standard
# input grids and formulas
#for model in [modelflow, modelSS, modeldepth, modelDO]:
    # Remove default grid and formulas
 #   model.InputGridCoverages.Clear()
#    model.Formulas.Clear()
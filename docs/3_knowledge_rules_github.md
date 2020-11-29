---
layout: default
title: Knowledge rules GitHub
nav_orde: 3
---

# Knowledge rules GitHub

## Purpose

The Knowledge rules GitHub is an Open access and Open source storage platform to provide autecological knowledge rules in a consistent format. These knowledge rules can then be used in field assessments, modelling and/or scripting. 
 


## GitHub structure

	
 
The basic structure consists of the following folders:
*  _knowledgerules : In this folder all the currently available knowledge rules are stored. These are stored in subfolders that will be explained further on. The knowledge rules are stored based on parameter, species, habitat type or Water framework directive basis and as an XML file.  More detail is provided on these files in section “3. Knowledge rules files and structure”.
*  XMLSchema : In this folder the XML schema (an .xsd file) is stored. This file describes the convention that needs to be followed when setting up a knowledge rules XML file. This file can be used to test whether the convention is indeed followed and to make suggestions while editing an XML file with an XML editor. More detail is provided on these files in section “3. Knowledge rules files and structure”.
*  scripting : In this folder the Python based tools are made available that can be used in combination with the knowledge rule XML files. The tools that are stored here can be found in section “4. Supporting tools”.
*  tool_adapters: In this folder adapters can be found that allow for the knowledge rules XML files to be used with computational models and other analysis techniques. The adapters that are stored here can be found in section “5. Model adapters”. 

### Folder: _knowledge_rules
Within the _knowledge_rules folder the knowledge rules files are separated by parameters , species, Habitats and WFD_indicators. These separate folders represent knowledge rule file categories. In the table below each category of knowledge rule files is specified

|Category       |Description                                                  |
|---------------|-------------------------------------------------------------|
|Parameters     |Under parameters knowledge rules for deriving abiotic environmental from other abiotic environmental factors are grouped (for example:  oxygen saturation in % from oxygen concentration in mg/L). |
|Species        |Under species  knowledge rules that can be used for predicting a  species living area suitability and species presence based on abiotic environmental factors are grouped (for example : spawning habitat based on minimum oxygen concentration in summer).|
|Habitats       |Under habitats knowledge rules that determine vegetation associations and habitats as defined in the EU habitat guideline based on abiotic environmental factors are grouped (for example : classifying the area of  H2110 – Embryonic shifting dunes).|
|WFD_indicators |Under WFD_indicators knowledge rules for indicators with legal standing for the Water Framework Directive that can be based on abiotic environmental factors are grouped (for example : determining the Ecological Quality Ratio for macrofauna based on the Water Framework Directive metric).|


Within  parameters the subfolders hydrodynamics and water_quality have been created to specific the applicable knowledge rule files further.  Within species the folders Birds, Fish, Mammals, Molluscs and Macrophytes. Within Habitats currently only the folder Vegetation_associations. Within WFD_indicators the folders ecological_indicator and ecological_status. 

   

### Folder: XMLSchema
There are no subfolders to the folder XMLSchema. There is only one file supplied in this folder, named AutecologyXML.xsd, that provides the schema for setting up XML knowledge rules files.

### Folder: scripting_and_tools
The tools and scripts made available within the folder scripting are devided in the subfolders update_knowledgerules, validate_xmls and view_xmls_tool.

|Subfolder             |Description                                                |
|----------------------|-----------------------------------------------------------|
|Scripting_library     |The autecologyXML library that can be used for scripting access to the knowledge rules XMLs is located here. |
|View_xmls_tool        |In this subfolder the script and installation script for the knowledge rules XML view tool is located.| 
|Validate_xmls         |In this subfolder a script is made available that automatically validates the current stored knowledge rules based on whether they follow the XML schema convention and whether they can be read using the autecologyXML library.|
|Update_knowledgerules |In this subfolder scripts are made available that will automatically update a knowledge rule setup in a previous format to the new format.|

Within scripting_library the subfolder examples have been created to store examples on how to use the scripting_library. Within view_xmls_tool there is a folder source containing the source files so that when the tool is compiled the build is placed in a separate folder outside this subfolder. There are no subfolder present within validate_xmls and update_knowledgerules.

### Folder: tool_adapters

Currently only one tool has been made available in the folder tool_adapters. This tool is HABITAT, a spatial environmental impact software developed by Deltares. Within this subfolder there are three folders that contain the required adapter that needs to be integrated with the tool (folder : Libraries_Habitat) and examples for how the tool adapter in combination with the tool can be used (folder: examples) .


## GitHub master and development

The KnowledgeRules GitHub is continuedly being developed. This can be through new knowledge rules being made available and by new tools and features being implemented. To have a constant working and tested version of the KnoweldgeRules GitHub the “master version”  is used.  For making new developments and to test them before submitting them to this “master version” we use the “development” branch. Additional branches can be created if specific new developments require a separate developing environment. 
Only the Deltares team has the rights to commit changes to the “master version”.

## Making a local copy

A local copy of the GitHub can be made in multiple ways and will depend on how you want to use the copy. We make the following distinction in use:
*  Exploring the KnowledgeRule Github and using currently existing knowledge rules
*  Developing new knowledge rules or tools and adding these to the KnowledgeRules Github

Exploring the KnowledgeRule Github and using currently existing knowledge rules
For exploring and using the currently existing material in the KnowledgeRule Github a downloadable copy will suffice. A copy can easily be downloaded as a zip file from the GitHub page by clicking the green “Code” button and selecting Download ZIP. Make sure that you download the “master” version. 
 
If you want to easily be able to update your clone of the “master” version we recommend you to look at the “Developing new knowledge rules or tools and adding these to the KnowledgeRules Github”description.

Developing new knowledge rules or tools and adding these to the KnowledgeRules Github
When you wish to add new knowledge rules or developed tools to the existing KnowledgeRules Github then we advise you to download Git or comparable software.
[Git](https://git-scm.com/) (no interface, access through command line)
[GitHub desktop](https://desktop.github.com/) (GUI based access)

Make sure you make a “clone” of the development branch or a newly created branch, as commits won’t be possible to the master version. A clone of the “master” version can be made to easily update your clone with the latest released and tested version.
When cloning the required branch you will need the link provided in Clone (under the green Code button).

## Committing changes to the GitHub

The method of committing changes that you have made to any of the branches will be product specific (e.g. Git, GitHub desktop). However, always provide a description of the changes you have made and why you have made these changes in the comments with your commit.
Always commit changes to the development branch. This branch will be tested by Deltares before being merged with the master branch, to ensure a working product.
We characterize two types of changes to the files available of the Knowledge Rules GitHub:

**Changes to knowledge rule XML files**: 
Before committing changes made in XMLs to the development branch make sure that these changes comply with the validate_xmls.py script.  These changes do not necessarily require communication between the Deltares and the contributor.

**Changes to the code**:
Changes in any python files need to be able to pass the tests provided in those files (if provided). Any significant changes to this file will require additional tests to be implemented. These changes, especially if significant, do require communication between the Deltares and the contributor.

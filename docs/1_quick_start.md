---
layout: default
title: Quick start
nav_order: 1
---

# Quick start

## Download the Knowledge Rules Github

To get started with the KnowledgeRule Github you will need to download it.
This is easily done by clicking the green **Code** button on the right hand corner of the Github, and selecting download as Zip.
Place the zip file in an accesible location on your computer and unzip it.

If you want to make changes and commit these changes to the KnowledgeRules GitHub page, we recommed that you read the chapter [Making a local copy](##Making-a-local-copy).

## View and edit knowledge rules as XML files

The knowledge rules available in the KnowledgeRule GitHub are located in the folder **KnowledgeRules-master/_knowledgerules**.
You can view and edit these knowledge rules as XML by opening these files with a text editor (e.g. Notepad, Notepad++) or with a XML editor (e.g. Altova XML Spy, XML Copy Editor).
Both Altova XML Spy as XML Copy Editor will automatically check the XML structure with the XSD file located in the folder **KnowledgeRules-master/XMLSchema**.

For more information on these editors read the chapter [XML editors](##XML-editors).

## View knowledge rules with visualisation tool

The visualisation tool located in the folder **KnowledgeRules-master/scripting_and_tools/view_xml_tools** can be used to visualize the knowledge rule XML files.
Read the file **README_compilation.txt** in the **source** folder to compile this tool using Python 3 with the setup.py file.

A pre-compiled version installer can be downloaded [here](https://www.dropbox.com/s/oym6pfykov0c5x7/view_edit_tool-1.0.0-amd64.msi?dl=0).

Start the tool and open any of the knowledge rule XML files to visualise them.

## Load knowledge rules in HABITAT

In this quick setup you will run a calculation for spawning suitability of the Ayu fish (<em>Plecoglossus_altivelis</em>) in the Tenryuu river, Japan.

Automated knowledge rule loading can be done with HABITAT version 3.0.1.51448 and higher.
Make sure this tool is installed. The tool is free-ware and can be requested by filling out the request form [HERE](https://oss.deltares.nl/web/habitat/download).

1. When installed move to this folder:
   **KnowledgeRules-master\tool_adapters\Deltares_HABITAT\Libraries_Habitat\**

   Copy the files in this folder (AutecologyXML.py and HabitatFunctions.py) and place these in your new installation of HABITAT in this folder:
   **Habitat [VERSION number]\plugins\DeltaShell.Plugins.Toolbox\Scripts\Libraries\**

   NB. the HABITAT installation is most likely located in your Program Files (x84) folder in the Deltares folder. 

2. Start up the HABITAT tool.
   When started, in the HABITAT tool right click **Project** (on the left hand side) and select Add > New Item > Script.
   Now try if this setup works. There is a small example script located in the folder:
   **KnowledgeRules-master\tool_adapters\Deltares_HABITAT\Scripts_model\**

   Load the script named **Case_Tenryuu_river_Plecoglossus_altivelis_Spawning_scenarios.py** by copy pasting the text in it to the script opened in the HABITAT tool.

3. Before you can run the script you will need to update the WorkDir path.
   Change : **WorkDir = "d:\\Projects\\check_outs\\KnowledgeRules_development\\"**
   Int    : **WorkDir = "[Where you placed the unzipped KnowledgeRules download]\\KnowledgeRules-master\\**

4. Now you can run the script. Press **Run script** in the top left corner of the HABITAT tool.
   The script will now generate two models of the Tenryuu river with different discharges and their impact on spawning suitability for the Ayu fish (<em>Plecoglossus_altivelis</em>).
   

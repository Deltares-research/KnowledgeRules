import csv
import clr as _clr
_clr.AddReference("log4net")

from Libraries.StandardFunctions import GetItemByName

from log4net import LogManager as _LogManager
from System import Object as _Object, Array as _Array

from DelftTools.Shell.Core.Workflow import CompositeModel as _CompositeModel
from NetTopologySuite.Extensions.Coverages import RegularGridCoverage as _RegularGridCoverage
from DeltaShell.Plugins.SharpMapGis import RegularGridCoverageLoader as _RegularGridCoverageLoader
from DeltaShell.Plugins.SharpMapGis.ImportExport import GdalFileExporter as _GdalFileExporter
from DeltaShell.Plugins.Habitat.Models import Equation as _Equation
from DeltaShell.Plugins.Habitat.Models import BrokenLinearModel as _BrokenLinearModel
from DeltaShell.Plugins.Habitat.Models import ClassificationModel as _ClassificationModel
from DeltaShell.Plugins.Habitat.Models import FormulaBasedModel as _FormulaBasedModel
from DeltaShell.Plugins.Habitat.Models import MultipleClassificationModel as _MultipleClassificationModel
from DeltaShell.Plugins.Habitat.Models import StatisticsModel as _StatisticsModel

_HabitatLogger = _LogManager.GetLogger("HabitatFunctions")

class HabitatModelType:
    FormuleBased = 1
    BrokenLinearReclassification = 2
    SpatialStatistics = 3
    TableReclassification = 4
    MultiTableReclassification = 5
    CompositeModel = 6
    
def CreateModel(modelType):
	"""Creates a Habitat model based on the specified modelType"""
	if (modelType == HabitatModelType.FormuleBased):
		return _FormulaBasedModel()
	if (modelType == HabitatModelType.BrokenLinearReclassification):
		return _BrokenLinearModel()
	if (modelType == HabitatModelType.SpatialStatistics):
		return _StatisticsModel()
	if (modelType == HabitatModelType.TableReclassification):
		return _ClassificationModel()
	if (modelType == HabitatModelType.MultiTableReclassification):
		return _MultipleClassificationModel()
	if (modelType == HabitatModelType.CompositeModel):
		return _CompositeModel()
	
def ImportMapFromFile(filePath):
	"""Imports a map (regular grid) from the filePath 
	(Supported formats : .asc, .bil, .tif, .tiff, .map)"""
	return _RegularGridCoverageLoader.LoadFromFile(filePath)

def PrintMapInformation(map):
	info = ("Name = " + map.Name + "\r\n" + "\r\n" +
		   "Total size (w,h) = " + str(map.SizeX) + " x " + str(map.SizeY) + "\r\n" + 
		   "Cell size (w,h) = " + str(map.DeltaX) + " x " + str(map.DeltaY) + "\r\n" +
		   "Origin (x,y) = " + str(map.Origin.X) + ", " + str(map.Origin.Y) + "\r\n")
	_HabitatLogger.Info(info)

def CreateEquation(name, model, equation):
	"""Creates an equation for the specified model 
	(name can not contain spaces)"""
	if ((' ' in name) == True):
		_HabitatLogger.Error("name can not contain spaces (\"" + name + "\" is not valid)" )
		return
	
	newEquation = _Equation()
	newEquation.Name = name
	newEquation.EquationString = equation
	newEquation.Variables.AddRange(model.InputGridCoverages)
	newEquation.Parse(model.InputGridCoverages)		
	return newEquation

def ExportToFile(outputName, model, filePath):
	"""Exports the selected model output grid to the specified filePath
	(Supported formats : .asc, .bil, .tif, .tiff, .map)"""
	grid = GetItemByName(model.OutputGridCoverages, outputName)
	if (grid == None):
		_HabitatLogger.Error("Could not find " + outputName + " in model output")
		return
	
	exporter = _GdalFileExporter()
	exporter.Export(grid, filePath)
	return
	
def LinkMaps(sourceModel, sourceParameterName, targetModel, targetParameterName):
	"""Links parameters of two models to each other"""
	sourceDataItem = GetItemByName(sourceModel.OutputDataItemSet.DataItems, sourceParameterName)
	targetDataItem = GetItemByName(targetModel.InputDataItemSet.DataItems, targetParameterName)

	targetDataItem.LinkTo(sourceDataItem)

def AddBrokenLinearReclassificationRow(model, x, y):
	"""Adds a row with x,y to the model"""
	model.InputTables[0].Rows.Add(x,y)

def AddSpatialStatisticsRow(model, value, description = ""):
	"""Adds a row with values to the model"""
	
	# output value, Description, Grid1, Grid2 ... etc.
	rowValues = [value, description]
	array = _Array.CreateInstance(_Object,len(rowValues))
	
	for index in range(len(rowValues)):
		array[index] = rowValues[index]
		
	model.InputTables[0].Rows.Add(array)

def AddMultiTableReclassificationRow(model, values, output, description = ""):
	"""Adds a row with values to the model"""
	
	# output value, Description, Grid1, Grid2 ... etc.
	rowValues = [output, description] + values 
	array = _Array.CreateInstance(_Object,len(rowValues))
	
	for index in range(len(rowValues)):
		array[index] = rowValues[index]
		
	model.InputTables[0].Rows.Add(array)
	
def ClearAllRows(model):
	"""Clears all rows from the model"""
	model.InputTables[0].Rows.Clear()
	
def CreateEmptyMap():
	return _RegularGridCoverage()
	
def WriteToAsc(output, path):
    with open(path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ') 
    
        # write values
        writer.writerow(["ncols", output.SizeX])
        writer.writerow(["nrows", output.SizeY])
        writer.writerow(["xllcorner", output.Origin.X])
        writer.writerow(["yllcorner", output.Origin.Y])
        writer.writerow(["cellsize", output.DeltaX])
        writer.writerow(["NODATA_value", output.Components[0].NoDataValue])
        
        yValues = output.Arguments[0].Values;
        xValues = output.Arguments[1].Values;
        
        for i in range(0, output.SizeY):
            rowValues = []
            for j in range(0,output.SizeX):
                rowValues.append(output[yValues[output.SizeY - i -1], xValues[j]])

            writer.writerow(rowValues)

def WriteStatisticsToCSV(model, path, delimiter = ";"):
    statistics_output = model.Statistics
    with open(path, 'w') as csvfile:
	statistics_lines = statistics_output.split("\n")
	for nr, row in enumerate(statistics_lines):
		if(nr == 0):
			continue
		row_list = row.replace("\t",delimiter)
		csvfile.writelines(row_list)
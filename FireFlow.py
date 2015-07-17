#################################################################################################################################
# Name: Elizabeth Rentschlar                                                                                                    #
# Purpose:                                                                                                                      #
# Created: 5/13/15                                                                                                              #
# Copyright: (c) City of Bryan                                                                                                  #
# ArcGIS Version: 10.2.2                                                                                                        #
# Python Version: 2.7                                                                                                           #
#################################################################################################################################

# Import arcpy module
import arcpy
from arcpy import env
import arcpy.mapping
#from arcpy.sa import *

# Set workspace
env.overwriteOutput = True
work_space = r"C:\Users\erentschlar\Desktop\ToDelete"
# arcpy.env.workspace = arcpy.GetParameterAsText(0)
env.workspace = work_space

# Script arguments
sde_GIS_ADMIN_COB_WATER_HYDRANTS = arcpy.GetParameterAsText(0)
if sde_GIS_ADMIN_COB_WATER_HYDRANTS == '#' or not sde_GIS_ADMIN_COB_WATER_HYDRANTS:
    sde_GIS_ADMIN_COB_WATER_HYDRANTS = "sde.GIS_ADMIN.COB_WATER_HYDRANTS" # provide a default value if unspecified

BRYAN__CITY_LIMITS = arcpy.GetParameterAsText(1)
if BRYAN__CITY_LIMITS == '#' or not BRYAN__CITY_LIMITS:
    BRYAN__CITY_LIMITS = "BRYAN  CITY LIMITS" # provide a default value if unspecified

# Local variables:
COB_Hydrants_shp = sde_GIS_ADMIN_COB_WATER_HYDRANTS
ThiessenPolygon_shp = COB_Hydrants_shp
ThiessenPolygon_shp__3_ = ThiessenPolygon_shp
ThiessenPolygon_shp__5_ = ThiessenPolygon_shp__3_
ThiessenPolygon_shp__4_ = ThiessenPolygon_shp__5_
FireFlow_shp = ThiessenPolygon_shp__4_

# Process: Select
arcpy.Select_analysis(sde_GIS_ADMIN_COB_WATER_HYDRANTS, COB_Hydrants_shp, "PITOT_GPM > 0 AND CCN_ENTITY = 'COB'")

# Process: Create Thiessen Polygons
arcpy.CreateThiessenPolygons_analysis(COB_Hydrants_shp, ThiessenPolygon_shp, "ALL")

# Process: Add Field
arcpy.AddField_management(ThiessenPolygon_shp, "GPM_Range", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field 
arcpy.CalculateField_management(ThiessenPolygon_shp__3_, "GPM_Range", "[PITOT_GPM]", "VB", "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(ThiessenPolygon_shp__5_, "GPM_Range", "Reclass(!GPM_Range!)", "PYTHON_9.3", "def Reclass(GPM_Range):\\n    if (int(GPM_Range)<=499):\\n        return \"0-499\"\\n    elif (int(GPM_Range)>=500 and int(GPM_Range)<=999):\\n        return \"500-999\"\\n    elif (int(GPM_Range)>=1000 and int(GPM_Range)<=1499):\\n        return \"1000-1499\"\\n    elif (int(GPM_Range)>=1500):\\n        return \"1500-2000\"")

# Process: Clip
arcpy.Clip_analysis(ThiessenPolygon_shp__4_, BRYAN__CITY_LIMITS, FireFlow_shp, "")



mapdoc = arcpy.mapping.MapDocument(r"G:\GIS_PROJECTS\WATER_SERVICES\Hydrants\FireFlow.mxd")

#Data Frame
listdf = arcpy.mapping.ListDataFrames(mapdoc)
data_frame = listdf[0]
listdf[0].scale = 90000

#Paths to the Layers and Shapefiles
#LyrCL = arcpy.mapping.Layer(r"G:\4_LAYERS\COB_CITY_LIMITS.lyr")
#LyrFF = arcpy.mapping.Layer(r"G:\GIS_PROJECTS\WATER_SERVICES\Hydrants\FireFlowSymbology.lyr")
#LyrST = arcpy.mapping.Layer(r"G:\4_LAYERS\COB_STREET_HISTORY_1996-2014.lyr")

# Adding the relevant layers	
#arcpy.mapping.AddLayer( data_frame ,LyrST,"TOP")
#arcpy.mapping.AddLayer( data_frame ,LyrCL,"BOTTOM")
#arcpy.mapping.AddLayer( data_frame ,LyrFF,"BOTTOM")


## Page Layout Elements
# Date for Title
import datetime
mydate = datetime.datetime.now()
month = mydate.strftime("%B")
year = mydate.strftime("%Y")

# Set Title Text
title = arcpy.mapping.ListLayoutElements(mapdoc, "TEXT_ELEMENT")[0]
title.text = "Analysis of Measured Fire Flow (Pitot GPM) " + month + " " + year

# May not be necessary 
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
mapdoc.save()

# Create PDF
pdf = r"G:\GIS_PROJECTS\WATER_SERVICES\Hydrants\FireFlow" +month + year + ".pdf"
arcpy.mapping.ExportToPDF(mapdoc, pdf )
#"PAGE_LAYOUT", , ,300, "BEST", "RGB", 1,"ADAPTIVE", "RASTERIZE_BITMAP",0,1,"LAYERS_ONLY",1,80
#arcpy.ApplySymbologyFromLayer_management()

# Finishing 

del mapdoc

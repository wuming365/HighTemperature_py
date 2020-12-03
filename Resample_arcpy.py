# -*- coding:utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")

inputpath = r"G:\high_temperture202011\turn"
outputpath = r"G:\high_temperture202011\turn_1"
for _, _, filenames in os.walk(inputpath):
    for filename in filenames:
        if filename[-4:]==".tif":
            filePathin = os.path.join(inputpath, filename)
            filePathout = os.path.join(outputpath, filename)
            arcpy.Resample_management(in_raster=filePathin, out_raster=filePathout,
                                    cell_size="0.00083333333 0.00083333333", resampling_type="NEAREST")
            print("processing "+filename)
# -*- coding:utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")

inputpath = r"H:\high_temperture202011\turn"
outputpath = r"H:\high_temperture202011\turn"
for _, _, filenames in os.walk(inputpath):
    for filename in filenames:
        filePathin = os.path.join(inputpath, filename)
        filePathout = os.path.join(outputpath, "1"+filename)
        arcpy.Resample_management(in_raster=filePathin, out_raster=filePathout,
                                  cell_size="0.00083333333 0.00083333333", resampling_type="NEAREST")
        print("processing "+filename)
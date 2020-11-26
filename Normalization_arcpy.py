# -*- coding: utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错
indexnames = {
    'max': 1,
    'HT_frequency': 1,
    'HT_duration': 1,
    'pop': 1,
    'deltaY': 1,
    'delatYpeople': 1,
    'NDVI': 1,
    'virrs': 1,
    'GDP': 1,
    'Euc': 0,
    'IMS': 0,
    'Danger': 1,
    'Expo': 1,
    'Vulner': 1,
    'DPE': 0,
    'Final': 1
}


def Normalize(path_input, path_output, isPositive):
    print ("Processing " + path_input.split("\\")[-1])
    try:
        maxValue = arcpy.GetRasterProperties_management(path_input, "MAXIMUM")
    except arcgisscripting.ExecuteError:
        # print(path_input.split("\\")[-1]+" need to calculate statistics")
        arcpy.CalculateStatistics_management(path_input)
    maxValue = arcpy.GetRasterProperties_management(path_input, "MAXIMUM")
    maxValue = maxValue.getOutput(0)

    minValue = arcpy.GetRasterProperties_management(path_input, "MINIMUM")
    minValue = minValue.getOutput(0)
    # print(maxValue)
    if float(maxValue)-float(minValue)!=0:
        # print ("Processing " + path_input.split("\\")[-1])
        if isPositive:
            NormalizationRaster = (
                Raster(path_input)-float(minValue))/(float(maxValue)-float(minValue))
        else:
            NormalizationRaster = (
                float(maxValue)-Raster(path_input))/(float(maxValue)-float(minValue))
    else:
        # print("max and min equal 0")
        NormalizationRaster=Raster(path_input)

    if not os.path.exists(path_output):
        NormalizationRaster.save(path_output)
    # return 1

def getIndexname(filename):
    a = filename.split("_")
    
    if len(a) == 4:
        return a[2]
    else:
        m=a[1].split(".")[0]
        return m


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder "+foldername+" is created")


def main():
    path_dirinput = r"H:\high_temperture202011\result_data"
    calcu = ["positive", "negative"]
    path_diroutput = r"H:\high_temperture202011\result_normalized"
    for name in calcu:
        path_dir = "{}\\{}".format(path_dirinput, name)
        for _, _, filenames in os.walk(path_dir):
            for filename in filenames:
                if filename[-4:] == ".tif":
                    index = getIndexname(filename)
                    path_index = path_diroutput+"\\"+index
                    mkdir(path_index)
                    path_input = path_dir+"\\"+filename
                    path_output = path_index+"\\"+filename
                    Normalize(path_input, path_output, name == "positive")


def main_testIndex():

    path_input = r"H:\high_temperture202011\result_data"
    calcu = ["positive", "negative"]
    b = 0
    for name in calcu:
        path_dir = "{}\\{}".format(path_input, name)
        for _, _, filenames in os.walk(path_dir):
            for filename in filenames:
                if filename[-4:] == ".tif":
                    index = getIndexname(filename)
                    b += 1
                    if index not in indexnames:
                        print ("Error")
                        return
    print (b/9)

def main_testNormalization():
    path_dirinput = r"H:\high_temperture202011\result_data"
    calcu = ["positive", "negative"]
    path_output = r"H:\high_temperture202011\result_normalized"
    num=0
    for name in calcu:
        path_dir = "{}\\{}".format(path_dirinput, name)
        for _, _, filenames in os.walk(path_dir):
            for filename in filenames:
                if filename[-4:] == ".tif":
                    index = getIndexname(filename)
                    path_index = path_output+"\\"+index
                    # mkdir(path_index)
                    path_input = path_dir+"\\"+filename
                    path_output = path_index+"\\"+filename
                    num+=Normalize(path_input, path_output, name == "positive")
    print(num)

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错

def getIndexPeakValue(path_dir,filenames):
    peakValue=dict()
    for filename in filenames:
        path_input=os.path.join(path_dir,filename)
        index = getIndexname(filename)
        try:
            maxValue = arcpy.GetRasterProperties_management(path_input, "MAXIMUM")
        except arcgisscripting.ExecuteError:
                # print(path_input.split("\\")[-1]+" need to Calculate statistics")
            arcpy.CalculateStatistics_management(path_input)
        print(path_input)
        maxValue = arcpy.GetRasterProperties_management(path_input, "MAXIMUM")
        maxValue = float(maxValue.getOutput(0))

        minValue = arcpy.GetRasterProperties_management(path_input, "MINIMUM")
        minValue = float(minValue.getOutput(0))
        if index not in peakValue.keys():
            peakValue[index]=[minValue,maxValue,path_input.split("\\")[-1].split("_")[0],path_input.split("\\")[-1].split("_")[0]]
        else:
            if minValue<peakValue[index][0]:
                peakValue[index][0]=minValue
                peakValue[index][2]=path_input.split("\\")[-1].split("_")[0]
            if maxValue>peakValue[index][1]:
                peakValue[index][1]=maxValue
                peakValue[index][3]=path_input.split("\\")[-1].split("_")[0]
    return peakValue

def Normalize(peakValue,index,path_input, path_output, isPositive):
    minValue,maxValue,_,_=peakValue[index]
    # print(maxValue)
    if float(maxValue)-float(minValue) != 0:
        # print ("Processing " + path_input.split("\\")[-1])
        if isPositive:
            NormalizationRaster = (
                Raster(path_input)-float(minValue))/(float(maxValue)-float(minValue))
            # print(path_input)
            # print(str(NormalizationRaster.height)+" "+str(Raster(path_input).height))
        else:
            NormalizationRaster = (
                float(maxValue)-Raster(path_input))/(float(maxValue)-float(minValue))
    else:
        # print("max and min equal 0")
        NormalizationRaster = Raster(path_input)

    if not os.path.exists(path_output):
        NormalizationRaster.save(path_output)
        print ("Processing " + path_input.split("\\")[-1])
    else:
        print(path_input.split("\\")[-1] + " already exists")
    # return 1


def getIndexname(filename):
    a = filename.split("_")

    if len(a) == 4:
        if a[1] == "HT":
            return a[1]+"_"+a[2]
        else:
            return a[2]
    else:
        m = a[1].split(".")[0]
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
    path_dirinput = r"../{}/result_data".format(YEAR)
    path_diroutput = r"../{}/result_normalized".format(YEAR)
    for name in CALCU:
        path_dir = "{}\\{}".format(path_dirinput, name)
        filenames=[i for i in os.listdir(path_dir) if i.endswith("tif")]
        peakValue=getIndexPeakValue(path_dir,filenames)
        with open("../2010/result_data/peakValue.txt","a") as f:
            for p in peakValue:
                f.write("{}:{},\n".format(p,str(peakValue[p])))
        for filename in filenames:
            if filename[-4:] == ".tif":
                index = getIndexname(filename)
                path_index = path_diroutput+"\\"+index
                mkdir(path_index)
                path_input = path_dir+"\\"+filename
                path_output = path_index+"\\"+filename
                Normalize(peakValue, index, path_input, path_output, name == "positive")


# def main_testIndex():

#     path_input = r"G:\high_temperture202011\result_data"

#     b = 0
#     for name in CALCU:
#         path_dir = "{}\\{}".format(path_input, name)
#         for _, _, filenames in os.walk(path_dir):
#             for filename in filenames:
#                 if filename[-4:] == ".tif":
#                     index = getIndexname(filename)
#                     print(index)
#                     b += 1
#                     if index not in INDEXNAMES:
#                         print ("Error")
#                         return
#     print (b/12)

# def main_testNormalization():
#     path_dirinput = r"H:\high_temperture202011\result_data"
#     CALCU = ["positive", "negative"]
#     path_output = r"H:\high_temperture202011\result_normalized"
#     num=0
#     for name in CALCU:
#         path_dir = "{}\\{}".format(path_dirinput, name)
#         for _, _, filenames in os.walk(path_dir):
#             for filename in filenames:
#                 if filename[-4:] == ".tif":
#                     index = getIndexname(filename)
#                     path_index = path_output+"\\"+index
#                     # mkdir(path_index)
#                     path_input = path_dir+"\\"+filename
#                     path_output = path_index+"\\"+filename
#                     num+=Normalize(path_input, path_output, name == "positive")
#     print(num)


if __name__ == "__main__":
    main()

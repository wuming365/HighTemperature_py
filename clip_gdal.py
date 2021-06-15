import sys
import os.path
import re
import shutil
import stat
import time
from collections import namedtuple
from os.path import getsize, join
from CONSTANT import *
from osgeo import gdal
import numpy as np
import numpy.ma as ma
from osgeo import ogr
import shapefile
import xlrd
from scipy import stats
from tqdm import tqdm
from tqdm.std import trange

def writeTiff(im_data, im_geotrans, im_proj, NDV, dirpath, filename):
    """
    im_data:ndarray,2维或3维数据
    dirpath:str或str_array
    """
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    number = 1
    im_bands = 1  # 均为单波段影像
    fullpath = []
    newpath = []
    newim_data = []
    newfilename = []
    mkdir(dirpath)
    isSingleImg = 0  # 0 Multi ; 1 Single ; 2 Error
    b_isSingleImg = False
    # 把imdata维度变为三维
    if isinstance(filename, str):
        if (len(im_data.shape) == 3):
            if (len(im_data[0]) == 1):
                isSingleImg = 1
            else:
                isSingleImg = 2
        else:
            isSingleImg = 1
            im_data = [im_data]
    else:
        if (len(im_data.shape) == 3):
            if (len(im_data[0]) == 1):
                isSingleImg = 2
        else:
            isSingleImg = 2
    if isSingleImg == 2:
        print("Error:Different images and files!!!")
        return
    elif isSingleImg == 1:
        print("Tips:There is one single Image")
        b_isSingleImg = True
    elif isSingleImg == 0:
        print(f"Tips:There are {len(im_data[0])} images")
        b_isSingleImg = False
    if b_isSingleImg:
        if filename[-5:] != ".tiff" and filename[-4:] != ".tif":
            filename = filename + ".tif"
        fullpath = [dirpath + "\\" + filename]
        filename = [filename]
    else:
        for i in range(len(filename)):
            if filename[i][-5:] != ".tiff" and filename[i][-4:] != ".tif":
                filename[i] = filename[i] + ".tif"
            fullpath.append(dirpath + "\\" + filename[i])

    number = len(im_data)
    im_height, im_width = im_data[0].shape
    newpath = fullpath
    newim_data = im_data
    newfilename = filename

    with tqdm(range(number)) as t:
        for i in t:
            # 创建文件
            driver = gdal.GetDriverByName("GTiff")
            dataset = driver.Create(newpath[i], im_width, im_height, im_bands,
                                    datatype)
            if (dataset != None):
                dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
                dataset.SetProjection(im_proj)  # 写入投影
                dataset.GetRasterBand(1).SetNoDataValue(NDV)  # 设置nodata值
            for band in range(im_bands):
                dataset.GetRasterBand(band + 1).WriteArray(newim_data[i])
            del dataset
            t.set_description(newfilename[i] + " has been successfully built")
        print("-" * 120)

def main():
    
    path_dirinput = r"E:\high_temperture202011"
    path_dirshp = r"../extent"
    path_dirout = r"G:\high_temperture202011\turn"
    with tqdm(REGIONNAMES) as t:
        for region in t:
            regionname = region
            countryname = REGIONNAMES[region]
            path_inputraster = f"{path_dirinput}\\{regionname}_road_Euc_2020.tif"  #python3
            path_clipshp = f"{path_dirshp}\\{regionname}.shp"
            path_outputraster = f"{path_dirout}\\{regionname}_road_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, NDV)

            path_inputraster = f"{path_dirinput}\\{regionname}_hospital_Euc_2020.tif"  #python3
            path_outputraster = f"{path_dirout}\\{regionname}_hospital_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, NDV)

            path_inputraster = f"{path_dirinput}\\{regionname}_water_Euc_2020.tif"  #python3
            path_outputraster = f"{path_dirout}\\{regionname}_water_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, NDV)
            # t.set_description(regionname)
    #shutil.rmtree(path_dirinput)
    # os.rename(path_dirout,path_dirinput)


if __name__ == "__main__":
    main()

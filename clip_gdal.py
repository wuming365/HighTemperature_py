import sys
import os.path
import re
import shutil
import stat
import time
from collections import namedtuple
from os.path import getsize, join

import gdal
import numpy as np
import numpy.ma as ma
import ogr
import shapefile
import xlrd
from scipy import stats
from tqdm import tqdm
from tqdm.std import trange


def openSingleImage(imagefilename):
    """
    打开遥感影像
    """
    dataset = gdal.Open(imagefilename)
    im_width = dataset.RasterXSize  # 列数
    im_height = dataset.RasterYSize  # 行数
    # im_bands = dataset.RasterCount  # 波段数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_band = dataset.GetRasterBand(1)
    Image = im_band.ReadAsArray(0, 0, im_width, im_height)
    del dataset
    # 关闭图像进程
    return np.double(Image), im_geotrans, im_proj


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder "+foldername+" is created")

    else:
        print("There is a folder called "+foldername)


def writeTiff(im_data, im_geotrans, im_proj, ndv, dirpath, filename):
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
        if(len(im_data.shape) == 3):
            if(len(im_data[0]) == 1):
                isSingleImg = 1
            else:
                isSingleImg = 2
        else:
            isSingleImg = 1
            im_data = [im_data]
    else:
        if(len(im_data.shape) == 3):
            if(len(im_data[0]) == 1):
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
            filename = filename+".tif"
        fullpath = [dirpath+"\\"+filename]
        filename = [filename]
    else:
        for i in range(len(filename)):
            if filename[i][-5:] != ".tiff" and filename[i][-4:] != ".tif":
                filename[i] = filename[i]+".tif"
            fullpath.append(dirpath+"\\"+filename[i])

    number = len(im_data)
    im_height, im_width = im_data[0].shape
    newpath = fullpath
    newim_data = im_data
    newfilename = filename

    with tqdm(range(number)) as t:
        for i in t:
            # 创建文件
            driver = gdal.GetDriverByName("GTiff")
            dataset = driver.Create(
                newpath[i], im_width, im_height, im_bands, datatype)
            if(dataset != None):
                dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
                dataset.SetProjection(im_proj)  # 写入投影
                dataset.GetRasterBand(1).SetNoDataValue(ndv)  # 设置nodata值
            for band in range(im_bands):
                dataset.GetRasterBand(band+1).WriteArray(newim_data[i])
            del dataset
            t.set_description(newfilename[i]+" has been successfully built")
        print("-"*120)


def clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv):
    """
    裁剪影像
    path_inputraster:str
    path_outputraster:str
    path_clipshp:str
    """
    input_raster = gdal.Open(path_inputraster)
    mkdir(os.path.dirname(path_outputraster))
    # 两个投影一样
    r = shapefile.Reader(path_clipshp)
    ds = gdal.Warp(path_outputraster,
                   input_raster,
                   format='GTiff',
                   outputBounds=r.bbox,
                   cutlineDSName=path_clipshp,
                   dstNodata=ndv
                   )
    ds = None


def main():
    regionnames = {
        # 'Abbas': 'irn',
        # 'Karachi': 'pak',
        # 'Alexandria': 'egy',
        # 'Gawdar': 'pak',
        # 'Kolkata': 'ind',
        # 'Maldives': 'mdv',
        # 'Mumbai': 'ind',
        # 'Tashkent': 'uzb',
        # 'Teran': 'irn',
        # 'Ankara': 'tur',
        # 'Piraeus': 'grc',
        # 'Melaka': 'mys',
        # 'Kuantan': 'mys',
        # 'Hambantota': 'lka',
        # 'Colombo': 'lka',
        # 'Minsk': 'blr',
        # 'Warsaw': 'pol',
        # 'Yawan': 'idn',
        # 'Valencia': 'esp',
        'Ekaterinburg': 'rus',
        'Novosibirsk': 'rus'
    }
    ndv = -3.4028234663852886e+38
    #ndv=255
    path_dirinput = r"E:\high_temperture202011"
    path_dirshp = r"E:\High temperature heat wave vulnerability\extent"
    path_dirout = r"G:\high_temperture202011\turn"
    with tqdm(regionnames) as t:
        for region in t:
            regionname = region
            countryname = regionnames[region]
            path_inputraster = f"{path_dirinput}\\{regionname}_road_Euc_2020.tif" #python3
            path_clipshp = f"{path_dirshp}\\{regionname}.shp"
            path_outputraster = f"{path_dirout}\\{regionname}_road_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv)

            path_inputraster = f"{path_dirinput}\\{regionname}_hospital_Euc_2020.tif" #python3
            path_outputraster = f"{path_dirout}\\{regionname}_hospital_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv)

            path_inputraster = f"{path_dirinput}\\{regionname}_water_Euc_2020.tif" #python3
            path_outputraster = f"{path_dirout}\\{regionname}_water_Euc_2020.tif"
            clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv)
            # t.set_description(regionname)
    #shutil.rmtree(path_dirinput)
    # os.rename(path_dirout,path_dirinput)


if __name__ == "__main__":
    main()

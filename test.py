# -*-coding:utf-8 -*-
import os
import os.path
import re
from collections import namedtuple

from osgeo import gdal
import numpy as np
import numpy.ma as ma
from osgeo import ogr
import shapefile
import xlrd
from scipy import stats
from tqdm import tqdm
from tqdm.std import trange

import time

# NDV = -3.4028234663852886e+38
NDV = -9999


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder " + foldername + " is created")

    # else:
    # print("There is a folder called " + foldername)


def clipTiff(path_inputraster, path_outputraster, path_clipshp, NDV=NDV):
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
                   dstNodata=NDV)
    ds = None
    print("Cliping " + path_outputraster)


path = r"../2010/turn"
path_out = r"../2010/turn_1"
path_clip = r"../extent"
filenames = [i for i in os.listdir(path) if i.endswith(".tif")]
for filename in filenames:
    clipTiff(os.path.join(path, filename), os.path.join(path_out, filename),
             os.path.join(path_clip,
                          filename.split("_")[0] + ".shp"))

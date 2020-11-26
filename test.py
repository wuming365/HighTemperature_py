# -*-coding:utf-8 -*-
import os
import os.path
import re
from collections import namedtuple

import gdal
import numpy as np
import numpy.ma as ma
import ogr
import shapefile
import xlrd
from scipy import stats
from tqdm import tqdm
from tqdm.std import trange

import time

# data=numpy.random.randint(5,size=(2,3,4))
# print(data)
# print(numpy.transpose(data))
# print(numpy.transpose(numpy.transpose(data)))
# ndv=3
# mode,count=stats.mode(data)
# a="Karachi20150102.tif"
# print(a[18:])
# print(data.max(axis=0))
# dataa=np.array([5,4,3,2,1])
# suma=0
# print([suma+a for a in dataa])
# data2=numpy.array([1,9,8,6,7])


# data2[data2<2]=10
# print(numpy.append(data,dataa,axis=0))
# for i in trange(1,101,ascii=True,desc="ninhao"):
#     time.sleep(0.05)
# a=ma.masked_where(data==1,data)+1
# print(a.filled(fill_value=1000))
# p=numpy.percentile(data[0],numpy.array([50,75,80]))
# print(p)
# a=numpy.zeros((10000,10000))
# b=numpy.zeros((10000,10000))
# c=numpy.zeros((10000,10000))

# b=np.random.randint(2,size=1000000)
# time1_start=time.perf_counter()
# c=''.join(str(i) for i in b)
# d=np.array([len(i) for i in c.split('0')])
# print(len(d[d>=3]))
# time1_end=time.perf_counter()
# print(time1_end-time1_start)
# time2_start=time.perf_counter()
# c=np.split(b,np.where(np.diff(b)<0)[0]+1)
# d=np.array([np.sum(i) for i in c])
# print(len(d[d>=3]))
# time2_end=time.perf_counter()
# print(time2_end-time2_start)

# b=np.random.randint(2,size=(5,2,2))
# c=np.split(b,np.where(np.diff(b)<0)[0]+1,axis=1)
# print(b.shape)
# print(c)
# d=np.array([np.sum(i) for i in c])
# print(len(d[d>=3]))

# def openSingleImage(imagefilename):
#     """
#     打开遥感影像
#     """
#     dataset = gdal.Open(imagefilename)
#     im_width = dataset.RasterXSize  # 列数
#     im_height = dataset.RasterYSize  # 行数
#     # im_bands = dataset.RasterCount  # 波段数
#     im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
#     im_proj = dataset.GetProjection()  # 地图投影信息
#     im_band = dataset.GetRasterBand(1)
#     Image = im_band.ReadAsArray(0, 0, im_width, im_height)
#     del dataset
#     # 关闭图像进程
#     return np.double(Image), im_geotrans, im_proj
# def clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv):
#     """
#     裁剪影像
#     path_inputraster:str
#     path_outputraster:str
#     path_clipshp:str
#     """
#     input_raster = gdal.Open(path_inputraster)

#     # 两个投影一样
#     r = shapefile.Reader(path_clipshp)
#     ds = gdal.Warp(path_outputraster,
#                    input_raster,
#                    format='GTiff',
#                    outputBounds=r.bbox,
#                    cutlineDSName=path_clipshp,
#                    dstNodata=ndv
#                    )
#     ds = None
# def writeTiff(im_data, im_geotrans, im_proj, ndv, dirpath, filename):
#     """
#     im_data:ndarray,2维或3维数据
#     dirpath:str或str_array
#     """
#     if 'int8' in im_data.dtype.name:
#         datatype = gdal.GDT_Byte
#     elif 'int16' in im_data.dtype.name:
#         datatype = gdal.GDT_UInt16
#     else:
#         datatype = gdal.GDT_Float32
#     number = 1
#     im_bands = 1  # 均为单波段影像
#     fullpath = []
#     newpath = []
#     newim_data = []
#     newfilename = []
#     # mkdir(dirpath)
#     isSingleImg=0 #0 Multi ; 1 Single ; 2 Error
#     b_isSingleImg=False
#     # 把imdata维度变为三维
#     if isinstance(filename, str):
#         if(len(im_data.shape)==3):
#             if(len(im_data[0])==1):
#                 isSingleImg=1
#             else:
#                 isSingleImg=2
#         else:
#             isSingleImg=1
#             im_data=[im_data] 
#     else:
#         if(len(im_data.shape)==3):
#             if(len(im_data[0])==1):
#                 isSingleImg=2
#         else:
#             isSingleImg=2
#     if isSingleImg==2:
#         print ("Error:Different images and files!!!")
#         return
#     elif isSingleImg==1:
#         print ("Tips:There is one single Image")
#         b_isSingleImg=True
#     elif isSingleImg==0:
#         print (f"Tips:There are {len(im_data[0])} images")
#         b_isSingleImg=False
#     if b_isSingleImg:
#         if filename[-5:] != ".tiff" and filename[-4:] != ".tif":
#             filename = filename+".tif"
#         fullpath = [dirpath+"\\"+filename]
#         filename=[filename]
#     else:
#         for i in range(len(filename)):
#             if filename[i][-5:] != ".tiff" and filename[i][-4:] != ".tif":
#                 filename[i] = filename[i]+".tif"
#             fullpath.append(dirpath+"\\"+filename[i])
    
#     number= len(im_data)
#     im_height, im_width=im_data[0].shape
#     newpath = fullpath
#     newim_data = im_data
#     newfilename = filename

#     with tqdm(range(number)) as t:
#         for i in t:
#             # 创建文件
#             driver = gdal.GetDriverByName("GTiff")
#             dataset = driver.Create(
#                 newpath[i], im_width, im_height, im_bands, datatype)
#             if(dataset != None):
#                 dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
#                 dataset.SetProjection(im_proj)  # 写入投影
#                 dataset.GetRasterBand(1).SetNoDataValue(ndv)  # 设置nodata值
#             for band in range(im_bands):
#                 dataset.GetRasterBand(band+1).WriteArray(newim_data[i])
#             del dataset
#             t.set_description(newfilename[i]+" has been successfully built")
#         print("-"*120)

# def main():
#     path_img_1="H:/高温热浪数据202011/中转/B2_20170720.tif"
#     path_img_2="H:/高温热浪数据202011/中转/B2_20170728.tif"
#     img,im_geotrans,im_proj=openSingleImage("E:/High temperature heat wave vulnerability/delatYpeople/karachi/karachi_delatYpeople_65_80.tif")
#     ndv=-3.4028230607370965e+38 #novalue值
#     ndv_1=-3.4028234663852886e+38 #img 的
#     path_shp="E:/interpolate/extent/Karachi.shp"
#     height,width=img.shape
#     # clipTiff(path_img_1,"H:/高温热浪数据202011/中转/B2_20170720_1.tif",path_shp,ndv)
#     # clipTiff(path_img_2,"H:/高温热浪数据202011/中转/B2_20170728_1.tif",path_shp,ndv)
#     img_1=openSingleImage("H:/高温热浪数据202011/中转/B2_20170720_1.tif")[0]
#     img_2=openSingleImage("H:/高温热浪数据202011/中转/B2_20170728_1.tif")[0]
#     img_1=ma.masked_where(img == ndv_1, img_1)
#     img_2=ma.masked_where(img == ndv_1, img_2)
#     Ig=np.zeros_like(img)
#     Ig=ma.masked_where(img == ndv_1, Ig)
#     for i in range(height):
#         for j in range(width):
#             if all([img_1[i][j]==ndv,img_2[i][j]!=ndv]):
#                 Ig[i][j]=img_2[i][j]
#             elif all([img_1[i][j]!=ndv,img_2[i][j]==ndv]):
#                 Ig[i][j]=img_1[i][j]
#             elif all([img_1[i][j]!=ndv,img_2[i][j]!=ndv]):
#                 Ig[i][j]=(3*img_1[i][j]+img_2[i][j])/4
#     Ig=Ig.filled(ndv_1)
#     writeTiff(Ig,im_geotrans,im_proj,ndv_1,"H:/高温热浪数据202011/中转","NDVI_20150724_karachi")

# if __name__ == "__main__":
#     main()

# a=np.array([[[1,2],[2,3]],[[1,2],[2,3]],[[1,3],[1,3]],[[2,4],[4,2]]])
# a=ma.masked_where(a==1,a)
a="ma.tif"
b="ma"
print(a.split(".")[0])
print(b.split(".")[0])
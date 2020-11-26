import gdal
import numpy as np
import os
import time
from tqdm import tqdm
from tqdm import trange


def openSingleImage(imagefilename):
    """读取影像文件"""
    dataset = gdal.Open(imagefilename)
    im_width = dataset.RasterXSize  # 列数
    im_height = dataset.RasterYSize  # 行数
    im_bands = dataset.RasterCount  # 波段数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    # 共有六个参数，分别代表分表代表左上角x坐标；东西方向上图像的分辨率；如果北边朝上，地图的旋转角度，0表示图像的行与x轴平行；左上角y坐标；
    # 如果北边朝上，地图的旋转角度，0表示图像的列与y轴平行；南北方向上地图的分辨率。
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_band = dataset.GetRasterBand(1)
    Image = im_band.ReadAsArray(0, 0, im_width, im_height)
    del dataset
    # 关闭图像进程
    return np.double(Image), im_geotrans, im_proj
def write_img(im_data, filename, im_proj, im_geotrans, dirpath):
    """写影像"""
    # im_data被写的影像
    # im_proj, im_geotrans均为被写影像参数
    # filename创建新影像的名字，dirpath影像写入文件夹

    # 判断栅格数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    filepath = []
    if isinstance(filename, str):
        filepath = dirpath + "\\" + filename
    else:
        for i in range(len(filename)):
            filepath.append(dirpath + "\\" + filename[i])
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape  # 一维矩阵
        print("Error:There is no way to get here!!!!")
    # 创建文件
    ndv = -3.4028234663852886e+38
    with trange(im_bands) as t:
        for i in t:
            driver = gdal.GetDriverByName('GTiff')  # 数据类型必须有，因为要计算需要多大内存空间
            data = driver.Create(filepath[i], im_width, im_height, im_bands, datatype)
            data.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
            data.SetProjection(im_proj)  # 写入投影
            data.GetRasterBand(1).SetNoDataValue(ndv)
            if im_bands == 1:
                data.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
            else:
                for h in range(im_bands):
                    data.GetRasterBand(h + 1).WriteArray(im_data[i])
            del data
    t.set_description(filename[i]+" has been successfully built")

def openImages(dirpath):
    """
    打开工作文件夹中的所有影像
    dirpath:数据读取文件夹
    return:Igs,im_geotrans.im_proj
    """
    Igs = []
    for dirPath, dirname, filenames in os.walk(dirpath):
        idate = 0
        with tqdm(filenames) as t:
            for filename in t:
                if filename[-4:] == ".tif":
                    Image, im_geotrans, im_proj = openSingleImage(dirPath + "\\" + filename)
                    Igs.append(Image)
                    idate = idate + 1
                    t.set_description(filename + " is already open……")
    return Igs, im_geotrans, im_proj

def GetpercentImages(Igs,percent):
    """计算时间序列图像百分位数 """
    height, width = Igs[0].shape
    perImages = np.empty((width, height,3), dtype="double")
    with tqdm(range(0, width)) as t:
        for i in t:
            for j in range(0, height):
                perImages[i][j] = np.percentile(
                    np.transpose(Igs)[i][j], percent)
            t.set_description("Proceeding col "+str(i))
    return np.transpose(perImages)
def heatwaveJud(name,perpath,dirpath1,outputpath):
    """判断是否发生热浪"""
    #name节点名称
    #perpath阈值标准所在路径
    #dirpath1影像所在路径
    #outputpath影像输出路径
    preImage = perpath +"\\"+name+"pre_85.tif"
    durname1 = name + "HT_duration.tif"
    frename1 = name + "HT_frequency.tif"
    height, width = preImage.shape
    heatwaveimg = []
    for dirPath, dirname, filenames in os.walk(dirpath1):
        with tqdm(filenames) as t:
            for filename in t:
                if filename[-4:] == ".tif":
                    Image, im_geotrans, im_proj = openSingleImage(dirPath + "\\" + filename)
                    newImage = []
                    for i in trange(0,width):
                        for j in trange(0,height):
                            if Image[i][j] > preImage[i][j] and Image[i][j] > 28:
                                newImage[i][j] = 1
                            else:
                                newImage[i][j] = 0
                    heatwaveimg.append(newImage)
    """计算热浪持续时间"""
    durimg = np.empty((width, height, 3), dtype="double")
    for i in trange(0, width):
        for j in trange(0, height):
            durimg[i][j] = sum(heatwaveimg[i][j])
    write_img(durimg, durname1, im_proj, im_geotrans, outputpath)
    """计算热浪发生频率"""
    fre = []
    dur = []
    row_dur = np.empty((width, height, 3), dtype="double")
    for i in trange(0, width):
        for j in trange(0, height):
            x = 0
            if heatwaveimg[x][i][j] != 0:
                row_dur[i][j] += 1
                x += 1
                dur.append(row_dur)
            else:
                continue
    frevalue = np.empty((width, height, 3), dtype="double")
    for i in trange(0, width):
        for j in trange(0, height):
            for k in (1, len(dur)):
                if dur[k][i][j] < 3:
                    frevalue[i][j] = 0
            else:
                if dur[k + 1][i][j] == 0:
                    frevalue[i][j] = 1
                else:
                    frevalue[i][j] = 0
            fre.append(frevalue)
        freimg = sum(fre)
    write_img(freimg, frename1, im_proj, im_geotrans, outputpath)

def main():
    precent = [85,90,95]
    name = "Maldives"
    dirPath1 = "H:/data_100m/4_HTEMPX/Maldives"
    dirPath2 = "H:/data_100m/4_HTEMPX/precent"
    outputpath = "H:/data_100m/4_HTEMPX/heatwave"
    Igs, im_geotrans, im_proj = openImages(dirPath1)
    preImage = GetpercentImages(Igs, precent)
    filename_pre = name + "pre_85.tif"
    write_img(preImage, filename_pre, im_proj, im_geotrans, dirPath2)
    heatwaveJud(name, dirPath2, dirPath1, outputpath)

main()

def reclass(name):
    if (name="canal"):
        return 20
	elif (name="drain"):
        return 10
    elif (name="stream"):
        return 30
    elif (name="river"):
        return 40

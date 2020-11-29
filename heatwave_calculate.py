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
    number = 1
    im_bands = 1  # 均为单波段影像
    fullpath = []
    newpath = []
    newim_data = []
    newfilename = []
    ndv = -3.4028234663852886e+38
    if isinstance(filename, str):
        fullpath = dirpath + "\\" + filename
    else:
        for i in range(len(filename)):
            fullpath.append(dirpath + "\\" + filename[i])
    if len(im_data.shape) == 3:
        number, im_height, im_width = im_data.shape
        newpath = fullpath
        newim_data = im_data
        newfilename = filename
    elif len(im_data.shape) == 2:
        im_height, im_width = im_data.shape
        newpath.append(fullpath)
        newim_data.append(im_data)
        newfilename.append(filename)
    else:
        number, (im_height, im_width) = 1, im_data.shape
        print("Error:There is no way to get here!!!!")
    with tqdm(range(number)) as t:
        for i in t:
            # 创建文件
            driver = gdal.GetDriverByName("GTiff")
            dataset = driver.Create(newpath[i], im_width, im_height, im_bands, datatype)
            if (dataset != None):
                dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
                dataset.SetProjection(im_proj)  # 写入投影
                dataset.GetRasterBand(1).SetNoDataValue(ndv)  # 设置nodata值
            for band in range(im_bands):
                dataset.GetRasterBand(band + 1).WriteArray(newim_data[i])
            del dataset
            t.set_description(newfilename[i] + " has been successfully built")
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
    return np.array(Igs), im_geotrans, im_proj
def GetpercentImages(Igs,percent):
    """计算时间序列图像百分位数 """
    perImages = np.percentile(Igs, percent)
    return perImages

def getHeatWaveFreq(b):
    c=''.join(str(i) for i in b)
    d=np.array([len(i) for i in c.split('0')])
    return len(d[d>=3])

def heatwaveJud(name,percent,dirpath1,outputpath):
    """判断是否发生热浪"""
    #name节点名称
    #perpath阈值标准所在路径
    #dirpath1影像所在路径
    #outputpath影像输出路径
    Igs, im_geotrans, im_proj = openImages(dirpath1)
    durname = name + "HT_duration.tif"
    frename = name + "HT_frequency.tif"
    perImage = GetpercentImages(Igs, percent)
    Comparevalue=max(perImage,30)
    height, width = Igs[0].shape
    heatwaveimg = []
    with tqdm(enumerate(Igs)) as t:
        for i,Ig in t:
            newImage = np.empty((height, width))
            newImage[Ig>Comparevalue]=1
            heatwaveimg.append(newImage)
            t.set_description(f"Page{i+1} has finished")
    """计算热浪持续时间"""
    durimg = np.empty((height, width))
    heatwaveimg=np.transpose(heatwaveimg)
    for j in range(0, width):
        for i in range(0, height):
            durimg[i][j] += sum(heatwaveimg[j][i])
    print("Heat wave duration has been calculated successfully")
    """计算热浪发生频率"""
    freimg = np.empty((height,width))
    
    for i in range(width):
        for j in range(height):
            freimg[j][i]=getHeatWaveFreq(heatwaveimg[i][j]) 
    print("Heat wave frequency has been calculated successfully")
    write_img(durimg, durname, im_proj, im_geotrans, outputpath)
    write_img(freimg, frename, im_proj, im_geotrans, outputpath)
    # return heatwaveimg, durimg, freimg

def main():
    precent = 95
    dirinputPath=r"G:\extent\4_HTEMPX"
    diroutputPath=r"G:\high_temperture202011\result_data\heatwave"
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
            'Ankara': 'tur',
            'Piraeus': 'grc',
            'Melaka': 'mys',
            'Kuantan': 'mys',
            'Hambantota': 'lka',
            'Colombo': 'lka',
            'Minsk': 'blr',
            'Warsaw': 'pol',
            'Yawan': 'idn',
            'Valencia': 'esp',
            'Ekaterinburg': 'rus',
            'Novosibirsk': 'rus'
        }
    for region in regionnames:
        name = region
        dirPath1 =os.path.join(dirinputPath,name) 
        outputpath = diroutputPath
        heatwaveJud(name, precent, dirPath1, outputpath)

if __name__ == "__main__":
    main()




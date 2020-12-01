import os
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


def delete_filefolder(folderPath):
    if os.path.exists(folderPath):
        for fileList in os.walk(folderPath):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree(folderPath)
        print(folderPath+": delete ok")
    else:
        print(folderPath+": no folderPath")


def openImages(dirpath):
    """
    打开工作文件夹中的所有影像
    dirpath:数据读取文件夹
    return:Igs,im_geotrans.im_proj
    """
    Igs = []

    for dirPath, _, filenames in os.walk(dirpath):
        idate = 0
        with tqdm(filenames) as t:
            for filename in t:
                if filename[-5:] == ".tiff" or filename[-4:] == ".tif":
                    Image, im_geotrans, im_proj = openSingleImage(
                        dirPath+"\\"+filename)
                    Igs.append(Image)
                    idate = idate+1
                    t.set_description(filename+" is already open……")
            print("-"*120)

    return np.double(Igs), im_geotrans, im_proj


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder "+foldername+" is created")


def writeTiff(im_data, im_geotrans, im_proj, ndv, dirpath, filename, overwrite='n'):
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
            bool_a = not os.path.exists(newpath[i])
            bool_b = False
            if not bool_a:
                if overwrite == 'y':
                    bool_b = True
            bool_c = bool_a or bool_b
            if bool_c:
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


def GetpercentImages(Igs, percen):
    """
    计算时间序列图像百分位数
    Igs:3维数据
    percen:百分位数组
    """
    _, height, width = Igs.shape
    percentImages = np.empty((width, height, 3), dtype="double")
    with tqdm(range(0, width)) as t:
        for i in t:
            for j in range(0, height):
                percentImages[i][j] = np.percentile(
                    np.transpose(Igs)[i][j], percen)
            t.set_description("Proceeding col "+str(i))
        print("-"*120)
    return np.transpose(percentImages)


def clipTiff(path_inputraster, path_outputraster, path_clipshp, ndv):
    """
    裁剪影像
    path_inputraster:str
    path_outputraster:str
    path_clipshp:str
    """
    input_raster = gdal.Open(path_inputraster)

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


def clipTIFFs(pathdir_input, path_diroutput, path_clipshp, regionname, renameindex, ndv):
    """
    批量裁剪影像
    pathdir_input:str
    path_diroutput:str
    path_clipshp:str 裁剪shp文件
    regionname:str
    renameindex:int 从第几个字符开始列入新名字
    """

    mkdir(path_diroutput)
    for _, _, filenames in os.walk(pathdir_input):
        with tqdm(filenames) as t:
            for filename in t:
                if filename[-4:] == ".tif":
                    # 裁剪
                    path_inputraster = pathdir_input+"\\"+filename
                    path_outputraster = path_diroutput + \
                        "\\"+regionname+filename[renameindex:]
                    clipTiff(path_inputraster, path_outputraster,
                             path_clipshp, ndv)
                    t.set_description(regionname+" has been clipped")
            print("-"*120)


def getNuminStr(str):
    """
    获得字符串中的数字，返回列表
    """
    return([int(s) for s in re.findall(r'\d+', str)])  # 正则表达式寻找字符串中的数字


def SummaryPopofSex(dirpath, regionname, ndv):
    """
    计算性别总数加和
    dirpath:str
    regionname:str
    """
    ageClasses = []  # 字符串数组
    print("Calculating summary of pop of every age classes.")
    time_start = time.perf_counter()
    for _, _, filenames in os.walk(dirpath):
        for filename in filenames:
            age = getNuminStr(filename)[0]
            if not age in ageClasses:
                ageClasses.append(age)

    path_diroutput = dirpath+"_sum_pop"
    Igs = []
    filenames_sum = []
    im_geotrans = ""
    im_proj = ""
    for age in ageClasses:
        filename_f = regionname+"_f_"+str(age)+"_2015.tif"
        filename_m = regionname+"_m_"+str(age)+"_2015.tif"
        filename_sum = regionname+"_sum_"+str(age)+"_2015.tif"
        fIg, im_geotrans, im_proj = openSingleImage(dirpath+"\\"+filename_f)
        mIg = openSingleImage(dirpath+"\\"+filename_m)[0]
        Ig = ma.masked_where(fIg == ndv, fIg)+ma.masked_where(mIg == ndv, mIg)
        Ig = Ig.filled(ndv)
        Igs.append(Ig)
        filenames_sum.append(filename_sum)
    time_end = time.perf_counter()
    print("The calculation time is "+str(time_end-time_start)+"s.")
    writeTiff(np.array(Igs, dtype="double"), im_geotrans,
              im_proj, ndv, path_diroutput, filenames_sum)


def ComputeDeltaY(path_dirdeltaY, regionname, ndv, y0, beta_i=[0.0222, 0.032, 0.043, 0.061]):
    """
    计算deltaY

    """
    print("Calculating DeltaY...")
    filename_deltaY = [regionname+"_deltaY_000_980_2015.tif", regionname+"_deltaY_980_990_2015.tif",
                       regionname+"_deltaY_990_995_2015.tif", regionname+"_deltaY_995_100_2015.tif"]
    if not os.path.exists(os.path.join(path_dirdeltaY, filename_deltaY[0])):
        time_start = time.perf_counter()
        Igs, im_geotrans, im_proj = openImages(path_dirdeltaY)
        # max,mft,percen_980,percen_990,percen_995=Igs
        maxIg = Igs[0]
        height, width = maxIg.shape
        deltaY = np.empty((4, height, width), dtype="double")
        for page in range(4):
            for i in range(height):
                for j in range(width):
                    if maxIg[i][j] != ndv and Igs[page+1][i][j] != ndv:
                        deltaY[page][i][j] = y0*beta_i[page] * \
                            (maxIg[i][j]-Igs[page+1][i][j])
                    else:
                        deltaY[page][i][j] = ndv
        time_end = time.perf_counter()
        print("The calculation time is "+str(time_end-time_start)+"s.")

        writeTiff(deltaY, im_geotrans, im_proj, ndv,
                  path_dirdeltaY, filename_deltaY)
    else:
        print("Files are exist!")
        print("The calculation time is 0s.")


# def getSumPop(path, ndv=-99999):
#     """
#     计算栅格和,返回年龄段标签及其总人数
#     path:dir_path or file_path
#     """
#     Igs = []  # 各年龄段影像
#     sumPop = []  # 各年龄段人口数量和
#     ageClasses = []  # 按顺序的年龄标签
#     if(path[-4:] == ".tif"):  # 如果是文件
#         Igs.append(openSingleImage(path)[0])
#         ageClasses.append(getNuminStr(os.path.basename(path))[0])
#     else:
#         Igs = openImages(path)[0]
#         # 添加年龄标签
#         for dirPath, dirname, filenames in os.walk(path):
#             for filename in filenames:
#                 if filename[-5:] == ".tiff" or filename[-4:] == ".tif":
#                     age = getNuminStr(filename)[0]
#                     ageClasses.append(age)

#     with tqdm(range(len(Igs))) as t:
#         for i in t:
#             sumPop.append(
#                 sum(sum(ma.masked_where(Igs[i] == ndv, Igs[i]).filled(0))))
#             t.set_description(str(ageClasses[i])+"_pop_sum has been added")

#     return np.array([ageClasses, sumPop])


def getAgespop(arrays):
    s = np.zeros_like(arrays[0])
    for i in range(len(arrays)):
        s += arrays[i]
    return s


def computeDeltaYPeople(path_dirpart, path_dirtotal, path_diroutput, regionname, path_MFT, path_Max, Yj, ndv, beta=[0, 1.6, 4.6]):
    """
    计算DeltaYPeople
    """
    # 计算城市分3个年龄段的pop_j/pop_total
    print("Calculating DeltaYPeople.")
    time_start = time.perf_counter()
    Igs = openImages(path_dirpart)[0]
    ageClasses = []
    for _, _, filenames in os.walk(path_dirpart):
        for filename in filenames:
            if filename[-5:] == ".tiff" or filename[-4:] == ".tif":
                age = getNuminStr(filename)[0]
                ageClasses.append(age)

    table_pop = Igs[np.argsort(ageClasses)]  # 按照年龄顺序排序
    table_pop = ma.masked_where(table_pop == ndv, table_pop)

    pop_total = openSingleImage(path_dirtotal)[0]
    pop_total = ma.masked_where(pop_total == ndv, pop_total)
    ageClasses.sort()
    index_65 = ageClasses.index(65)
    index_80 = ageClasses.index(80)

    # pop_total_cal = getAgespop(table_pop).filled(ndv)  # 计算出来的数值下
    pop_0 = getAgespop(table_pop[:index_65])
    pop_65 = getAgespop(table_pop[index_65:index_80])
    pop_80 = getAgespop(table_pop[index_80:])
    pop_0[pop_0 < 1] = 0
    pop_65[pop_65 < 1] = 0
    pop_80[pop_80 < 1] = 0
    pop = [pop_0, pop_65, pop_80]
    rate_below65 = np.divide(pop[0], pop_total)
    rate_middle = np.divide(pop[1], pop_total)
    rate_above80 = np.divide(pop[2], pop_total)

    MFT, im_geotrans, im_proj = openSingleImage(path_MFT)
    MFT = ma.masked_where(MFT == ndv, MFT)
    Max = openSingleImage(path_Max)[0]
    Max = ma.masked_where(Max == ndv, Max)

    rate_pop = [rate_below65, rate_middle, rate_above80]

    deltaYpeople = []
    filename = [regionname+"_deltaYpeople_00_65_2015.tif",
                regionname+"_deltaYpeople_65_80_2015.tif", regionname+"_deltaYpeople_80_00_2015.tif"]
    for i in range(3):
        deltaYpeople.append((Yj[i]*(Max-MFT)*rate_pop[i]*beta[i]).filled(ndv))
        pop[i] = pop[i].filled(ndv)
        rate_pop[i] = rate_pop[i].filled(ndv)
    time_end = time.perf_counter()
    print("The calculation time is"+str(time_end-time_start)+" s.")
    writeTiff(np.array(deltaYpeople, dtype="double"),
              im_geotrans, im_proj, ndv, path_diroutput, filename)
    # writeTiff(np.array(Max-MFT,dtype="double"),im_geotrans,im_proj,ndv,r"E:\delatYpeople","t_t0.tif")
    # writeTiff(np.array(pop_total_cal,dtype="double"),im_geotrans,im_proj,ndv,r"E:\delatYpeople","pop_total_cal.tif")
    # writeTiff(np.array(rate_pop,dtype="double"),im_geotrans,im_proj,ndv,r"E:\delatYpeople",["rate0.tif","rate65.tif","rate80.tif"])
    # writeTiff(np.array(pop,dtype="double"),im_geotrans,im_proj,ndv,r"E:\delatYpeople",["pop0.tif","pop65.tif","pop80.tif"])


def get_paths_size(dirs):
    # 提取指定文件夹和大小的函数

    size = 0
    for root, _, files in os.walk(dirs):
        sums = sum([getsize(join(root, file)) for file in files]) / 2**30
        size += sums
    print(f"{dirs} -> 文件夹内文件占用空间：{int(size//1)}GB")
    return size


def splitImages(path_dir, ndv, min):
    """
    判断文件夹大于180Gb就分八块，保证每次运行内存大于30G小于50G
    """
    volume = get_paths_size(path_dir)
    regionname = path_dir.split("\\")[-1]  # 文件夹名称
    if(volume >= min):
        print("Split the "+regionname+".")
        path_diroutputs = []
        for i in trange(8):
            path_diroutput = path_dir+"_"+str(i)
            mkdir(path_diroutput)
            path_diroutputs.append(path_diroutput)
        for _, _, filenames in os.walk(path_dir):
            with tqdm(filenames) as t:
                for filename in t:
                    if filename[-4:] == ".tif":
                        # 裁剪
                        path_inputraster = path_dir+"\\"+filename
                        Ig, im_geotrans, im_proj = openSingleImage(
                            path_inputraster)
                        height, width = Ig.shape
                        height_split = [0, height//2, height-1]
                        width_split = [0, width//4,
                                       width//2, width//4*3, width-1]
                        index = 0
                        for i in range(2):
                            for j in range(4):
                                writeTiff(Ig[height_split[i]:height_split[i+1], width_split[j]:width_split[j+1]],
                                          im_geotrans, im_proj, ndv, path_diroutputs[index], filename[:-4]+"_"+str(index)+".tif")
                                index = index+1
                        #t.set_description(regionname+" has been splitted")
                print("-"*120)
        return True
    else:
        print(f"{regionname} don't need split.")
        return False


def clipRegions(path_dir, path_clipshp, ndv, min):
    """
    判断区域是否需要裁剪
    path_dir:array 文件夹
    min:int 超过多少裁剪
    """
    path_diroutput = path_dir+"_1"
    volume = get_paths_size(path_dir)
    regionname = path_dir.split("\\")[-1]
    if(volume >= min):
        clipTIFFs(path_dir, path_diroutput, path_clipshp, regionname, -12, ndv)
        delete_filefolder(path_dir)
        os.rename(path_diroutput, path_dir)
    else:
        print(regionname+" don't need clip.")


def main():
    inputpath = r"G:\extent\4_HTEMPX"  # 输入的城市地址
    filename_mode = "MFT"
    filename_max = "max"
    base_path = "E:\\High temperature heat wave vulnerability"
    percen = [98, 99, 99.5]
    filename_percen = ["percen_980", "percen_990", "percen_995"]
    ndv = -3.4028234663852886e+38

    countrynames = {
        'pak': [534.470781798936, 5023.08047186522, 14756.472169218, 725.381603018017],
        'irn': [204.741873390693, 2765.60588865875, 10800.9744295223, 461.048229330302],
        'egy': [312.899968106733, 5345.88078688905, 16475.3728213329, 589.099092812004],
        'ind': [577.114942473571, 5452.01189872163, 13256.2064061997, 677.162973972817],
        'mdv': [137.912707197264, 1376.63778155838, 10011.9158828108, 297.979760232981],
        'uzb': [204.741873390693, 2765.60588865875, 10800.9744295223, 631.849838680504],
        'blr': [448.22201080611, 3956.88848285732, 12872.6380094772, 1265.63790156098],
        'grc': [201.381899760866, 2073.19771582528, 9615.97427186187, 1092.28536836944],
        'idn': [341.896269294193, 4531.08970494719, 15043.2405633622, 649.34204343592],
        'mys': [237.553827941087, 3470.05961405609, 11139.8031163271, 499.765698895476],
        'pol': [320.243214988411, 2736.24283308342, 10536.2967358783, 1008.07640135626],
        'rus': [551.444717204407, 3948.27978930515, 12431.2361440204, 1265.55290707226],
        'esp': [154.830468751955, 1694.00546794559, 9133.02069973709, 871.577845169866],
        'lka': [233.595129825896, 2966.0764383601, 12032.061788856, 599.344617094331],
        'tur': [186.304361470242, 2899.79038870804, 10805.9612928024, 543.896991626259]
    }

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
                    # 'Ekaterinburg': 'rus',
                    # 'Novosibirsk': 'rus'
    }
    with tqdm(regionnames) as t:
        print("#"*120)
        for region in t:
            regionname = region  # 地区名
            regionfilename = regionname+".tif"  # 地区文件名
            countryname = regionnames[region]  # 国家名
            countryfilename = regionnames[region]+".tif"  # 国家文件名

            # 计算DeltaY
            print("Proceeding region:"+regionname)
            path_dirDeltaY = base_path+"\\deltaY\\"+regionname
            path_folder = inputpath+"\\"+regionname
            regionname_split = {}
            # 判断是否需要裁剪
            path_clipshp = base_path+"\\extent\\"+regionname+".shp"
            clipRegions(path_folder, path_clipshp, ndv, 20)
            # 判断是否需要切片
            bsplit = splitImages(path_folder, ndv, 180)
            if(bsplit):
                for i in range(8):
                    regionname_split[regionname+"_"+str(i+1)] = countryname
            else:
                regionname_split[regionname] = countryname
            for ifn, regionname in enumerate(regionname_split):
                regionfilename = regionname+".tif"  # 地区文件名
                # 局部变量regionname\regionfilename代表分区以后的/未分区
                # 打开影像
                path_folder = path_folder+"_" + \
                    str(ifn) if bsplit else path_folder
                Igs, im_geotrans, im_proj = openImages(path_folder)
                # 计算
                if not os.path.exists(os.path.join(path_dirDeltaY, regionname + "_"+filename_mode + "_2015.tif")):
                    time_begin = time.perf_counter()
                    print("Calculating MFT_"+regionname)
                    modeImage = stats.mode(Igs)[0][0]  # 众数MFT
                    time_mode = time.perf_counter()
                    print("time calculate mode is " +
                          str(time_mode-time_begin)+"s.")
                    writeTiff(modeImage, im_geotrans, im_proj, ndv,
                              path_dirDeltaY, regionname + "_"+filename_mode + "_2015.tif")
                if not os.path.exists(os.path.join(path_dirDeltaY, regionname + "_"+filename_max + "_2015.tif")):
                    print("Calculating Max_"+regionname)
                    maxImage = Igs.max(axis=0)  # 最大值Max
                    time_max = time.perf_counter()
                    print("time calculate max is " +
                          str(time_max-time_mode)+"s.")
                    writeTiff(maxImage, im_geotrans, im_proj, ndv,
                              path_dirDeltaY, regionname + "_"+filename_max + "_2015.tif")
                    print("-"*120)
                if not os.path.exists(os.path.join(path_dirDeltaY, regionname + "_"+filename_percen[0] + "_2015.tif")):
                    percenImages = GetpercentImages(Igs, percen)  # 计算百分位数
                    writeTiff(percenImages, im_geotrans, im_proj, ndv, path_dirDeltaY, [
                        regionname + "_"+filename + "_2015.tif" for filename in filename_percen])

                ComputeDeltaY(path_dirDeltaY, regionname, ndv,
                              countrynames[countryname][3])

                # 将人口网格裁剪到各研究区
                path_dirinput = base_path+"\\country_pop\\"+countryname
                path_diroutput = base_path+"\\region_pop\\"+regionname
                path_clipshp = base_path+"\\extent\\"+regionname+".shp"
                clipTIFFs(path_dirinput, path_diroutput,
                          path_clipshp, regionname, 3, ndv)
                path_totalPop = path_diroutput+"_pop_2015.tif"
                clipTiff(path_dirinput+"_ppp_2015.tif",
                         path_totalPop, path_clipshp, ndv)

                # 按照年龄将不同性别人口栅格加和
                SummaryPopofSex(path_diroutput, regionname, ndv)
                # 计算DeltaYPeople

                path_dirageClasses = path_diroutput+"_sum_pop"
                path_dirdeltaYpeople = base_path+"\\deltaYpeople\\"+regionname
                path_MFT = path_dirDeltaY+"\\"+region + "_"+filename_mode + "_2015.tif"
                path_Max = path_dirDeltaY+"\\"+region + "_"+filename_max + "_2015.tif"
                computeDeltaYPeople(path_dirageClasses,
                                    path_totalPop,
                                    path_dirdeltaYpeople,
                                    regionname,
                                    path_MFT,
                                    path_Max,
                                    countrynames[countryname][:3],
                                    ndv)

            t.set_description(regionname + " has calculated!")
            print("#"*120)


    # clipTIFFs(r"E:\High temperature heat wave vulnerability\Pakistan\pak_ppp_2015.tif",
    # r"E:\High temperature heat wave vulnerability\Pakistan\pak_karachi_2015.tif",
    # r"E:\High temperature heat wave vulnerability\pop\Karachi\Karachi.shp",
    # ndv)
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错
# arcpy.env.workspace=r"H:"
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

regionnames = [
    # 'Abbas',
    # 'Karachi',
    # 'Alexandria',
    # 'Gawdar',
    # 'Kolkata',
    # 'Maldives',
    # 'Mumbai',
    # 'Tashkent',
    # 'Teran',
    'Ankara',
    'Piraeus',
    'Melaka',
    'Kuantan',
    'Hambantota',
    'Colombo',
    'Minsk',
    'Warsaw',
    'Yawan',
    'Ekaterinburg',
    'Novosibirsk',
    'Valencia',
]
year = {
    'max': 2015,
    'HT_frequency': 2015,
    'HT_duration': 2015,
    'pop': 2015,
    'deltaY': 2015,
    'deltaYpeople': 2015,
    'NDVI': 2015,
    'virrs': 2015,
    'GDP': 2015,
    'Euc': 2020,
    'IMS': 2015,
    'Danger': 2015,
    'Expo': 2015,
    'Vulner': 2015,
    'DPE': 2015,
    'Final': 2015
}


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder "+foldername+" is created")


def calculate2(path_dirinputdata, path_diroutdata, index1, index2):
    for region in regionnames:
        for singleIndex2 in index2:
            path_dirindex2 = os.path.join(path_diroutdata, singleIndex2)
            mkdir(path_dirindex2)
            path_index1list = []
            for index1s in index2[singleIndex2]:
                for singleIndex1 in index1[index1s]:
                    path_index1list.append(os.path.join(path_dirinputdata, index1s, "{}_{}_{}.tif".format(
                        region, singleIndex1, str(year[index1s]))))
            out_raster = 0
            for singleIndex1 in path_index1list:
                # print(singleIndex1)
                out_raster += Raster(singleIndex1)
            path_outdata = os.path.join(
                path_dirindex2, "{}_{}_{}.tif".format(region, singleIndex2, str(year[singleIndex2])))
            if not os.path.exists(path_outdata):
                out_raster.save(path_outdata)
    print("done")


def calculate3(path_dirinputdata, path_diroutdata, index1, index2):
    for region in regionnames:
        for singleIndex2 in index2:
            path_dirindex2 = os.path.join(path_diroutdata, singleIndex2)
            mkdir(path_dirindex2)
            path_index1list = []
            for index1s in index2[singleIndex2]:
                for singleIndex1 in index1[index1s]:
                    path_index1list.append(os.path.join(path_dirinputdata, index1s, "{}_{}_{}.tif".format(
                        region, singleIndex1, str(year[index1s]))))

            out_raster = Raster(path_index1list[0])
            for singleIndex1 in path_index1list[1:]:
                # print(singleIndex1)
                out_raster *= Raster(singleIndex1)
            path_outdata = os.path.join(
                path_dirindex2, "{}_{}_{}.tif".format(region, singleIndex2, str(year[singleIndex2])))
            if not os.path.exists(path_outdata):
                out_raster.save(path_outdata)
    print("done")


def main():
    index1 = {
        'max': ['max'],
        'HT_frequency': ['HT_frequency'],
        'HT_duration': ['HT_duration'],
        'pop': ['pop'],
        'deltaY': ['deltaY_000_980', 'deltaY_980_990', 'deltaY_990_995', 'deltaY_995_100'],
        'deltaYpeople': ['deltaYpeople_00_65', 'deltaYpeople_65_80', 'deltaYpeople_80_00'],
        'NDVI': ['NDVI'],
        'virrs': ['virrs'],
        'GDP': ['GDP'],
        'Euc': ['hospital_Euc', 'road_Euc', 'water_Euc'],
        'IMS': ['IMS']
    }
    index2 = {
        'Danger': ["max", "HT_frequency", "HT_duration"],
        'Expo': ["pop"],
        'Vulner': ["deltaY", "deltaYpeople"],
        'DPE': ["NDVI", "virrs", "GDP", "Euc", "IMS"]
    }
    index2file = {
        'Danger': ['Danger'],
        'Expo': ['Expo'],
        'Vulner': ['Vulner'],
        'DPE': ['DPE']
    }
    index3 = {
        'Final': ['Danger', 'Expo', 'Vulner', 'DPE']
    }
    path_dirinputdata = r"G:\high_temperture202011\result_normalized"
    path_diroutdata = r"G:\high_temperture202011\result_data"
    # calculate2(path_dirinputdata, path_diroutdata, index1, index2)  # 计算二级指标
    calculate3(path_dirinputdata,path_diroutdata,index2file,index3)


def main_test():
    path_dirinputdata = r"G:\high_temperture202011\result_normalized"
    path_diroutdata = r"H:\high_temperture202011\result_data"
    for region in regionnames:
        for singleIndex2 in index2:
            path_dirindex2 = os.path.join(path_diroutdata, singleIndex2)
            print("@"*120)
            print(path_dirindex2)
            path_index1list = []
            for index1s in index2[singleIndex2]:
                for singleIndex1 in index1[index1s]:
                    path_index1list.append(os.path.join(path_dirinputdata, index1s, "{}_{}_{}.tif".format(
                        region, singleIndex1, str(year[index1s]))))
            print(len(path_index1list))
            for singleIndex1 in path_index1list:
                print("index1"+singleIndex1)


def main_testRaster():
    raster = 0
    raster += Raster(r"H:\high_temperture202011\result_normalized\max\Karachi_max_2015.tif")
    raster.save("H:\\karachi_max.tif")


if __name__ == "__main__":
    main()

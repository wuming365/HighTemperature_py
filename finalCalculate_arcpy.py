# -*- coding: utf-8 -*-
import arcgisscripting
from CONSTANT import *
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错
# arcpy.env.workspace=r"H:"

year = {
    'max': YEAR,
    'HT_frequency': YEAR,
    'HT_duration': YEAR,
    'pop': YEAR,
    'deltaY': YEAR,
    'deltaYpeople': YEAR,
    'NDVI': YEAR,
    'Nightlight': YEAR,
    'GDP': YEAR,
    'Euc': 2020,
    'IMS': YEAR,
    'Danger': YEAR,
    'Expo': YEAR,
    'Vulner': YEAR,
    'DPE': YEAR,
    'Final': YEAR
}

def calculate2(path_dirinputdata, path_diroutdata, index1, index2):
    for region in REGIONNAMES:
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
    for region in REGIONNAMES:
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

    path_dirinputdata = r"../{}/result_normalized".format(YEAR)
    path_diroutdata = r"../{}/result_data".format(YEAR)
    # calculate2(path_dirinputdata, path_diroutdata, index1, index2)  # 计算二级指标
    calculate3(path_dirinputdata,path_diroutdata,INDEX2FILE,INDEX3)


def main_test():
    path_dirinputdata = r"G:\high_temperture202011\result_normalized"
    path_diroutdata = r"H:\high_temperture202011\result_data"
    for region in REGIONNAMES:
        for singleIndex2 in INDEX2:
            path_dirindex2 = os.path.join(path_diroutdata, singleIndex2)
            print("@"*120)
            print(path_dirindex2)
            path_index1list = []
            for index1s in INDEX2[singleIndex2]:
                for singleIndex1 in INDEX1[index1s]:
                    path_index1list.append(os.path.join(path_dirinputdata, index1s, "{}_{}_{}.tif".format(
                        region, singleIndex1, str(year[index1s]))))
            print(len(path_index1list))
            for singleIndex1 in path_index1list:
                print("index1"+singleIndex1)


def main_testRaster():
    raster = 0
    raster += Raster(r"H:\high_temperture202011\result_normalized\max\Karachi_max_YEAR.tif")
    raster.save("H:\\karachi_max.tif")


if __name__ == "__main__":
    main()

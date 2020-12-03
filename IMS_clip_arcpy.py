# -*- coding:utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")

IMSClip = {
    # 'Abbas': 'ImperviousMap_E50N30.tif',
    # 'karachi': 'ImperviousMap_E60N30.tif',
    # 'Alexandria': 'Processed',
    # 'Gawdar': 'Processed',
    # 'Kolkata': 'ImperviousMap_E80N30.tif',
    # 'Maldives': 'ImperviousMap_E70N10.tif',
    # 'Mumbai': 'Processed',
    # 'Tashkent': 'Processed',
    # 'Teran': 'ImperviousMap_E50N40.tif',
    # 'Ankara': 'Processed',
    # 'Piraeus': 'ImperviousMap_E20N40.tif',
    # 'Melaka': 'ImperviousMap_E100N10.tif',
    # 'Kuantan': 'ImperviousMap_E100N10.tif',
    # 'Hambantota': 'ImperviousMap_E80N10.tif',
    # 'Colombo': 'Processed',
    # 'Minsk': 'ImperviousMap_E20N60.tif',
    # 'Warsaw': 'ImperviousMap_E20N60.tif',
    # 'Yawan': 'ImperviousMap_E100N0.tif',
    # 'Ekaterinburg': 'Processed',
    'Novosibirsk': 'ImperviousMap_E80N60.tif',
    # 'Valencia': 'ImperviousMap_W10N40.tif',
}
path_dirori = r"G:\high_temperture202011\GISp"
path_dirext = r"G:\high_temperture202011\extent"
path_dirclipout = r"G:\high_temperture202011\turn"
path_dirresout = r"G:\high_temperture202011\turn"
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错
for regionname in IMSClip:
    path_outclip = os.path.join(path_dirclipout, regionname+"_clip.tif")
    if(IMSClip[regionname] != "Processed"):
        path_clipshp = os.path.join(path_dirext, regionname+".shp")
        path_inputraster = os.path.join(path_dirori, IMSClip[regionname])
        extent = arcpy.Describe(path_clipshp).extent  # 得到8个 后面又4个NaN
        extent = " ".join(str(extent).split(" ")[:4])  # 这里只需要四个数字组成的字符串
        arcpy.Clip_management(in_raster=path_inputraster, rectangle=str(extent), out_raster=path_outclip,
                            in_template_dataset=path_clipshp, nodata_value="255", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
        path_resout = os.path.join(path_dirresout, "IMS_"+regionname+".tif")
        arcpy.Resample_management(in_raster=path_outclip, out_raster=path_resout,
                              cell_size="0.00083333333 0.00083333333", resampling_type="NEAREST")
    # if(IMSClip[regionname] != "Processed"):
        region = "IMS_"+regionname+".tif"
        arcpy.gp.RasterCalculator_sa('Con("%s" == 0,0,Con("%s" == 1,0,Con("%s" == 2,1)))' % (
            region, region, region), path_dirresout+"\\"+regionname+"_IMS_2015"+".tif")  # 双引号在单引号中不需要转义字符，栅格计算的文件必须在arcmap中缓存
    # else: #rename

    print("Processing "+regionname)
"""
裁剪重采样
for region in regionnames:
    regionname = region
    countryname = regionnames[region]
    path_outclip = os.path.join(path_dirclipout, regionname+"_virrs_clip.tif")
    path_clipshp = os.path.join(path_dirext, regionname+".shp")
    path_inputraster = os.path.join(path_dirori, countryname+"_viirs_100m_2015.tif")
    extent = arcpy.Describe(path_clipshp).extent  # 得到8个 后面又4个NaN
    extent = " ".join(str(extent).split(" ")[:4])  # 这里只需要四个数字组成的字符串
    arcpy.Clip_management(in_raster=path_inputraster, rectangle=str(extent), out_raster=path_outclip, in_template_dataset=path_clipshp,nodata_value="256", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    path_resout = os.path.join(path_dirresout, regionname+"_virrs_2015.tif")
    arcpy.Resample_management(in_raster=path_outclip, out_raster=path_resout, cell_size="0.00083333333 0.00083333333", resampling_type="NEAREST")
"""

# -*- coding:utf-8 -*-
import arcgisscripting
from arcpy.sa import *
import arcpy
import os
import shutil
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0" #防止并行报错
input_path_hospital = r"H:\high_temperture202011\zanshi"
input_path_road=r"H:\high_temperture202011\road"
input_path_waterway=r"H:\high_temperture202011\waterway"
output_path = r"H:\high_temperture202011\result_data\RoadHospiWater"
path_turn = r"H:\high_temperture202011\turn"
path_clip=r"H:\high_temperture202011\extent"
regionnames = {
                'Abbas': 'irn',
                'Karachi': 'pak',
                'Alexandria': 'egy',
                'Gawdar': 'pak',
                'Kolkata': 'ind',
                'Maldives': 'mdv',
                'Mumbai': 'ind',
                'Tashkent': 'uzb',
                'Teran': 'irn',
                'Ankara': 'tur',
                'Piraeus': 'grc',
                'Melaka': 'mys',
                'Kuantan': 'mys',
                'Hambantota': 'lka',
                'Colombo': 'lka',
                'Minsk': 'blr',
                'Warsaw': 'pol',
                'Yawan': 'idn'
                'Valencia': 'esp',
                'Ekaterinburg': 'rus',
                'Novosibirsk': 'rus'
                }
for region in regionnames:
    regionname = region
    countryname = regionnames[region]
    country_poi="{0}\\{1}_pois_osm.shp".format(input_path_hospital,countryname) #python2
    region_turn_hospital="hospital_{}_{}".format(countryname,regionname) # layer
    distance_hospital="{0}\\hospital_EucDistance_2020_{1}.tif".format(path_turn,regionname)
    clipshp="{0}\\{1}.shp".format(path_clip,regionname)
    country_road="{0}\\{1}_roads_osm.shp".format(input_path_road,countryname) #python2
    distance_road="{0}\\road_EucDistance_2020_{1}.tif".format(path_turn,regionname)
    country_waterway="{0}\\{1}_waterway_osm.shp".format(input_path_waterway,countryname) #python2
    buffer_region="{0}\\{1}_waterway_buf.shp".format(path_turn,regionname) #python2
    country_water="{0}\\{1}_water_osm.shp".format(r"H:\high_temperture202011\water",countryname) #python2
    output_water="{0}\\{1}_{2}_water_osm.shp".format(path_turn,countryname,regionname)
    distance_water="{0}\\water_EucDistance_2020_{1}.tif".format(path_turn,regionname)
    #整个国家太大，将外接矩形扩大一些
    extent = arcpy.Describe(clipshp).extent  # 得到8个 后面有4个NaN
    a=str(extent).split(" ")[:4]
    a=map(float,a)
    a[0]-=0.3
    a[1]-=0.3
    a[2]+=0.3
    a[3]+=0.3
    a=map(str,a)
    extent = " ".join(a)  # 这里只需要四个数字组成的字符串
    arcpy.env.extent=extent # 不要设置extent，否则会按照小区域进行计算
    # 创建图层文件并选择
    # arcpy.MakeFeatureLayer_management(in_features=country_poi, out_layer=region_turn_hospital, where_clause='"fclass" = \'hospital\'', workspace="", field_info="FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;osm_id osm_id VISIBLE NONE;code code VISIBLE NONE;fclass fclass VISIBLE NONE;name name VISIBLE NONE")
    # 从poi中选择hospital
    arcpy.env.mask=clipshp # mask的不是shp的最小外接矩形，需要再裁剪一下
    # arcpy.gp.EucDistance_sa(region_turn_hospital, distance_hospital, "", "0.00083333333", "")
    # arcpy.gp.EucDistance_sa(country_road, distance_road, "", "0.00083333333", "")
    # waterway生成缓冲区并与water合并后计算欧氏距离
    if not os.path.exists(buffer_region): #arcpy不会自动覆盖，避免调试失败删除文件才可继续，在所有输出上判断是否存在
        arcpy.Buffer_analysis(in_features=country_waterway, out_feature_class=buffer_region, buffer_distance_or_field="width", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field="", method="PLANAR")
    if not os.path.exists(output_water):
        arcpy.Merge_management(inputs="{};{}".format(buffer_region,country_water), output=output_water, field_mappings='osm_id "osm_id" true true false 10 Text 0 0 ,First,#,mdv_waterway_osm_Buffer,osm_id,-1,-1,{1},osm_id,-1,-1;code "code" true true false 2 Short 0 0 ,First,#,{0},code,-1,-1,{1},code,-1,-1;fclass "fclass" true true false 28 Text 0 0 ,First,#,mdv_waterway_osm_Buffer,fclass,-1,-1,{1},fclass,-1,-1;width "width" true true false 4 Long 0 0 ,First,#,{0},width,-1,-1;name "name" true true false 100 Text 0 0 ,First,#,{0},name,-1,-1,{1},name,-1,-1;BUFF_DIST "BUFF_DIST" true true false 8 Double 0 0 ,First,#,{0},BUFF_DIST,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0 ,First,#,{0},ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#,{0},Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0 ,First,#,{0},Shape_Area,-1,-1'.format(buffer_region,country_water))
    if not os.path.exists(distance_water):
        arcpy.gp.EucDistance_sa(output_water, distance_water, "", "0.00083333333", "")
    # 生成hospital要素类
    # arcpy.CopyFeatures_management(in_features=country_poi, out_feature_class=region_turn_hospital, config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")
    # 裁剪输出到指定文件夹 用gdal裁剪，和之前数据格网大小一致，gdal与arcpy裁剪会差1行1列
    # arcpy.Clip_analysis(in_features=region_turn_hospital, clip_features=clipshp, out_feature_class=region_hospital, cluster_tolerance="")
    print("hospital processed "+regionname)
    

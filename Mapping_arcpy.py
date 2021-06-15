
############需要放到ArcMap里跑，否则会出问题
from CONSTANT import *
from arcpy.sa import *
import arcpy



import os
import arcpy.mapping as mp
arcpy.CheckOutExtension("Spatial")
arcpy.env.parallelProcessingFactor = "0"  # 防止并行报错

YEAR = 2010
INDEXCNAMES={
		"Danger":"危险性",
		"Expo":"暴露度",
		"Vulner":"脆弱性",
		"DPE":"孕灾环境",
		"Final":"最终结果",
        # "NDVI":"NDVI",
        # "hospital_Euc":"hospital_Euc",
        # "road_Euc":"road_Euc",
        # "Nightlight":"Nightlight",
        # "water_Euc":"water_Euc",
        # "IMS":"IMS",
		}
REGIONCNAMES={
		"Abbas":["阿巴斯","Iran","伊朗"],
		"Alexandria":["亚特兰大港","Egypt","埃及"],
		"Ankara":["安卡拉","Turkey","土耳其"],
		"Colombo":["科伦坡","Sri Lanka","斯里兰卡"],
		# "Djibouti":["吉布提","Djibouti","吉布提"],
		"Ekaterinburg":["叶卡捷琳堡","Russia","俄罗斯"],
		"Gawdar":["瓜达尔港","Pakistan","巴基斯坦"],
		"Hambantota":["汉班托塔港","Sri Lanka","斯里兰卡"],
		"Karachi":["卡拉奇","Pakistan","巴基斯坦"],
		"Kolkata":["加尔各答","india","印度"],
		"Kuantan":["关丹","Malaysia","马来西亚"],
		"Maldives":["马尔代夫","Maldives","马尔代夫"],
		"Melaka":["马六甲","Malaysia","马来西亚"],
		"Minsk":["明斯克","Belarus","白俄罗斯"],
		"Mumbai":["孟买","India","印度"],
		"Novosibirsk":["新西伯利亚","Russia","俄罗斯"],
		# "Nursultan":["努尔苏丹（原阿斯塔纳）","Kazakhstan","哈萨克斯坦"],
		"Piraeus":["比雷艾夫斯港","Greece","希腊"],
		"Tashkent":["塔什干","Uzbekistan","乌兹别克斯坦"],
		"Teran":["德黑兰","Iran","伊朗"],
		# "Valencia":["瓦伦西亚","Spain","西班牙"],
		"Warsaw":["华沙","Poland","波兰"],
		"Yawan":["雅万高铁","Indonesia","印度尼西亚"],
		}

basepath=r"./{}/result_normalized".format(YEAR)
path=os.getcwd()
# print("0 "+os.getcwd())
mxd=mp.MapDocument(r"CURRENT")
# print("1 "+os.getcwd())###########################
df=mp.ListDataFrames(mxd,"Layers")[0]
# print("2 "+os.getcwd())#####################
Info=dict()
baselyr=mp.ListLayers(mxd)[0]
# print("3 "+os.getcwd())####################

for index in INDEXCNAMES:
    pathIndex=os.path.join(basepath,index)
    for region in REGIONCNAMES:
        name="{}_{}_{}".format(region,index,YEAR)
        png_name = r"./{}/MAP/{}/{}.png".format(YEAR,index,name)
        print(name)
        pathtif=r"{}/{}.tif".format(pathIndex,name)
        arcpy.CalculateStatistics_management(pathtif) #Arcmap内Python包含AddLayer，独立脚本不含 
        max = float(arcpy.GetRasterProperties_management(pathtif, "MAXIMUM").getOutput(0))
        min = float(arcpy.GetRasterProperties_management(pathtif, "MINIMUM").getOutput(0))
        mean = float(arcpy.GetRasterProperties_management(pathtif, "MEAN").getOutput(0))
        std = float(arcpy.GetRasterProperties_management(pathtif, "STD").getOutput(0))
        if index in Info:
            Info[index][region]=[min,max,mean,std]
        else:
            Info[index]={region:[min,max,mean,std]}
            
        layer=mp.ListLayers(mxd)[0]
        if layer.name==baselyr.name:
            baselyr.visible=True
        else:
            baselyr.visible=False
            mp.UpdateLayer(df,layer,baselyr,True)
            if layer.symbologyType == "RASTER_CLASSIFIED":
                layer.symbology.reclassify()
            # print(layer.symbology.classBreakValues)
        classValues=layer.symbology.classBreakValues
        #获得重分类后的数量信息
        str=""
        for i in range(len(classValues)):
            if i<len(classValues)-1:
                str+="{} {} {}".format(classValues[i],classValues[i+1],i+1)
            if i<len(classValues)-2:
                str+=";"
        reclassName = "{}/Reclass/reclass_{}.tif".format(basepath,name)
        if not os.path.exists(reclassName):
            arcpy.gp.Reclassify_sa("{}.tif".format(name), "VALUE", str,"{}/Reclass/reclass_{}.tif".format(basepath,name) , "DATA")
    
        re_layer=mp.Layer(reclassName)
        Count={}
        count_sort=[]
        for row in arcpy.da.SearchCursor(re_layer,["Value","Count"]):
            Count[row[0]]=row[1]
        for i in sorted(list(Count)):
            count_sort.append(Count[i])
        if len(count_sort)==5:
            count_sort.append(float(sum(count_sort[-3:]))/sum(count_sort))
            count_sort.append(float(sum(count_sort[-2:]))/sum(count_sort))
        Info[index][region].append(count_sort)
        if re_layer.name==mp.ListLayers(mxd)[0].name:
            re_layer=mp.ListLayers(mxd)[0]
            mp.RemoveLayer(df,re_layer)
        
        # if not os.path.exists(png_name):
        #     for elm in mp.ListLayoutElements(mxd,"TEXT_ELEMENT"):
        #         if elm.name=="title":
        #             elm.text="高温热浪\n{}".format(INDEXCNAMES[index])
        #         elif elm.name=="region":
        #             elm.text="中文：{}\n英文：{}\n年份：{}\n平均值：{:.4f}\n标准差：{:.4f}".format(REGIONCNAMES[region][0],region,YEAR,Info[index][region][2],Info[index][region][3])
        #         elif elm.name=="country":
        #             elm.text="中文：{}\n英文：{}".format(REGIONCNAMES[region][2],REGIONCNAMES[region][1])
        #     df.extent=layer.getExtent()
        #     arcpy.RefreshActiveView()
        #     arcpy.RefreshTOC()
        #     mp.ExportToPNG(mxd,png_name)
        if layer.name!=baselyr.name:
            mp.RemoveLayer(df,layer)
            
with open(r"./{0}/Map/Information_{0}.txt".format(YEAR),"w") as f:
    f.write("Region,RCName,Index,ICName,Year,Min,Max,Mean,Std,Count1,Count2,Count2,Count4,Count5,中-高,中高-高\n")
    for index in Info:
        for region in Info[index]:
            Min,Max,Mean,Std,count_sort=Info[index][region]
            Count1,Count2,Count3,Count4,Count5,PercenSum3,PercenSum2,_=count_sort
            f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{:.3f},{:.3f}\n".format(region,REGIONCNAMES[region][0],index,INDEXCNAMES[index],YEAR,Min,Max,Mean,Std,Count1,Count2,Count3,Count4,Count5,PercenSum3*100,PercenSum2*100))


    
    

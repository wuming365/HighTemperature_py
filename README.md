# highemperature_py
1.	文件命名:Region_Index_Year.tif

2.	turn:文件中转文件夹

3.	extent:表示范围的shp文件所在文件夹

4.	GISp:Global Impervious SurfaceMap

5.	waterway process step：
1.width calculation
def Reclass(WellYield):
    	if (WellYield == "river"):
        	return 20
    	elif (WellYield =="stream"):
        	return 15
    	elif (WellYield == "canal"):
        	return 10
    	elif (WellYield == "drain"):
        	return 5
2.buffer by field "width"
3.Merge with water.shp

6.	所有的计算范围(extent)为shp外界矩形四边向外扩展0.3，设置掩膜(mask)为shp文件

7.	最后裁剪均使用gdal生成，arcpy与gdal会相差一行一列，最终结果如下
NumofRowCol = {
    	'Abbas': '3465, 2325',
    	'Karachi': '1108, 1085',
    	'Alexandria': '2260, 1905',
    	'Gawdar': '4480, 980',
    	'Kolkata': '2339, 1940',
    	'Maldives': '1224, 2592',
    	'Mumbai': '1386, 3014',
    	'Tashkent': '3117, 2512',
    	'Teran': '2783, 1431',
}
像元大小:"0.00083333333 0.00083333333"

8.	已有的地区和国家对应关系
regionnames = {
                    'Abbas': 'irn',
                    'Karachi': 'pak',
                    'Alexandria': 'egy',
                    'Gawdar': 'pak',
                    'Kolkata': 'ind',
                    'Maldives': 'mdv',
                    'Mumbai': 'ind',
                    'Tashkent': 'uzb',
                    'Teran': 'irn'
                    }

9.	国家的生产数据 from GBD Results
    countrynames = {
        	'pak': [534.470781798936, 5023.08047186522, 14756.472169218, 725.381603018017],
        	'irn': [204.741873390693, 2765.60588865875, 10800.9744295223, 461.048229330302],
        	'egy': [312.899968106733, 5345.88078688905, 16475.3728213329, 589.099092812004],
        	'ind': [577.114942473571, 5452.01189872163, 13256.2064061997, 677.162973972817],
        	'mdv': [137.912707197264, 1376.63778155838, 10011.9158828108, 297.979760232981],
        	'uzb': [204.741873390693, 2765.60588865875, 10800.9744295223, 631.849838680504]
    	}
分别为0-65，65-80，80+，all ages 的死亡率(per 100k)

10.	指标体系
 
评价体系 + Final
表示分数越高灾害越强
+：和上级指标正相关
用1表示
-：和上级指标负相关
用0表示	危险性 + Danger	强度 最大值 + max
		频率 频数 + HT_frequency
		持续时间 热浪 + HT_duration
	暴露度 + Expo	人口数量 + pop
	脆弱性 + Vulner	不同强度热浪对人群的致死率 多个 + deltaY
		热浪对不同年龄段人群的致死率 多个 + deltaYpeople
	孕灾环境 – DPE
(Disaster-pregnant environment)	植被覆盖度 + NDVI
		用电量 + virrs
		GDP + GDP
		距医院距离 - Euc
		距水体距离 - Euc
		距道路距离 - Euc
		不透水面覆盖度 - IMS


# highemperature_py


 - 文件树
	```
	│  clip_gdal.py # 用gdal裁剪
	│  finalCalculate_arcpy.py # 计算二级和三级指标
	│  heatwave_calculate.py # 计算热浪持续时间和频率
	│  IMS_clip_arcpy.py # 计算IMS不透水面
	│  Normalization_arcpy.py # 指标值归一化
	│  README.md 
	│  Resample_arcpy.py # 用arcpy重采样至"0.00083333333 0.00083333333"
	│  shp_clip_arcpy.py # 计算water、hospital、road的Eucdistance
	│  test.py # 测试代码文件
	│  vulnerability_gdal.py #计算脆弱性&裁剪区域
 - 文件命名:Region_Index_Year.tif
 - extent:表示范围的shp文件所在文件夹
 - GISp:Global Impervious SurfaceMap
 - waterway process step：
	 1. width calculation
	    ```python
	    // A code block
	    def Reclass(WellField):
			if (WellYield == "river"):
				return 20
			elif (WellYield =="stream"):
				return 15
			elif (WellYield == "canal"):
				return 10
			elif (WellYield == "drain"):
				return 5
	 2. buffer by field "width"
	 3. Merge with water.shp

 - 所有的计算范围(`extent`)为shp外界矩形四边向外扩展`0.1`，设置掩膜(mask)为shp文件
 - 最后裁剪均使用gdal生成，arcpy与gdal会相差一行一列，最终结果如下
	```python
	    NumofRowCol = {
	        	'Abbas': '3465, 2325',
	        	'Alexandria': '2260, 1905',
	        	'Ankara': '1560,1201',
	        	'Colombo': '877,1286',
	        	'Djibouti':@@@@@@@@@@@未做2015
	        	'Ekaterinburg': '3036,1362',
	        	'Gawdar': '4480, 980',
				'Hambantota': '1317,1784',
				'Karachi': '1108, 1085',
	        	'Kolkata': '2339, 1940',
	        	'Kuantan': '940,1974',
	        	'Maldives': '1224, 2592',
	        	'Melaka': '1569,1340',
	        	'Minsk': '3012,1378',
	        	'Mumbai': '1386, 3014',
	        	'Novosibirsk': '3318,2448'
	        	'NurSultan': '3278,1522',
	        	'Piraeus': '1426,2844',
	        	'Tashkent': '3117, 2512',
	        	'Teran': '2783, 1431',
	        	'Valencia': '1805,1554',
				'Warsaw': '2001,1164',
				'Yawan': '3063,2939',
				    }
		像元大小:"0.00083333333 0.00083333333"

 - 已有的地区和国家对应关系
	```python
		REGIONNAMES = {
		                    'Abbas': 'irn',
		                    'Alexandria': 'egy',
		                    'Ankara': 'tur',
		                    'Colombo': 'lka',
		                    'Djibouti':'dji',
		                    'Ekaterinburg': 'rus', #rus2 for osm
		                    'Gawdar': 'pak',
		                    'Hambantota': 'lka',
		                    'Karachi': 'pak',
		                    'Kolkata': 'ind',
		                    'Kuantan': 'mys',
		                    'Maldives': 'mdv',
		                    'Melaka': 'mys',
		                    'Minsk': 'blr',
		                    'Mumbai': 'ind',
		                    'Novosibirsk': 'rus', #rus1 for osm
		                    'NurSultan':'kaz',
		                    'Piraeus': 'grc',
		                    'Tashkent': 'uzb',
		                    'Teran': 'irn',
		                   'Valencia': 'esp',
		                    'Warsaw': 'pol',
		                    'Yawan': 'idn',
		                    }
 - 国家的生产数据 from GBD Results  [http://ghdx.healthdata.org/gbd-results-tool](http://ghdx.healthdata.org/gbd-results-tool)
    ```python
    countrynames_2015 = {
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
		'tur': [186.304361470242, 2899.79038870804, 10805.9612928024, 543.896991626259],
		'kaz': [400.49966051634, 4719.60965479109, 15810.27142003640, 805.41677930925],
			}
	countrynames_2010 = {
		'pak': [593.03758396383, 5270.39440908467, 15700.97511101140, 789.82033349754],
		'irn': [223.11233145403, 2886.76862490416, 11105.33442579990, 450.20536035465],
		'egy': [329.93642470087, 5265.12822538898, 16197.24690780350, 589.10509534206],
		'ind': [434.87325374981, 4536.83162372381, 12001.44832528940, 701.71917941031],
		'mdv': [606.61843103002, 2728.07042747218, 10570.54143887150, 316.09770422351],
		'uzb': [365.61776768595, 7307.34991470124, 26640.92322840300, 658.25282316134],
		'blr': [568.23048055218, 4648.86192489513, 12809.07951444310, 1401.33758391848],
		'grc': [255.34644789769, 2212.70084112597, 10046.40854247460, 961.68300106982],
		'idn': [362.11130517634, 4646.37067950888, 15180.01259467360, 651.89177476373],
		'mys': [222.47139454995, 3853.89974968537, 12404.54653971730, 467.28186248326],
		'pol': [341.38243307728, 3128.59114440609, 10593.69283453420, 967.98045142470],
		'rus': [657.62395788745, 4703.17596888471, 12732.57625544340, 1394.81914984204],
		'esp': [159.56485562996, 1880.76346929809, 9184.42687944668, 807.78155673355],
		'lka': [290.54150366162, 3352.45621736712, 13207.30681559210, 633.61440209213],
		'tur': [186.73745198034, 3112.50824650203, 10972.06345995990, 522.06476587897],
		'kaz': [504.61816457559, 5179.86245015006, 15412.02015507310, 945.04924663248],
			}
		分别为0-65，65-80，80+，all ages 的死亡率(per 100k)

 - 指标体系
<table align="center">
	<tr>
	    <th>Index3</th>
	    <th>Index2</th>
	    <th>Index1</th>  
	</tr >
	<tr align="center">
	    <td rowspan="13">
	    <p> <br>评价体系 + Final</br>
	    <br>表示分数越高灾害越强</br></p> 
	    <p><br><font color="red">"+"：和上级指标正相关</font></br>
	    <br>用1表示</br></p>
	    <p><font color="red">"-"：和上级指标负相关</font>
	    <br>用0表示</br></p> </td>
	    <td rowspan="3">
	    <font>危险性 + Danger</font>
	    </td>
	    <td>强度 <font color="red">温度最大值</font> + max</td>
	</tr>
	<tr align="center">
	    <td>频率  <font color="red">热浪频数</font> + HT_frequency</td>
	</tr>
	<tr align="center">
	    <td>持续时间  <font color="red">热浪持续时间</font> + HT_duration</td>
	</tr>
	<tr align="center">
	    <td rowspan="1">暴露度 + Expo</td>
	    <td>人口数量 + pop</td>
	</tr>
	<tr align="center">
		<td rowspan="2">
		脆弱性 + Vulner
		<br><font size=2>强度:,MFT, 98.5, 99.0, 99.5</font></br>
		<br><font size=2>年龄段:,0-65, 65-80, 80+</font></br></td>
	    <td>不同强度热浪对人群致死率  <font color="red">4个</font>  + deltaY_</td>
	</tr>
	<tr align="center">
	    <td>热浪对不同年龄段人群的致死率  <font color="red">3个年龄段</font> + deltaYpeople_</td>
	</tr>
	<tr align="center">
	    <td rowspan="7">
	    孕灾环境 - DPE
	    <br>Disaster-pregnant environment</br></td>
	    <td>植被覆盖度 + NDVI</td>
	</tr>
	<tr align="center">
	    <td>用电量 + Nightlight</td>
	</tr>
	<tr align="center">
	    <td>GDP + GDP
</td>
	</tr>
	<tr align="center">
	    <td>至医院距离 - hospital_Euc</td>
	</tr>
	<tr align="center">
	    <td >至道路距离 - road_Euc</td>
	</tr>
	<tr align="center">
	    <td >至水体距离 - water_Euc</td>
	</tr>
	<tr align="center">
	    <td >不透水面覆盖度 - IMS</td>
	</tr>
</table>

 - 部分数据来源
	 - [GDP_2015](%5Bhttp://ghdx.healthdata.org/gbd-results-tool%5D%28http://ghdx.healthdata.org/gbd-results-tool%29)
	 - NDVI ：from Google Earth Engine 2015.7->2015.8
	 - [IMS data paper](https://essd.copernicus.org/articles/12/1625/2020/essd-12-1625-2020-discussion.html)	----这是一个可爱的分隔符----[IMS data Download](https://zenodo.org/record/3505079#.XmGz6NIzbIU)  
	 - hospital、water、road ：from OpenStreetMap 2020-11
	 - [virrs 夜光遥感数据](https://www.worldpop.org/geodata/listing?id=39)、[dmsp夜光遥感数据](https://www.worldpop.org/geodata/listing?id=40)
	 - [pop Age and sex structures](https://www.worldpop.org/geodata/listing?id=30)

 - Index代码
```python
		INDEXNAMES = {
				'max': 1,
				'HT_frequency': 1,
				'HT_duration': 1,
				'pop': 1,
				'deltaY': 1,
				'delatYpeople': 1,
				'NDVI': 1,
				'Nightlight': 1,
				'GDP': 1,
				'Euc': 0,
				'IMS': 0,
				'Danger': 1,
				'Expo': 1,
				'Vulner': 1,
				'DPE': 0,
				'Final': 1
				}
		year = {
				'max': 2015,
				'HT_frequency': 2015,
				'HT_duration': 2015,
				'pop': 2015,
				'deltaY': 2015,
				'deltaYpeople': 2015,
				'NDVI': 2015,
				'nightlight': 2015,
				'GDP': 2015,
				'Euc': 2020,
				'IMS': 2015,
				'Danger': 2015,
				'Expo': 2015,
				'Vulner': 2015,
				'DPE': 2015,
				'Final': 2015
				}
		INDEX1 = {
				'max': ['max'],
				'HT_frequency': ['HT_frequency'],
				'HT_duration': ['HT_duration'],
				'pop': ['pop'],
				'deltaY': ['deltaY_000_980', 'deltaY_980_990', 'deltaY_990_995', 'deltaY_995_100'],
				'deltaYpeople': ['deltaYpeople_00_65', 'deltaYpeople_65_80', 'deltaYpeople_80_00'],
				'NDVI': ['NDVI'],
				'Nightlight': ['Nightlight'],
				'GDP': ['GDP'],
				'Euc': ['hospital_Euc', 'road_Euc', 'water_Euc'],
				'IMS': ['IMS']
				}
		INDEX2 = {
				'Danger': ["max", "HT_frequency", "HT_duration"],
				'Expo': ["pop"],
				'Vulner': ["deltaY", "deltaYpeople"],
				'DPE': ["NDVI", "Nightlight", "GDP", "Euc", "IMS"]
				}
		INDEX2FILE = {
				'Danger': ['Danger'],
				'Expo': ['Expo'],
				'Vulner': ['Vulner'],
				'DPE': ['DPE']
				}
		INDEX3 = {
				'Final': ['Danger', 'Expo', 'Vulner', 'DPE']
				}
		REGIONCNAMES={
		"Abbas":["阿巴斯","Iran","伊朗"],
		"Alexandria":["亚特兰大港","Egypt","埃及"],
		"Ankara":["安卡拉","Turkey","土耳其"],
		"Colombo":["科伦坡","Sri Lanka","斯里兰卡"],
		"Djibouti":["吉布提","Djibouti","吉布提"],
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
		"Nursultan":["努尔苏丹（原阿斯塔纳）","Kazakhstan","哈萨克斯坦"],
		"Piraeus":["比雷艾夫斯港","Greece","希腊"],
		"Tashkent":["塔什干","Uzbekistan","乌兹别克斯坦"],
		"Teran":["德黑兰","Iran","伊朗"],
		"Valencia":["瓦伦西亚","Spain","西班牙"],
		"Warsaw":["华沙","Poland","波兰"],
		"Yawan":["雅万高铁","Indonesia","印度尼西亚"],
		}
		INDEXCNAMES={
		"Danger":"危险性",
		"Expo":"暴露度",
		"Vulner":"脆弱性",
		"DPE":"孕灾环境",
		"Final":"最终结果",
		}

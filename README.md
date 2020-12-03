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
	        	'Karachi': '1108, 1085',
	        	'Alexandria': '2260, 1905',
	        	'Gawdar': '4480, 980',
	        	'Kolkata': '2339, 1940',
	        	'Maldives': '1224, 2592',
	        	'Mumbai': '1386, 3014',
	        	'Tashkent': '3117, 2512',
	        	'Teran': '2783, 1431',
	        	'Ankara': '1560,1201',
				'Piraeus': '1426,2844',
				'Melaka': '1569,1340',
				'Kuantan': '940,1974',
				'Hambantota': '1317,1784',
				'Colombo': '877,1286',
				'Minsk': '3012,1378',
				'Warsaw': '2001,1164',
				'Yawan': '3063,2939',
				'Valencia': '1805,1554',
				'Ekaterinburg': '3036,1362',
				'Novosibirsk': '3318,2448'
				    }
		像元大小:"0.00083333333 0.00083333333"

 - 已有的地区和国家对应关系
	```python
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
		                    'Yawan': 'idn',
		                    'Valencia': 'esp',
		                    'Ekaterinburg': 'rus', #rus2 for osm
		                    'Novosibirsk': 'rus' #rus1 for osm
		                    }
 - 国家的生产数据 from GBD Results  [http://ghdx.healthdata.org/gbd-results-tool](http://ghdx.healthdata.org/gbd-results-tool)
    ```python
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
	    <td rowspan="1">暴露度</td>
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
	    <td>用电量 + virrs</td>
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
	 - [virrs 夜光遥感数据](https://www.worldpop.org/geodata/listing?id=39)
	 - [pop Age and sex structures](https://www.worldpop.org/geodata/listing?id=30)

 - Index代码
```python
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


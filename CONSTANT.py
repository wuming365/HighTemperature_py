# -*- coding: utf-8 -*-
import os
import numpy as np
##########

REGIONCNAMES = {
    "Abbas": ["阿巴斯", "Iran", "伊朗"],
    "Alexandria": ["亚特兰大港", "Egypt", "埃及"],
    "Ankara": ["安卡拉", "Turkey", "土耳其"],
    "Colombo": ["科伦坡", "Sri Lanka", "斯里兰卡"],
    # "Djibouti":["吉布提","Djibouti","吉布提"],
    "Ekaterinburg": ["叶卡捷琳堡", "Russia", "俄罗斯"],
    "Gawdar": ["瓜达尔港", "Pakistan", "巴基斯坦"],
    "Hambantota": ["汉班托塔港", "Sri Lanka", "斯里兰卡"],
    "Karachi": ["卡拉奇", "Pakistan", "巴基斯坦"],
    "Kolkata": ["加尔各答", "india", "印度"],
    "Kuantan": ["关丹", "Malaysia", "马来西亚"],
    "Maldives": ["马尔代夫", "Maldives", "马尔代夫"],
    "Melaka": ["马六甲", "Malaysia", "马来西亚"],
    "Minsk": ["明斯克", "Belarus", "白俄罗斯"],
    "Mumbai": ["孟买", "India", "印度"],
    "Novosibirsk": ["新西伯利亚", "Russia", "俄罗斯"],
    # "Nursultan":["努尔苏丹（原阿斯塔纳）","Kazakhstan","哈萨克斯坦"],
    "Piraeus": ["比雷艾夫斯港", "Greece", "希腊"],
    "Tashkent": ["塔什干", "Uzbekistan", "乌兹别克斯坦"],
    "Teran": ["德黑兰", "Iran", "伊朗"],
    # "Valencia":["瓦伦西亚","Spain","西班牙"],
    "Warsaw": ["华沙", "Poland", "波兰"],
    "Yawan": ["雅万高铁", "Indonesia", "印度尼西亚"],
}

INDEXCNAMES = {
    "Danger": "危险性",
    "Expo": "暴露度",
    "Vulner": "脆弱性",
    "DPE": "孕灾环境",
    "Final": "最终结果",
}

CALCU = ["positive", "negative"]
###########
###########通用
REGIONNAMES = {
    'Abbas': 'irn',
    'Alexandria': 'egy',
    'Ankara': 'tur',
    'Colombo': 'lka',
    # 'Djibouti': 'dji',
    'Ekaterinburg': 'rus',  #rus2 for osm
    'Gawdar': 'pak',
    'Hambantota': 'lka',
    'Karachi': 'pak',
    'Kolkata': 'ind',
    'Kuantan': 'mys',
    'Maldives': 'mdv',
    'Melaka': 'mys',
    'Minsk': 'blr',
    'Mumbai': 'ind',
    'Novosibirsk': 'rus',  #rus1 for osm
    # 'Nursultan': 'kaz',
    'Piraeus': 'grc',
    'Tashkent': 'uzb',
    'Teran': 'irn',
    # 'Valencia': 'esp',
    'Warsaw': 'pol',
    'Yawan': 'idn',
}
YEAR = 2010
NDV = -3.4028234663852886e+38

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

INDEX1 = {
    'max': ['max'],
    'HT_frequency': ['HT_frequency'],
    'HT_duration': ['HT_duration'],
    'pop': ['pop'],
    'deltaY':
    ['deltaY_000_980', 'deltaY_980_990', 'deltaY_990_995', 'deltaY_995_100'],
    'deltaYpeople':
    ['deltaYpeople_00_65', 'deltaYpeople_65_80', 'deltaYpeople_80_00'],
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

INDEX3 = {'Final': ['Danger', 'Expo', 'Vulner', 'DPE']}


def mkdir(path):
    """
    创建文件夹
    """
    folder = os.path.exists(path)
    foldername = path.split("\\")[-1]

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("The folder " + foldername + " is created")


#####################
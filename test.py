# -*-coding:utf-8 -*-
import os
import os.path
import re
from collections import namedtuple

import gdal
import numpy as np
import numpy.ma as ma
import ogr
import shapefile
import xlrd
from scipy import stats
from tqdm import tqdm
from tqdm.std import trange

import time

# data=numpy.random.randint(5,size=(2,3,4))
# print(data)
# print(numpy.transpose(data))
# print(numpy.transpose(numpy.transpose(data)))
# ndv=3
# mode,count=stats.mode(data)
# a="Karachi20150102.tif"
# print(a[18:])
# print(data.max(axis=0))
# dataa=np.array([5,4,3,2,1])
# suma=0
# print([suma+a for a in dataa])
# data2=numpy.array([1,9,8,6,7])


# data2[data2<2]=10
# print(numpy.append(data,dataa,axis=0))
# for i in trange(1,101,ascii=True,desc="ninhao"):
#     time.sleep(0.05)
# a=ma.masked_where(data==1,data)+1
# print(a.filled(fill_value=1000))
# p=numpy.percentile(data[0],numpy.array([50,75,80]))
# print(p)
# a=numpy.zeros((10000,10000))
# b=numpy.zeros((10000,10000))
# c=numpy.zeros((10000,10000))

# b=np.random.randint(2,size=1000000)
# time1_start=time.perf_counter()
# c=''.join(str(i) for i in b)
# d=np.array([len(i) for i in c.split('0')])
# print(len(d[d>=3]))
# print(time1_end-time1_start)
# time2_start=time.perf_counter()
# c=np.split(b,np.where(np.diff(b)<0)[0]+1)
# d=np.array([np.sum(i) for i in c])
# print(len(d[d>=3]))


# a=np.array([[[1,2],[2,3]],[[1,2],[2,3]],[[1,3],[1,3]],[[2,4],[4,2]]])
# a=ma.masked_where(a==1,a)
a="ma.tif"
b="ma"
print(a.split(".")[0])
print(b.split(".")[0])
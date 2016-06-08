# -*- coding: utf-8 -*-
"""
Created on Fri May 20 21:06:05 2016

@author: lenovo
"""
import pandas as pd
import os

from collections import Counter

fileOrder = 'season_1/training_data/order_data/order_data_2016-01-01'
fileDir = 'season_1/training_data/order_data'
clusterMapFile = 'season_1/training_data/cluster_map/cluster_map'


   
orderNames = ['order_id','driver_id','passenger_id','start_district_hash','dest_district_hash','Price','Time']

region = set()

for filename in os.listdir(fileDir):
    
    if filename[0] != '.':
        
        fileOrderPath = fileDir + '/' + filename
        
        dfTemp = pd.read_csv(fileOrderPath,sep='\t',names=orderNames,index_col='order_id')
        
        SS = set(list(dfTemp['start_district_hash']))   
        
        DS = set(list(dfTemp['dest_district_hash']))
        
        region = region|SS|DS
        

##### 将 district_hash 映射为数字
        
cluster_map_df = pd.read_table(clusterMapFile, names=['district_hash', 'district_id'])
cluster_map_set = set(list(cluster_map_df['district_hash']))
cluster_map_dict = cluster_map_df.set_index('district_hash').to_dict()

region_temp = region - cluster_map_set

region_dict = dict(zip(region_temp,range(len(region_temp)+1,len(region)+len(region_temp)+1)))  

region_dict.update(cluster_map_dict)

#dfTemp = pd.read_csv(fileOrder,sep='\t',names=orderNames,index_col='order_id')



timeList = list(dfTemp['Time'])
timeListint = []
for etim in timeList:
    l1 = etim.split(' ')
    l2 = l1[1].split(':')
    l3 = map(int,l2)
    timeListint.append(l3[0]*6+l3[1]/10)
    
#SS = set(list(dfTemp['start_district_hash']))
#    
#DS = set(list(dfTemp['dest_district_hash']))
#
#SS_dict = dict(zip(SS,range(len(SS))))
#
#DS_dict = dict(zip(DS,range(len(DS))))
#
#region = SS|DS
#

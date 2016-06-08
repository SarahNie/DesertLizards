# -*- coding: utf-8 -*-
"""
Created on Tue May 31 21:48:07 2016

@author: xin
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import time

from matplotlib.ticker import MultipleLocator, FuncFormatter

dates = ['2016-01-01','2016-01-02','2016-01-03','2016-01-04','2016-01-05',
         '2016-01-06','2016-01-07','2016-01-08','2016-01-09','2016-01-10',
         '2016-01-11','2016-01-12','2016-01-13','2016-01-14','2016-01-15',
         '2016-01-16','2016-01-17','2016-01-18','2016-01-19','2016-01-20',
         '2016-01-21']

## Load train data
for day in range(1,len(dates)):
    date = dates[day]
    print date
    df_map = pd.read_csv("training_data/cluster_map/cluster_map.csv",names=['region_hash','region_index'])
    df_order = pd.read_table("training_data/order_data/order_data_" + date, 
                             names=['order_id', 'driver_id', 'passenger_id', 'start_district_hash', 'dest_district_hash', 'Price', 'Time'])
    
    #df_order = df_order.dropna()
    Num_regions = df_map.index.size
                             
    # Generate time slots for a day
    Num_timeslots = 144
    timeslots = []
    for i in range(0,Num_timeslots+1):
        hour = i/6
        if hour<10:
            hour = '0'+str(hour)
        else:
            hour = str(hour)    
        minute = str(i%6) + '0'
        second = '00'
        date_time = date + ' ' + hour + ':' + minute + ':' + second
        timeslots.append(date_time)
        
    ## Get the number of drivers and passengers in each region and each time slot
    NumArrivals_ST = np.zeros((Num_regions, Num_timeslots), dtype='float32')
    NumCars_ST = np.zeros((Num_regions, Num_timeslots), dtype='float32')
    
    start = time.clock()
    for i in range(0,Num_regions):
        print i
        for j in range(0,Num_timeslots):
            NumArrivals_ST[i,j] = df_order.passenger_id[df_order.start_district_hash==df_map['region_hash'][i]][timeslots[j] < df_order.Time][df_order.Time < timeslots[j+1]].value_counts().size
            NumCars_ST[i,j] = df_order.driver_id[df_order.start_district_hash==df_map['region_hash'][i]][timeslots[j] < df_order.Time][df_order.Time < timeslots[j+1]].value_counts().size
    end = time.clock()
    print(end-start)
    df_NumArrivals_ST = pd.DataFrame(NumArrivals_ST)
    df_NumCars_ST = pd.DataFrame(NumCars_ST)
    df_NumArrivals_ST.to_csv('df_NumArrivals_ST'+'_'+date)
    df_NumCars_ST.to_csv('df_NumCars_ST'+'_'+date)

"""
## PLot demand v.s. supply for a specific day (date)
for Region_idx in range(0,Num_regions):
    fig = plt.figure()
    ax = plt.gca()
    ax.xaxis.set_major_locator( MultipleLocator(12) )
    ax.set_xticklabels(['0', '0', '2', '4', '6',  '8',  '10',  '12', '14', '16', '18', '20', '22', '24'])
    df_NumCars_ST.loc[Region_idx].plot(label="Cars",color="blue")    
    df_NumArrivals_ST.loc[Region_idx].plot(label="Arrivals",color="red")    
    plt.xlabel(date+' '+'Regions:'+str(Region_idx))
    plt.ylabel('Arrivals and Cars')
    plt.legend(loc = 'best')
    plt.title('Total Demand v.s. Supply for a specific region')
"""
    
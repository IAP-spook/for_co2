#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
#import sqlite3
#import os
#import time
#import matplotlib.pyplot as plt


name_list = ['Time', 'Record_num', 'Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',\
                 'Diag_R3', 't_hmp', 'rh_hmp', 'e_hmp']
n_lst_num = ['Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',\
		'Diag_R3','t_hmp', 'rh_hmp', 'e_hmp']
dtype_dict = {'Time': pd.datetime, 'Record_num': np.int32, 'Ux': np.float64, 'Uy': np.float64,
                  'Uz': np.float64, 'Ts': np.float64, 'CO2': np.float64,
                  'H2O': np.float64, 'Press': np.float64, 'Diag_R3': np.int,
                  't_hmp': np.float64, 'rh_hmp': np.float64, 'e_hmp': np.float64}

data_path = '/Users/WangYinan/Desktop/2016/data1'
db_dir = '/Users/WangYinan/Desktop/2016/data1'
db_name = 'co2.db'
db_tb_name = 'data_raw'
test_file_dir = '/Users/WangYinan/Desktop/2016/data1/CR1000_ts_data_130927.dat'
H_dir='/Users/WangYinan/for_co2/hour_mean.csv'

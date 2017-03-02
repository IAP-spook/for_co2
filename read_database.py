# -*- coding:utf-8 -*-

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def filter_strike(data_to_flt, window_width, factor):
    data_to_flt = data_to_flt.astype(np.float64)
    data_to_flt[abs(data_to_flt) > 900] = np.nan
    data_to_flt[data_to_flt < 200] = np.nan
    data_roll = pd.rolling_mean(data_to_flt, window=window_width, min_periods=1)
    data_residual = data_to_flt-data_roll
    # data_flt_index=abs(data_residual-data_residual.mean())<3.25*data_residual.std()
    data_flt_index = abs(data_residual) < factor*data_residual.std()
    data_to_flt[data_flt_index == False] = np.nan
    return data_to_flt


def cvt_2_ppm(data_pd):
    data_co2 = data_pd.CO2.astype(np.float64)
    data_co2_ppm = ((data_pd.t_hmp.astype(np.float64)+273.15)*8.314/(44*data_pd.Press.astype(np.float64)))*data_co2
    return data_co2_ppm


plt.style.use('ggplot')
data_base_dir = '/Users/WangYinan/Desktop/data'
data_base_name = 'DH_co2.db'
name_list = ['Time', 'Record_num', 'Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',
             'Diag_R3', 't_hmp', 'rh_hmp', 'e_hmp']

conn = sqlite3.connect(os.path.join(data_base_dir, data_base_name))
cur = conn.cursor()
# cur.execute("select * from data_raw")
# data_raw = cur.fetchall()
data_raw = pd.read_sql("select * from '13/12';", conn, index_col='Time')

cur.close()
conn.close()
data_raw.index = pd.to_datetime(data_raw.index)
data_raw.CO2 = filter_strike(data_raw.CO2, 3000, 3.25)
data_raw.CO2 = cvt_2_ppm(data_raw)
data_hour = data_raw.CO2.resample('H', how='mean')
plt.plot(data_hour.index, data_hour)
plt.show()

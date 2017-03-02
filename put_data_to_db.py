# -*- coding:utf-8 -*—

import pandas as pd
import numpy as np
import sqlite3
# import matplotlib.pyplot as plt
import platform
import os
import time
from multiprocessing.dummy import Pool as TreadPool


def read_co2file(file_path_para):
    """
    :param file_path_para: 文件路径
    :return: 返回DataFrame数据结构,index为时间,columns为name_list

    """
    name_list = ['Time', 'Record_num', 'Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',
                 'Diag_R3', 't_hmp', 'rh_hmp', 'e_hmp']
    data_raw = pd.read_csv(file_path_para, sep=',', header=3, names=name_list, low_memory=False)
    data_raw = data_raw.drop_duplicates(['Time'])
    data_raw.index = pd.to_datetime(data_raw.Time)
    del data_raw['Time']
    print 'Data Periods: %s \n' % (data_raw.index[-1]-data_raw.index[0])
    temp_period = pd.date_range(data_raw.index[0], data_raw.index[-1], freq='100ms')
    print 'Data Integrity: %s%% \n' % ((float(len(data_raw.index))/len(temp_period))*100.0)
    print file_path_para+'\n'
    return data_raw


def filter_strike(data_to_flt, window_width, factor):
    data_to_flt = data_to_flt.astype(np.float64)
    data_to_flt[abs(data_to_flt) > 900] = np.nan
    data_to_flt[data_to_flt < 100] = np.nan
    data_roll = pd.rolling_mean(data_to_flt, window=window_width, min_periods=1)
    data_residual = data_to_flt-data_roll
    # data_flt_index=abs(data_residual-data_residual.mean())<3.25*data_residual.std()
    data_flt_index = abs(data_residual) < factor*data_residual.std()
    data_to_flt[data_flt_index == False] = np.nan
    return data_to_flt


def get_filenames(file_path_para):
    fn_lst = []
    for dirpaths, dir_names, filenames in os.walk(file_path_para):
        for file_name in filenames:
            fn_lst.append(os.path.join(dirpaths, file_name))
    # Mac system
    if platform.system() == 'Darwin':
        del fn_lst[0]
    return fn_lst


def cvt_2_ppm(data_pd):
    data_co2 = data_pd.CO2.astype(np.float64)
    data_co2_ppm = ((data_pd.t_hmp.astype(np.float64)+273.15)*8.314/(44*data_pd.Press.astype(np.float64)))*data_co2
    return data_co2_ppm


def put_data_to_db(db_dir_path, data, db_name, db_table_name):
    conn = sqlite3.connect(os.path.join(db_dir_path, db_name))
    cur = conn.cursor()
    data.to_sql(db_table_name, conn, if_exists='append', flavor='sqlite')
    cur.close()
    conn.close()

if __name__ == '__main__':

    file_path = '/Users/WangYinan/Desktop/DH'
    db_dir_path = '/Users/WangYinan/Desktop/data'
    db_name = 'DH_co2.db'
    for dirpaths, dirnames, fns in os.walk(file_path):
        if len(fns) > 3:

            file_names = [os.path.join(dirpaths, fn) for fn in fns]
            print file_names
            if file_names[0] == os.path.join(dirpaths, '.DS_Store'):
                del file_names[0]
            start = time.time()
            pool = TreadPool(4)
            temp = pool.map(read_co2file, file_names)
            pool.close()
            pool.join()
            db_table_name = dirpaths[-5:]

            for element in temp:
                put_data_to_db(db_dir_path, element, db_name, db_table_name)
                print db_name

            end = time.time()
            print end-start






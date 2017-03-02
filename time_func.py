# -*- coding:utf-8 -*-
from consts_lst import *


def time_func(func):
    def wrapper_time_func(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        print end - start
        return func
    return wrapper_time_func


@time_func
def read_co2file(file_path_para):
    """
    :param file_path_para: 文件路径
    :return: 返回DataFrame数据结构,index为时间,columns为name_list

    """
    '''name_list = ['Time', 'Record_num', 'Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',
                 'Diag_R3', 't_hmp', 'rh_hmp', 'e_hmp']'''
    data_raw = pd.read_csv(file_path_para, sep=',', header=3, names=name_list)
    data_raw = data_raw.drop_duplicates(['Time'])
    data_raw.index = pd.to_datetime(data_raw.Time)
    del data_raw['Time']
    print 'Data Periods: %s \n' % (data_raw.index[-1]-data_raw.index[0])
    temp_period = pd.date_range(data_raw.index[0], data_raw.index[-1], freq='100ms')
    print 'Data Integrity: %s%% \n' % ((float(len(data_raw.index))/len(temp_period))*100.0)
    print file_path_para+'\n'
    return data_raw


time_func(read_co2file(test_read_file_dir))

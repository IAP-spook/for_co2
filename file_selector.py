# -*- coding:utf-8 -*-

import os
import re
import shutil

input_dir = '/Users/WangYinan/Desktop/DH_2013_2015_ts'
out_dir = '/Users/WangYinan/Desktop/DH'
fn_list = os.listdir(input_dir)
del fn_list[0]
months = ['01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12']
years = ['13', '14', '15']
for year in years:
    year_dir = os.path.join(out_dir, year)
    os.mkdir(year_dir)
    for month in months:
        os.mkdir(os.path.join(year_dir, month))
        pattern = re.compile('CR1000_ts_data_'+year+month+'\d\d.dat')
        for fn in fn_list:
            if pattern.match(fn):
                shutil.copy(os.path.join(input_dir, fn), os.path.join(year_dir, month))


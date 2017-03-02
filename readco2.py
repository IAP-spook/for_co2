#!/usr/bin/env python
# -*- coding:utf-8 -*-

from consts_lst import *
import matplotlib.pyplot as plt


def read_co2(file_dir):
	data_raw=pd.read_csv(file_dir,sep=',',header=3,names=name_list,dtype=dtype_dict,low_memory=False)
	data_raw.drop_duplicates(['Time'],keep='first',inplace=True)
	data_raw.index=pd.to_datetime(data_raw['Time'])
	return data_raw


if __name__=='__main__':

	plt.style.use('ggplot')
	data=read_co2(test_file_dir)
	plt.plot(data.CO2)
	plt.show()

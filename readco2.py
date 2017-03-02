#!/usr/bin/env python
# -*- coding:utf-8 -*-

from consts_lst import *
import matplotlib.pyplot as plt


def read_co2(file_dir):
	data_raw=pd.read_csv(file_dir,sep=',',header=3,names=name_list,\
	dtype=dtype_dict,low_memory=False)
	data_raw.drop_duplicates(['Time'],keep='first',inplace=True)
	data_raw.index=pd.to_datetime(data_raw['Time'])
	return data_raw


def destrike_data(input,*args):
	if args: 
		roll_result = input.rolling(window=args[0],\
		min_periods=1).mean()
	else:
		roll_result = input.rolling(window=3000,\
		min_periods=1).mean()
	residual = input-roll_result
	up_li=residual.mean()+3*residual.std()
	down_li=residual.mean()-3*residual.std()
	input[residual>up_li]=np.nan
	input[residual<down_li]=np.nan
	return input

if __name__=='__main__':

	plt.style.use('ggplot')
	data=read_co2(test_file_dir)
	#plt.plot(destrike_data(data.CO2,6000))
	plt.plot(destrike_data(data.CO2))
#	plt.plot(data.CO2)
#	plt.boxplot(destrike_data(data.CO2))
	
	plt.show()

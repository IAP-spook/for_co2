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


def despike_3sig(data_to_flt, *args):
	#默认参数必须指向不可变对象!we need to make a copy of data_to_flt.
	#第一次是copy,loc also work,cause bug,not to use pd.loc
	if len(args)==0:
		window_width, sigma_pm = 3000, 3
	elif len(args)==1:
		window_width, sigma_pm = args[0], 3
	#	print type(window_width)
	elif len(args)==2:
		window_width, sigma_pm = args
	else:
		raise Exception("Only need 2 arguments to be input!")
	#if not will casuse a warning from pandas chain index
	data_to_flt = data_to_flt.copy()
	roll_result = data_to_flt.rolling(window=window_width,\
		min_periods=1).mean()
	residual = data_to_flt-roll_result
	strike_index = abs(residual) >= sigma_pm*abs(residual.std())
	data_to_flt[strike_index] = np.nan
	#print input_data.dtype
	return data_to_flt

def despike_edire(data_in, n_sig=None):
	if n_sig:
		n_s = n_sig
	else:
		n_s = 4
	data_in = data_in.copy()
	data_diff=data_in.diff()
	if data_diff.std() > 0:
		data_in[data_diff>n_s*data_diff.std()]=np.nan
	if data_diff.std() < 0:
		data_in[data_diff<n_s*data_diff.std()]=np.nan	
	return data_in

def pre_process(data_input):
	#Diag_Rs=1,Licor instrument doesn't work
	bad_num = (data_input.Diag_R3 == 1).count()
	if(len(data_input)-bad_num)/len(data_input)>0.01:
		raise Exception("This file has too many bad points!")
	if (data_input.Diag_R3==1).any():
		data_input[data_input.Diag_R3==1] = np.nan
	data_input[(data_input.Ux>=50)|(data_input.Ux<=-50)]=np.nan
	data_input[(data_input.Uy>=50)|(data_input.Uy<=-50)]=np.nan
	data_input[(data_input.Uz>=10)|(data_input.Uz<=-10)]=np.nan
	data_input[(data_input.Ts>=50)|(data_input.Ts<=-50)]=np.nan
	data_input[(data_input.CO2>=1000)|(data_input.CO2<=100)]=np.nan
	data_input[(data_input.H2O>=50)|(data_input.H2O<=0)]=np.nan
	return data_input

	
	
if __name__=='__main__':

	plt.style.use('ggplot')
	data=read_co2(test_file_dir)
	#plt.plot(despike_data(data.CO2,6000))
	data_strike=despike_3sig(data.CO2,3000)
	plt.plot(data_strike)
#	plt.plot(despike_data(data.CO2))
#	plt.plot(data.CO2)
#	plt.boxplot(despike_data(data.CO2))
	
	plt.show()

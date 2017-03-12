#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *


def stationary_index(dat,freq=None):
	#This function return the index representing unstablity of turbulence(default using CO2 and Uz),the default time resolution is evey 30minutes
	if freq==None:	
		freq = '30min'
		sub_freq = '5min'
	else:
		freq = freq
		sub_freq = '5min'
	#define a func to compute residual,which is  equal to X-E(X)
	res=lambda x:x-x.mean()
	#compute residual each 30mins
	#if other like Ts,H2O,modify following scripts
	da_30min_a=dat.CO2.resample(freq).apply(res)
	da_30min_b=dat.Uz.resample(freq).apply(res)
	#Compute residual each 5mins
	da_5min_a = dat.CO2.resample(sub_freq).apply(res)
	da_5min_b = dat.Uz.resample(sub_freq).apply(res)
	#Compute covarance of CO2 and Uz(every 30min),corr_30min size=Time/30min
	#cov(X,Y)=E[[X-E(X)][Y-E(Y)]]
	cov_30min=(da_30min_a*da_30min_b).resample(freq).mean()
	#Compute covarance of CO2 and Uz(every 5min)
	cov_5min=(da_5min_a*da_5min_b).resample(sub_freq).mean()
	#compute the average of all 5min corr in each 30mins
	cov_5m_ave=cov_5min.resample(freq).mean()
	#Compute the stationary index IST
	IST = abs((cov_5m_ave-cov_30min)/cov_30min)
	return IST

if __name__=='__main__':
	data=read_co2(test_file_dir)
	dat=clean_data(data)
	IST = stationary_index(dat)
	plt.plot(IST)
	plt.show()

#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *
from monin_obukhov_length import MO_len, ustar


def logic_func(v):
	if v <= -0.1:
		return 1.3*(1.0-3.0*v)**(1.0/3.0)
	elif v>=0.1:
		return 1.5
	else:
		return 1.4
def itc_func(dat,Z=None,freq=None):
	if freq is None:
		freq = '30T'
	else:
		freq = freq
	if Z is None:
		Z=2.0
	else:	
		Z=Z
	sigma_uz_30min = dat.Uz.resample(freq).std()
	u_star=ustar(dat,freq)
	obs_v=sigma_uz_30min/u_star
	L=MO_len(dat,freq)
	kesai = Z/L
	model_v = [logic_func(k) for k in kesai]		
	model_v = pd.Series(model_v,index=obs_v.index)
	ITC=abs((model_v-obs_v)/(model_v))
	return ITC

if __name__=='__main__':
	data=read_co2(test_file_dir)
	dat=clean_data(data)
	ITC=itc_func(dat,Z=2.0,freq='30T')
	plt.plot(ITC)
	plt.show()

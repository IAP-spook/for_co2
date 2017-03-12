#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *
import math

data=read_co2(test_file_dir)
dat = clean_data(data)

freq = '30min'
def MO_len(dat,freq=None):
	if freq==None:
		freq='30min'
	else:
		freq=freq
	#===============================================================================
	#compute friction velocity
	#define a func to compute residual,which is  equal to X-E(X)
	res=lambda x:x-x.mean()
	#compute residual each 30mins
	da_30min_a=dat.Ux.resample(freq).apply(res)
	da_30min_b=dat.Uy.resample(freq).apply(res)
	da_30min_c=dat.Uz.resample(freq).apply(res)
	u_star_1 = (da_30min_a*da_30min_c).resample(freq).mean()
	u_star_2 = (da_30min_b*da_30min_c).resample(freq).mean()
	my_power = lambda x:x**2
	my_bipyramid = lambda x:x**(1.0/4)
	#ustar = map(math.sqrt,map(math.sqrt,u_star_1*u_star_1+u_star_2*u_star_2))
	ustar = (u_star_1.apply(my_power)+u_star_2.apply(my_power)).apply(my_bipyramid)
	#compute virtual temperature,Tv=T(1+0.378e/P)=T(1+0.61q)
	Tv = dat.t_hmp*(1+0.61*dat.rh_hmp/100.0)
	#compute potential virtual temperature,Theta_v=Tv*(P0/P)**kd,kd=0.28572=Rd/Cpd
	#Po=101.325kPa
	Theta = Tv*((101.325/dat.Press).apply(lambda x:x**(0.28572)))
	#compute covariance of Uz and p_v_t
	da_30min_theta = Theta.resample(freq).apply(res)
	cov_30min_heat = (da_30min_c*da_30min_theta).resample(freq).mean()
	#compute monin obukhow length,L=-U*Tv/kgE(w'Tv'),Tv is p_v_t(potential virtual temoerature),karman const=0.35-0.43，we take it 0.4 
	mn_obhf_length = -(ustar.apply(lambda x:x**3)*Theta.resample(freq).mean())/(0.4*9.8*cov_30min_heat) 
#	return ustar, Theta,cov_30min_heat,mn_obhf_length
	return mn_obhf_length


def ustar(dat,freq=None):
	if freq==None:
		freq='30min'
	else:
		freq=freq
	#===============================================================================
	#compute friction velocity
	#define a func to compute residual,which is  equal to X-E(X)
	res=lambda x:x-x.mean()
	#compute residual each 30mins
	da_30min_a=dat.Ux.resample(freq).apply(res)
	da_30min_b=dat.Uy.resample(freq).apply(res)
	da_30min_c=dat.Uz.resample(freq).apply(res)
	u_star_1 = (da_30min_a*da_30min_c).resample(freq).mean()
	u_star_2 = (da_30min_b*da_30min_c).resample(freq).mean()
	my_power = lambda x:x**2
	my_bipyramid = lambda x:x**(1.0/4)
	#ustar = map(math.sqrt,map(math.sqrt,u_star_1*u_star_1+u_star_2*u_star_2))
	ustar = (u_star_1.apply(my_power)+u_star_2.apply(my_power)).apply(my_bipyramid)
	return ustar

if __name__=='__main__':
	data=read_co2(test_file_dir)
	dat = clean_data(data)
	L = MO_len(dat,freq='30min') 
	plt.plot(L)
	plt.show()

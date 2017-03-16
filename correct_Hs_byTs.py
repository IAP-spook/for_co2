#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *

########################## Formula and Consts #########################################################
#                   correcting the sensible heat using Ts				              # 
# H = (1-0.51E[q])*density_atm*Cp*E[w'*Ts']-0.51*density_atm*Cp(E[T]/density_atm)*E[w'*density_vapor']# 
# momentum_flux = -density_atm*(u*)^2								      #
# u* = (E[u'w']**2+E[v'w']**2)^(1/4)								      #	
# H = density_atm*Cp*E[w'T']									      # 	
# lamda*E = lamda*E[w'density_vapor']								      #	
# Fc = E[w'density_co2']									      #	
#+++++++some parameters+++++									      #	
# density_atm = P/(287.059*(Ta+273.15))+density_vapor [kg/m3] Ta[C]						      #
# Cp = Cpd*(1+0.84q)				      [J/kg/K]						      #	
# lamda = (2.501-0.00237*T0)*10^6			[J/kg] T0[C]					      #	
### P is pressure,Ta is temperature of atmos,Cpd = 1004.67[j/kg/K],T0 is surface temperature	      #	
# the unit of density is kg/m^3       								      #
######################################################################################################

def density_air(dat):
	return dat.Press*10**3/(287.059*(dat.Ts/(1+0.51*(dat.rh_hmp/100))+273.15))+dat.H2O*10**(-3)

def Cp(dat):
	return 1004.67*(1+0.84*dat*0.01)

def correct_Hs(dat,freq=None):
	if freq is None:
		freq = '30T'
	else:
		freq = freq
	d_air = density_air(dat)
	d_atm = d_air-dat.H2O*10**(-3)
	res = lambda x:x-x.mean()
	w_disturbance_freq_resample = dat.Uz.resample(freq).apply(res)
	#w_resam =w_disturbance_freq_resample.resample(freq).mean()  
	ts_disturbance_freq_resample = (dat.Ts+273.15).resample(freq).apply(res)
	#ts_resam = ts_disturbance_freq_resample.resample(freq).mean() 	
	vapor_d_r = (dat.H2O*10**(-3)).resample(freq).apply(res)
	#vapor_resam = vapor_d_r.resample(freq).mean()
	w_t_temp = w_disturbance_freq_resample*ts_disturbance_freq_resample 
	w_t = w_t_temp.resample(freq).mean()
	w_v_temp = w_disturbance_freq_resample*vapor_d_r
	w_v = w_v_temp.resample(freq).mean()
	T_from_Ts = dat.Ts/(1+0.51*(dat.rh_hmp/100))+273.15
	T_mean_freq = T_from_Ts.resample(freq).mean()
	d_atm_freq = d_atm.resample(freq).mean()
	d_air_freq = d_air.resample(freq).mean()
	Cp_freq = Cp(dat.rh_hmp).resample(freq).mean()
	temp_H1 = (1-0.51*0.01*dat.rh_hmp.resample(freq).mean())*d_air_freq*Cp_freq*w_t	
	temp_H2 = 0.51*d_air_freq*Cp_freq*(T_mean_freq/d_atm_freq)*w_v
	return temp_H1-temp_H2


def uncorrect_Hs(dat,freq = None):
	if freq is None:
		freq = '30T'
	w_res = dat.Uz.resample(freq).apply(lambda x:x-x.mean())
	ts_res = (dat.Ts+273.15).resample(freq).apply(lambda x:x-x.mean())
	thmp_res = (dat.t_hmp+273.15).resample(freq).apply(lambda x:x-x.mean())
	w_ts = (w_res*ts_res).resample(freq).mean()
	w_thmp = (w_res*thmp_res).resample(freq).mean()
	init_H1 = density_air(dat).resample(freq).mean()*Cp(dat.rh_hmp).resample(freq).mean()*w_ts
	init_H2 = density_air(dat).resample(freq).mean()*Cp(dat.rh_hmp).resample(freq).mean()*w_thmp
	return init_H1
	
if __name__=='__main__':
	data=read_co2(test_file_dir)
	data=clean_data(data)
	H_correct = correct_Hs(data,freq='30T')
	H_uncorrect = uncorrect_Hs(data,freq='30T') 
	plt.plot(H_correct)
	plt.plot(H_uncorrect)
	plt.show()

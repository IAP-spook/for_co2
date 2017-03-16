#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *
data=read_co2(test_file_dir)
data=clean_data(data)

def t_true(dat):
	return dat.Ts/(1.0+0.51*0.01*dat.rh_hmp)

def den_air(dat):
	return dat.Press*10**2/(287.059*(t_true(dat)+273.15))

def den_v(dat):
	return dat.H2O*10**(-3)

def sigma(dat,freq=None):
	if freq is None:
		freq = '30T'
	den_a_fmean = den_air(dat).resample(freq).mean()
	den_v_fmean = (dat.H2O*10**(-3)).resample(freq).mean()
	return den_v_fmean/den_a_fmean

def crt_wpl_liu_LE(dat,freq=None):
	if freq is None:
		freq = '30T'
	res = lambda x:x-x.mean()
	w_res = dat.Uz.resample(freq).apply(res)
	v_res = den_v(dat).resample(freq).apply(res)
	T = t_true(dat)
	t_res = T.resample(freq).apply(res)
	wt_fmean = (w_res*t_res).resample(freq).mean()
	wv_fmean = (w_res*v_res).resample(freq).mean()
	den_v_fmean = den_v(dat).resample(freq).mean()
	den_d_fmean = den_air(dat).resample(freq).mean()
	t_fmean = T.resample(freq).mean()
	#sigma_fmean = sigma(dat).resample(freq).mean()
	E_wpl = (1+1.608*sigma(dat))*(wv_fmean+(den_v_fmean/t_fmean)*wt_fmean)
	E_liu = wv_fmean+(den_v_fmean/(den_v_fmean+den_d_fmean))*0.608*wv_fmean+(den_d_fmean/(den_d_fmean+den_v_fmean))*den_v_fmean*(1+1.608*sigma(dat,freq))*wt_fmean/t_fmean
	lamda = (2.501-0.00237*dat.t_hmp)*10**6
	lamda_fmean = lamda.resample(freq).mean()
	LE_wpl = lamda_fmean*E_wpl
	LE_liu = lamda_fmean*E_liu
	return LE_wpl,lamda_fmean*wv_fmean,LE_liu
	
def crt_wpl_liu_Fc(dat,freq=None):
	if freq is None:
		freq = '30T'
	res = lambda x:x-x.mean()
	w_res = dat.Uz.resample(freq).apply(res)
	v_res = den_v(dat).resample(freq).apply(res)
	c_res = dat.CO2.resample(freq).apply(res)
	c_res = c_res*10**(-6)
	T = t_true(dat)
	t_res = T.resample(freq).apply(res)
	wt_fmean = (w_res*t_res).resample(freq).mean()
	wv_fmean = (w_res*v_res).resample(freq).mean()
	wc_fmean = (w_res*c_res).resample(freq).mean()
	den_v_fmean = den_v(dat).resample(freq).mean()
	den_c_fmean = (data.CO2*10**(-6)).resample(freq).mean()
	den_d_fmean = den_air(dat).resample(freq).mean() 
	t_fmean = T.resample(freq).mean()+273.15
	Fc_wpl = wc_fmean+1.608*(den_c_fmean/den_d_fmean)*wv_fmean+(1+1.608*sigma(dat,freq))*(den_c_fmean/t_fmean)*wt_fmean
	Fc_liu = wc_fmean+(den_c_fmean/(den_d_fmean+den_v_fmean))*0.608*wv_fmean+(den_d_fmean/(den_d_fmean+den_v_fmean))*den_c_fmean*(1+1.608*sigma(dat,freq))*wt_fmean/t_fmean
	return Fc_wpl,wc_fmean,Fc_liu
		



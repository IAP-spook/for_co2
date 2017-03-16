#!/usr/bin/env python
#-*-coding:utf-8-*-
from readco2 import *
from correct_WPL_Liu import *

data = read_co2(test_file_dir)
dat = clean_data(data)
freq = '30T'
res = lambda x:x-x.mean()
w_res = dat.Uz.resample(freq).apply(res)
v_res = den_v(dat).resample(freq).apply(res)
c_res = dat.CO2.resample(freq).apply(res)
c_res = c_res*10**(-6)
t = t_true(dat)
t_res = t.resample(freq).apply(res)
wt_fmean = (w_res*t_res).resample(freq).mean()
wv_fmean = (w_res*v_res).resample(freq).mean()
wc_fmean = (w_res*c_res).resample(freq).mean()
den_v_fmean = den_v(dat).resample(freq).mean()
den_c_fmean = (data.CO2*10**(-6)).resample(freq).mean()
den_d_fmean = den_air(dat).resample(freq).mean() 
t_fmean = t.resample(freq).mean()+273.15
Fc = wc_fmean+1.608*(den_c_fmean/den_d_fmean)*wv_fmean+(1+1.608*sigma(dat,freq))*(den_c_fmean/t_fmean)*wt_fmean

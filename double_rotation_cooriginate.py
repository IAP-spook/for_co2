#!/usr/bin/env python
#-*-coding:utf-8-*-

from readco2 import *
import math


def double_rotation_cooriginate(dat,freq=None):
	if freq == None:
		freq='30min'
	else:
		re_da_mean=dat.resample(freq).mean()
		alpha = map(math.atan, re_da_mean.Uy/re_da_mean.Ux)
		for aa in alpha:
			u1=dat.Ux*math.cos(aa)+dat.Uy*math.sin(aa)
			v1=-dat.Uy*math.sin(aa)+dat.Uy*math.cos(aa)
		w1=dat.Uz

		beta = map(math.atan, re_da_mean.Uz/u1.resample('30min').mean())	
		for bb in beta:
			u2=u1*math.cos(bb)+w1*math.sin(bb)
			w2=-u1*math.sin(bb)+w1*math.cos(bb)
		v2=v1
	return u2,v2,w2


if __name__=='__main__':
	data=read_co2(test_file_dir)
	cl_da=clean_data(data)
	Ux,Uy,Uz = double_rotation_cooriginate(cl_da,freq='30min')
	plt.subplot(3,2,1)
	plt.plot(Ux)
	plt.subplot(3,2,2)
	plt.plot(cl_da.Ux)
	plt.subplot(3,2,3)
	plt.plot(Uy)
	plt.subplot(3,2,4)
	plt.plot(cl_da.Uy)
	plt.subplot(3,2,5)
	plt.plot(Uz)
	plt.subplot(3,2,6)
	plt.plot(cl_da.Uz)
	plt.show()
#	print Ux.resample('30min').mean
#	print Uy.resample('30min').mean
#	print Uz.resample('30min').mean
	

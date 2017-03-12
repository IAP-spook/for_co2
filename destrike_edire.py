#!/usr/bin/env python
# -*-coding:utf-8-*-

from consts_lst import *
from readco2 import read_co2
import matplotlib.pyplot as plt

data = read_co2(test_file_dir)

def destrike_edire_v2(data_to_flt,n_sigma=None):
	if n_sigma:
		nn=n_sigma
	else:
		nn=4
	data = data_to_flt.copy()
	data_diff = data.diff()
	data_diff_std=data_diff.std()	
	for ii,jj in enumerate(data_diff):
		if jj>nn*data_diff_std:
			data.ix[ii] = np.nan
	
	return data
			


if __name__=='__main__':
	print data.head(3)
	plt.plot(destrike_edire_v2(data.CO2))
	plt.show()

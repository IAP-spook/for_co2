#!/usr/bin/env python
# -*-coding:utf-8-*-

from consts_lst import *
from readco2 import *
import os

fns = os.listdir(data_path)
len_fns = len(fns)
fns.sort()
file_path=[os.path.join(data_path,fn) for fn in fns]

def resample_hour_mean(data):
	r_dat=data.resample('H').mean()
	r_dat_std=data.resample('H').std()
	return r_dat,r_dat_std

resam_dat_matrix_mean=pd.DataFrame()
resam_dat_matrix_std=pd.DataFrame()
#file_path1=file_path[0:3]
for fp in file_path:
	print "Reading file %s \n" % fp
	temp_dat=read_co2(fp)
	print "Cleanning data %s\n" % fp
	temp_cl_dat=clean_data(temp_dat)
	print "Concat Data!"
	#print len(temp_cl_dat)
	temp_re=temp_cl_dat.resample('H').mean()
	#print len(temp_re)
	resam_dat_matrix_mean=resam_dat_matrix_mean.append(temp_re)
	#print len(resam_dat_matrix_mean)
	resam_dat_matrix_std=resam_dat_matrix_std.append(temp_cl_dat.resample('H').std())

output_dir=os.path.abspath(os.curdir)
#print output_dir
#print resam_dat_matrix_mean.head(5)
resam_dat_matrix_mean.to_csv(os.path.join(output_dir,'hour_mean.csv'))
resam_dat_matrix_std.to_csv(os.path.join(output_dir,'hour_std.csv'))

print "Successfuly Done!"
		










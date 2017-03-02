#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from hmmlearn import hmm
import os
from matplotlib.dates import YearLocator, MonthLocator


def co2_filter_strike(data_to_flt, window_width, factor):
    data_to_flt = data_to_flt.astype(np.float64)
    data_to_flt[abs(data_to_flt) > 900] = np.nan
    data_to_flt[data_to_flt < 100] = np.nan
    data_roll = data_to_flt.rolling(window=window_width, min_periods=1).mean()
    data_residual = data_to_flt-data_roll
    # data_flt_index=abs(data_residual-data_residual.mean())<3.25*data_residual.std()
    data_flt_index = abs(data_residual) < factor*data_residual.std()
    data_to_flt[data_flt_index == False] = np.nan
    return data_to_flt


def cvt_2_ppm(data_pd):
    _data_co2 = data_pd.CO2.astype(np.float64)
    data_co2_ppm = ((data_pd.t_hmp.astype(np.float64)+273.15)*8.314/(44*data_pd.Press.astype(np.float64)))*_data_co2
    return data_co2_ppm

plt.style.use('ggplot')
input_dir = '/Users/WangYinan/Desktop/DH_2013_2015_ts'
fns = os.listdir(input_dir)
del fns[0]
name_list = ['Time', 'Record_num', 'Ux', 'Uy', 'Uz', 'Ts', 'CO2', 'H2O', 'Press',
             'Diag_R3', 't_hmp', 'rh_hmp', 'e_hmp']
data_raw = pd.read_csv(os.path.join(input_dir, fns[10]), sep=',', header=3, names=name_list, index_col='Time')
data_raw.index = pd.to_datetime(data_raw.index)
data_co2 = cvt_2_ppm(data_raw)
# print type(data_co2)
data_co2 = co2_filter_strike(data_co2, 3000, 3.25)
data_co2 = data_co2.fillna(method='ffill')
# H2O
data_h2o = data_raw.H2O
data_h2o = data_h2o.fillna(method='ffill')
data_h2o = np.atleast_2d(data_h2o).T
# Pressure
data_p = data_raw.Press.fillna(method='ffill')
data_p = np.atleast_2d(data_p).T
# print len(data_co2)
data_random = data_co2-data_co2.rolling(window=3000, min_periods=1).mean()
data_random = np.atleast_2d(data_random).T
# print len(data_random)
data_sample = np.column_stack([data_random, data_h2o, data_p])
# length = [len(data_random), len(data_h2o)]
print("fitting to HMM and decoding ...")

model = hmm.GaussianHMM(n_components=4, covariance_type='diag', n_iter=1000).fit(data_sample)
latent_states = model.predict(data_sample)

print("done")
print("Transition matrix")
print(model.transmat_)
print()

print("Means and vars of each hidden state")
for i in range(model.n_components):
    print("{0}th hidden state".format(i))
    print("mean = ", model.means_[i])
    print("var = ", np.diag(model.covars_[i]))
    print()

# plt.figure(figsize=(15, 8))

for i in range(model.n_components):
    state = (latent_states == i)
    plt.plot(data_co2.index[state], data_random[state], '.', label='latent state %d'%i, lw=1)
    plt.legend()

plt.show()
'''

fig, axs = plt.subplots(model.n_components, sharex=True, sharey=True)
colours = cm.rainbow(np.linspace(0, 1, model.n_components))
for i, (ax, colour) in enumerate(zip(axs, colours)):
    # Use fancy indexing to plot data in each state.
    mask = latent_states == i
    ax.plot_date(data_co2.index[mask], data_co2[mask], ".-", c=colour)
    ax.set_title("{0}th hidden state".format(i))

    # Format the ticks.
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_minor_locator(MonthLocator())

    ax.grid(True)

plt.show()
'''



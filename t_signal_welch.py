#!/usr/bin/env python
#-*-coding:utf-8-*-

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
#fs是采样频率，本例信号x的时间间隔是0.0001s正好是1/fs
fs = 10e3
#x的长度为N
N = 1e5
amp = 2*np.sqrt(2)
freq = 1234.0
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
# nperseg是每段的长度
f, Pxx_den = signal.welch(x, fs, nperseg=1024,scaling='spectrum')
plt.semilogy(f, Pxx_den)
plt.ylim([0.5e-3, 1])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()

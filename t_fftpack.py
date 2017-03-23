#!/usr/bin/env python
#-*-coding:utf-8-*-

from scipy.fftpack import fft,ifft
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
'''
确定信号分为能量信号和功率信号，随机信号一定是功率信号。
能量信号可以进行傅里叶变换，得到频谱的幅度再平方即为能量谱（或称能量谱密度）。能量谱对时间平均即为功率谱。
功率信号不是说不存在傅里叶变换，而应该说是在频域引入冲激响应为前提下存在（通过傅里叶级数间接推导），频谱是离散的，例如无限长周期双频正弦的傅里叶变换频谱为频域两个离散的脉冲。
然后是属于功率信号中的随机信号能否写成傅里叶级数展开，进而得到对应的傅里叶变换频谱有点涉及极限概念的讨论，可以姑且先不深究，因为我们有对随机信号有更好的处理手段，那就是功率谱估计。

所以总结，频谱和能量谱（也叫能量谱密度）是傅里叶变换得到的复数结果和模平方的关系；
而功率谱（也就是功率谱密度）是针对随机信号分析提出的概念。

然后在前面问说有对随机信号直接做FFT的做法其实就是截断成能量信号进行处理，上面也解释了这种处理不符合随机信号定义，
但之所以还有人这样来说，我觉得应该是做语音信号之类的非平稳信号处理时，做短时频域分析下作的近似处理。
'''
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
# nperseg是每段的长度，density是功率谱密度，单位是v*2/Hz,spectrum是功率谱单位是V**2
f, Pxx_den = signal.welch(x, fs, nperseg=1024,scaling='density')
xx = np.linspace(0.0,fs/2,len(x)//2)
ff = fft(x)
# Fourier变换的幅度取模，平方等到能量谱，在对时间平均也可得到功率谱，这只适合确定信号，即能量信号，随机信号为功率信号，要通过求自相关函数，在FFT，即可求得功率谱，功/频率
fff = (abs(ff)**2)/N
f3=fff/sum(fff)
#f4=Pxx_den/f
plt.subplot(2,1,1)
plt.plot(f,Pxx_den)
plt.subplot(2,1,2)
plt.plot(xx,abs(f3[0:(len(x))//2]))
plt.show() 

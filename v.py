#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.signal import blackmanharris, fftconvolve
import os
import wave
from pylab import *

files_path = './train/'

def list_files(files):
  processed = []
  for f in files:
    if f[0] == '0':
      processed.append(files_path + f)
  return processed

files = os.listdir(files_path)
files = list_files(files)

detected = 0

frame_size = 1024



for f_name in files:

  original_gender = f_name[len(f_name) - 5]
  deteceted_gender = 'K'

  f = wave.open(f_name)

  fs = f.getframerate()
  signal = f.readframes(-1)
  signal = np.fromstring(signal, 'Int16')

  subplot(321)
  plot(signal)

  start_index = 15000
  frame_size = 4096
  end_index = start_index + frame_size - 1
  signal = signal[start_index:int(end_index) + 1]

  subplot(324)
  plot(signal)

  fftResult = np.log(abs(fft(signal)))
  ceps = ifft(fftResult)

  subplot(322)
  plot(fftResult)

  subplot(323)
  plot(ceps)

  nceps = len(ceps)
  peaks = np.zeros(nceps)

  print len(peaks)

  k=3

  while(k <= nceps - 2):
    y1 = ceps[k - 1]
    y2 = ceps[k]
    y3 = ceps[k + 1]
    if (y2 > y1 and y2 >= y3):
      peaks[k]=ceps[k]
    k = k + 1
  subplot(325)
  plot(peaks)

  # print f.getsampwidth()/(max(peaks)+1)
  print f.getframerate()

  # print posmax

  show()

  f.close()

  if original_gender == deteceted_gender:
    detected += 1

print float(detected)/float(len(files))

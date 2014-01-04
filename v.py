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

  fftResult = np.log(abs(fft(signal)))
  ceps = ifft(fftResult)

  posmax = ceps.argmax()

  print posmax

  f.close()

  if original_gender == deteceted_gender:
    detected += 1

print float(detected)/float(len(files))

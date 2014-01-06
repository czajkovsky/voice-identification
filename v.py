#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import scipy.io.wavfile
import struct
from pylab import *
from numpy import *
from scipy import *
from os import listdir
import sys
import os
import wave
from scikits.audiolab import wavread

def file_preprocessing(path):
  data, fs, encoding = wavread(path)
  signal = [mean(d) for d in data]

  f = wave.open(path, "r")
  frames = f.getnframes()
  fs = f.getframerate()
  f.close()

  return (signal, fs, frames)

def m_frequency(data):

  signal, fs, frames = data

  T = frames / fs
  period = 1.5
  n = int(min(T, period) * fs)

  signal = signal[0:n]

  amplitude = abs(fft(signal)) #glosnosc
  frequency = linspace(0, fs, n)

  amp, freq = [], []
  for i in range(len(frequency)):
    if 85 < frequency[i] < 230:
      freq.append(frequency[i])
      amp.append(amplitude[i])

  maxAmp = max(amp)
  for i in range(len(amp)):
    if amp[i] == maxAmp:
      freqOfMax = freq[i]

  return freqOfMax


def list_files(files):
  processed = []
  for f in files:
    if f[0] == '0':
      processed.append(files_path + f)
  return processed

files_path = './train/'

files = os.listdir(files_path)
files = list_files(files)

detected = 0
count = 0

for f_name in files:

  original_gender = f_name[len(f_name) - 5]

  detected_gender = 'K'
  if m_frequency(file_preprocessing(f_name)) < 175:
    detected_gender = 'M'

  count += 1
  if original_gender == detected_gender:
    detected += 1

  print detected_gender, " / ", original_gender, '\t', "{0:.0f}%".format(float(detected)/float(count)*100)

print float(detected)/float(len(files))







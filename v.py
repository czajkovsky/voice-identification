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

def line_stats(detected_k, count_k, detected_m, count_m, detected, original_gender):

  if count_k == 0:
    ratio_k = '\t\t-'
  else:
    ratio_k = float(detected_k) / float(count_k) * 100
    ratio_k = "\t\tK:{0:.0f}%".format(ratio_k)

  if count_m == 0:
    ratio_m = '\t\t-'
  else:
    ratio_m = float(detected_m) / float(count_m) * 100
    ratio_m = "\t\tM:{0:.0f}%".format(ratio_m)

  ratio_g = float(detected_k + detected_m) / float(count_k + count_m) * 100
  ratio_g = "\t\tG:{0:.0f}%".format(ratio_g)

  print "[", original_gender, "]", detected, ratio_g, ratio_k, ratio_m

def file_preprocessing(path):
  data, fs, enc = wavread(path)
  signal = [mean(d) for d in data]

  f = wave.open(path, "r")
  frames = f.getnframes()
  fs = f.getframerate()
  f.close()

  return (signal, fs, frames)

def m_frequency(data):

  signal, fs, frames = data

  T = frames / fs
  period = 1.7
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

detected_k = 0
detected_m = 0
count_k = 0
count_m = 0

for f_name in files:

  original_gender = f_name[len(f_name) - 5]

  detected_gender = 'K'
  detected = False

  if m_frequency(file_preprocessing(f_name)) < 172:
    detected_gender = 'M'

  if original_gender == 'K':
    count_k += 1
    if detected_gender == original_gender:
      detected = True
      detected_k += 1
  else:
    count_m += 1
    if detected_gender == original_gender:
      detected = True
      detected_m += 1

  line_stats(detected_k, count_k, detected_m, count_m, detected, original_gender)

print "\n---------\n\n"
print "M: ", detected_m, "/", count_m, "({0:.0f}%)".format(float(detected_m) / float(count_m) * 100)
print "M: ", detected_k, "/", count_k, "({0:.0f}%)".format(float(detected_k) / float(count_k) * 100)





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

files_path = './train/'

def line_stats(detected_k, count_k, detected_m, count_m, detected, original_gender):

  if count_k == 0:
    ratio_k = '\t\tK:-'
  else:
    ratio_k = float(detected_k) / float(count_k) * 100
    ratio_k = "\t\tK:{0:.0f}%".format(ratio_k)

  if count_m == 0:
    ratio_m = '\t\tM:-'
  else:
    ratio_m = float(detected_m) / float(count_m) * 100
    ratio_m = "\t\tM:{0:.0f}%".format(ratio_m)

  ratio_g = float(detected_k + detected_m) / float(count_k + count_m) * 100
  ratio_g = "\t\tG:{0:.0f}%".format(ratio_g)

  print "%02d" % (count_m + count_k,), ": [", original_gender, "]", detected, ratio_g, ratio_k, ratio_m

def file_preprocessing(path):
  data, fs, enc = wavread(path)
  signal = [mean(d) for d in data]

  f = wave.open(path, "r")
  frames = f.getnframes()
  fs = f.getframerate()
  f.close()

  return (signal, fs, frames)

def m_frequency(data, period):

  signal, fs, frames = data

  T = frames / fs
  n = int(min(T, period) * fs)

  signal = signal[0:n]

  amp = abs(fft(signal))
  freq = linspace(0, fs, n)

  p_amp, p_freq = [], []
  for i in range(len(freq)):
    if 85 < freq[i] < 230:
      p_freq.append(freq[i])
      p_amp.append(amp[i])

  return p_freq[p_amp.index(max(p_amp))]

def list_files(files):
  processed = []
  for f in files:
    if f[0] == '0':
      processed.append(files_path + f)
  return processed

def classify_gender(period, diff, stats):

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

    if m_frequency(file_preprocessing(f_name), period) < diff:
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

    if stats:
      line_stats(detected_k, count_k, detected_m, count_m, detected, original_gender)

  if stats:
    print "---------------"
    print "M: ", detected_m, "/", count_m, "({0:.0f}%)".format(float(detected_m) / float(count_m) * 100)
    print "K: ", detected_k, "/", count_k, "({0:.0f}%)".format(float(detected_k) / float(count_k) * 100)
    print "---------------"
    print "G: ", detected_m + detected_k, "/", count_m + count_k, "({0:.0f}%)".format(float(detected_k + detected_m) / float(count_k + count_m) * 100)

  return (detected_m, detected_k)

if __name__ == '__main__':
  period = 1.7
  diff = 170
  stats = True
  detected_m, detected_k = classify_gender(period, diff, stats)


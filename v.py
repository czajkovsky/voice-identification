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

def freq_from_crossings(sig, fs):
  indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
  crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
  return fs / mean(diff(crossings))

def freq_from_autocorr(sig, fs):
  corr = fftconvolve(sig, sig[::-1], mode='full')
  corr = corr[len(corr)/2:]

  d = diff(corr)
  start = find(d > 0)[0]

  px = argmax(corr[start:]) + start

  return fs / px

def m_frequency(path):

  data, fs, encoding = wavread(path)
  signal = [mean(d) for d in data]

  wfile = wave.open(path, "r")
  T = (1.0 * wfile.getnframes()) / wfile.getframerate()

  wfile.close()

  sec = 2

  if sec != None:
    if T > sec: #one second is enought
      T = sec
  n = T * fs
  n = int(n)

  if sec != None:
    signal = signal[0:n]

  amplitude = abs(fft(signal)) #glosnosc
  frequency = linspace(0, fs, n)

  #sound less then 85 or higher then 255 are unreachable for humans
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

  if m_frequency(f_name) < 175:
    detected_gender = 'M'

  count += 1
  if original_gender == detected_gender:
    detected += 1

  print detected_gender, " / ", original_gender, '\t', "{0:.0f}%".format(float(detected)/float(count)*100)

print float(detected)/float(len(files))







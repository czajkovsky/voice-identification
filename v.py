#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from pylab import *
import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import os
import wave

K = 3          # number of windows
L = 8192       # 1st pass window overlap, 50%
M = 16384      # 1st pass window length
N = 32768      # 1st pass DFT lenth: acyclic correlation

def welch(x, w, L, N):
    # Welch's method
  M = len(w)
  K = (len(x) - L) / (M - L)
  Xsq = zeros(N/2+1)                  # len(N-point rfft) = N/2+1
  for k in range(K):
    m = k * ( M - L)
    xt = w * x[m:m+M]
    Xsq = Xsq + abs(rfft(xt, N)) ** 2
  Xsq = Xsq / K
  Wsq = abs(rfft(w, N)) ** 2
  bias = irfft(Wsq)                   # for unbiasing Rxx and Sxx
  p = dot(x,x) / len(x)               # avg power, used as a check
  return Xsq, bias, p

def detect_frequency(g, fs):

  K = 3
  L = 8192
  M = 16384
  N = 32768

  g = g / float64(max(abs(g)))
  mi = len(g) / 4

  x = g[mi:mi + K*M - (K-1)*L]
  w = hamming(M)

  Xsq, bias, p = welch(x, w, L, N)
  Rxx = irfft(Xsq)
  Rxx = Rxx / bias
  mp = argmax(Rxx[28:561]) + 28

  N = M = L - (L % mp)
  x = g[mi:mi+K*M]
  w = ones(M); L = 0
  Xsq, bias, p = welch(x, w, L, N)
  Rxx = irfft(Xsq)
  Rxx = Rxx / bias
  mp = argmax(Rxx[28:561]) + 28

  Sxx = Xsq / bias[0]
  Sxx[1:-1] = 2 * Sxx[1:-1]
  Sxx = Sxx / N
  n0 = N / mp
  np = argmax(Sxx[n0-2:n0+3]) + n0-2

  m = -1
  m_i = -1
  s = 0
  fq = 0
  for x in range(0, len(Sxx)):
    if x > 14 and x < 45:
      s = s + Sxx[x]
      fq = fq + x * Sxx[x]

  return fq / s * 5.5

  subplot2grid((2,1), (1,0))
  title('Power Spectral Density, S$_{xx}$'); xlabel('Frequency (Hz)')
  fr = r_[:5 * np]; f = fs * fr / N;
  vlines(f, 0, Sxx[fr], colors='b', linewidth=2)
  grid(); axis('tight'); ylim(0,1.25*max(Sxx[fr]))
  show()

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
avg_f = 0.0

for f_name in files:

  original_gender = f_name[len(f_name) - 5]
  deteceted_gender = 'K'

  f = wave.open(f_name)

  fs = f.getframerate()
  signal = f.readframes(-1)
  signal = np.fromstring(signal, 'Int16')

  freq = detect_frequency(signal, fs)

  if freq > 154.0:
    deteceted_gender = 'M'

  avg_f = avg_f + freq

  f.close()

  if original_gender == deteceted_gender:
    detected += 1

print float(detected)/float(len(files))
print float(avg_f)/float(len(files))







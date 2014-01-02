#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
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

for f in files:
  original_gender = f[len(f) - 5]
  deteceted_gender = 'K'

  if original_gender == deteceted_gender:
    detected += 1

print float(detected)/float(len(files))

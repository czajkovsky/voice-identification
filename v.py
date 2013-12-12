#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import wave
from os import listdir


files_path = './train/'
files = listdir(files_path)
detected = 0

for f_name in files:
  original_gender = f_name[4]
  deteceted_gender = 'K'

  wave.open(files_path + f_name, 'r')

  if original_gender == deteceted_gender:
    detected += 1

print float(detected)/float(len(files))

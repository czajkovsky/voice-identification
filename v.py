#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import wave
from os import listdir


files_path = './train/'
files = listdir(files_path)

for f_name in files:
  original_gender = f_name[4]
  wave.open(files_path + f_name, 'r')
  print original_gender

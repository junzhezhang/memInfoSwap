import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from unit_functions import *
from random import shuffle
from scipy.stats import gaussian_kde

#fileName1 = 'vec_run_5_alex.csv'
#fileName2 = 'vec_run_5_resnet.csv'
#fileName3 = 'vec_run_5_vgg.csv'

truePath ="/Users/junzhezhang/Downloads/offline-singa/"

fileName1 = truePath+'vec_run_5_alex.csv'
fileName2 = truePath+'vec_run_5_resnet.csv'
fileName3 = truePath+'vec_run_5_vgg.csv'

def csv_to_raw_list(fileName1):
  f2 = open(fileName1)
  rows = f2.read().splitlines()
  split_rows = []
  for row in rows:
    values = row.split(' ')
    split_rows.append([int(values[0]),values[1],values[2],int(values[3])])
  return split_rows

vec_run= csv_to_raw_list(fileName3)
print (vec_run[0])
load = []
for row in vec_run:
  if row[1] == "Malloc":
    if len(load)>0:
      load.append(load[-1]+(row[3]>>20))
    else:
      load.append(row[3]>>20)
  if row[1] == "Free":
    load.append(load[-1]-(row[3]>>20))
  if (row[1] != "Malloc" or row[1] != "Free"):
    load.append(load[-1])
print ("verify length")
print (len(vec_run))
print (len(load))
x_list = range(0,len(load))


font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14}
plt.rc('font', **font)
plt.xlabel('Operation Index over 5 Iterations',fontsize=16)
plt.ylabel('Memory Load in MB',fontsize=16)
plt.plot(x_list,load,linewidth=3)
plt.xlim([0,25000])
plt.ylim([0,700])
plt.show()

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from unit_functions import *
from random import shuffle
from scipy.stats import gaussian_kde


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
    split_rows.append([int(values[0]),values[1],values[2],int(values[3]),values[4]])
  return split_rows

vec_run_alex= csv_to_raw_list(fileName1)
vec_run_resnet= csv_to_raw_list(fileName2)
vec_run_vgg= csv_to_raw_list(fileName3)

distinct_blocks_alex = blockInfo_list_to_distinct_blocks(vec_run_alex[1247:1247+612*3])
distinct_blocks_vgg = blockInfo_list_to_distinct_blocks(vec_run_vgg[8737:8737+4144*3])
distinct_blocks_resnet = blockInfo_list_to_distinct_blocks(vec_run_resnet[6675:6675+3172*3])

size_1 = []
size_2 = []
size_3 = []
largest_size_1 = 0
largest_size_2 = 0
largest_size_3 = 0
for block in distinct_blocks_alex:
  size_1.append(block[0][3]>>20)
  largest_size_1=max(largest_size_1,block[0][3]>>20)
for block in distinct_blocks_resnet:
  size_2.append(block[0][3]>>20)
  largest_size_2=max(largest_size_2,block[0][3]>>20)
for block in distinct_blocks_vgg:
  size_3.append(block[0][3]>>20)
  largest_size_3=max(largest_size_3,block[0][3]>>20)


fig, ax = plt.subplots()

density_1 = gaussian_kde(size_1)
xs_1 = np.linspace(0,largest_size_1+5,200)
density_1.covariance_factor = lambda : .25
density_1._compute_covariance()
ax.plot(xs_1,density_1(xs_1),'g--', label='AlexNet')

density_2 = gaussian_kde(size_2)
xs_2 = np.linspace(0,largest_size_2+5,200)
density_2.covariance_factor = lambda : .25
density_2._compute_covariance()
ax.plot(xs_2,density_2(xs_2),'b--', label='ResNet')

density_3 = gaussian_kde(size_3)
xs_3 = np.linspace(0,largest_size_3+5,200)
density_3.covariance_factor = lambda : .25
density_3._compute_covariance()
ax.plot(xs_3,density_3(xs_3),'y--', label='VGG')

plt.xlabel('variable size in MB',fontsize = 16)
plt.ylabel('frequency',fontsize =16)
legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#00FFCC')
plt.show()
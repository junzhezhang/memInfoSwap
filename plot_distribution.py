import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from unit_functions import *
from random import shuffle
from scipy.stats import gaussian_kde
# reference https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
smallest_block = 1<<20
truePath ="/Users/junzhezhang/Downloads/offline-singa/"

fileName1 = truePath+"vec_block_fresh_vgg.csv"
fileName2 = truePath+"load_origin_vgg.csv"
maxLen = 3172
location = 6675
maxIdx = 1369
memLimit = 300

vec_run = csv_blockInfo_to_list(fileName1,maxLen)
print vec_run[0]
load_origin = csv_load_to_list(fileName2)
distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)

size_list = []
x_bound = 0
y_bound = 0
largest_size = 0
for block in distinct_blocks:
  size_list.append(block[0][3]>>20)
  largest_size=max(largest_size,block[0][3]>>20)

print len(size_list)
# histagram
# plt.hist(size_list,bins=50)
# plt.legend()
# plt.xlabel('variable size in MB')
# plt.ylabel('frequency')
# # ax.set_xlim((0, largest_size))
# # plt.title('Side-by-Side Histogram with Multiple Airlines')
# plt.show()

density = gaussian_kde(size_list)
xs = np.linspace(0,largest_size+5,200)
density.covariance_factor = lambda : .25
density._compute_covariance()
plt.plot(xs,density(xs))
plt.xlabel('variable size in MB')
plt.ylabel('frequency')
plt.show()
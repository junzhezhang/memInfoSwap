import csv
import numpy as np
# import matplotlib.pyplot as plt
from unit_functions import *
# from bo_run.py import compute_and_normalize_sorters

from bayes_opt import BayesianOptimization
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
# %matplotlib inline


truePath ="/Users/junzhezhang/Downloads/offline-singa/"

smallest_block = 1<<20

fileName1 = truePath+"vec_block_fresh_vgg.csv"
fileName2 = truePath+"load_origin_vgg.csv"
maxLen = 3172
location = 6675
maxIdx = 1369

memLimit = 400<<20

vec_run = csv_blockInfo_to_list(fileName1,maxLen)
load_origin = csv_load_to_list(fileName2)
distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)
vec_swap = get_swappable_blocks(distinct_blocks,maxIdx,smallest_block)

a,b = load_over_limit(load_origin,memLimit,0,maxLen,maxLen)
print a,b
# 44,2260
print len(vec_swap)
vec_swap_outter_limit = []
for i in range(0,len(vec_swap)):
  if vec_swap[i].r_idx <=a and vec_swap[i].d_idx >= b:
    #print vec_swap[i].r_idx#, vec_swap[d].d_idx
    vec_swap_outter_limit.append(vec_swap[i])

print len(vec_swap_outter_limit)

load_updated = list(load_origin)
for i in range(0,len(vec_swap_outter_limit)):
  # print vec_swap_outter_limit[i].r_idx
  load_update(load_updated,vec_swap_outter_limit[i].r_idx,
    vec_swap_outter_limit[i].d_idx,-1,vec_swap_outter_limit[i].size,maxLen)

c,d = load_over_limit(load_updated,memLimit,0,maxLen,maxLen)
print c,d
e,f = load_peak(load_origin,maxLen)
print e,f
e,f = load_peak(load_updated,maxLen)
print e,f

# print "-------- dt <0"
# for i in range(0,len(vec_swap)):
#   if vec_swap[i].dt <=0:
#     print vec_swap[i].r_idx,vec_swap[i].d_idx,vec_swap[i].size


compute_and_normalize_sorters(vec_swap,load_origin,maxLen)
vec_swap.sort(key=lambda x: x.wdto, reverse=True)
vec_swap_selct,load_updated = swap_select(vec_swap,load_origin,memLimit,maxLen)
load_no_overhead,overhead,total_dt = swap_sched(vec_swap_selct,load_origin,vec_run,memLimit,
      "stick-to-limit",maxIdx,maxLen)
print overhead
print "--------------------- see if r_idx < 900"
vec_swap.sort(key=lambda x: x.r_idx, reverse=True)
for itm in vec_swap:
  if 352 < itm.r_idx < 1042:
    print itm.r_idx,itm.d_idx,itm.size




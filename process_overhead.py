

import csv
import numpy as np
import matplotlib.pyplot as plt
from unit_functions import *


# input as raw vec_run from itr0 - 9 itr.: to cut into 3 fresh iterations. when it is swtiched.
# no load


# vgg
maxLen = 3172
location = 6675
relativePath = "vec_run_10itr_vgg13_cifar.csv"



truePath ="/Users/junzhezhang/Downloads/offline-singa/"
fileName1 = truePath + relativePath

smallest_block = 1<<20

vec_run_full = full_csv_blockInfo_to_full_list(fileName1)

vec_load_full = full_list_to_full_load(vec_run_full)

print vec_run_full[1]
print len(vec_run_full)
print len(vec_load_full)
print "hello world"

# x = range(0,len(vec_load_full))
# plt.xlabel('operation index over 5 iterations',fontsize =16)
# plt.ylabel('memory load in MB',fontsize=16)
# plt.plot(x,vec_load_full)
# plt.show()

# i = location
# temp_time = vec_run_full[i][-1]
# while (i<len(vec_run_full)-maxLen):
#   i = i +maxLen
#   print vec_run_full[i][-1]
#   print (vec_run_full[i][-1] - temp_time)/1000000
#   temp_time = vec_run_full[i][-1]

# cut into 3 fresh iteration.
vec_run = vec_run_full[location+4*maxLen:location+7*maxLen]
for i in range(0,len(vec_run)):
  vec_run[i][0] = i
load_origin = vec_load_full[location+4*maxLen:location+7*maxLen]
print len(vec_run)

maxLoad, maxIdx = load_peak(load_origin,maxLen)
print str(maxLoad)+"----- maxLoad "+str(maxIdx)


###
distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)

vec_swap = get_swappable_blocks(distinct_blocks,maxIdx,smallest_block)

print "------ to get lowest memory"
lowest_memLimit = get_lowest_memLimit(vec_swap,load_origin,maxLen)

print "lowest memory limit: "+str(lowest_memLimit>>20)
print "lowest memory limit: "+str(lowest_memLimit>>20)

a = lowest_memLimit
b = maxLoad
c = 10<<20

memLimit_list = range(a,b,c)

overhead_pri = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c, "pri",maxLen,maxIdx)

overhead_dto = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c, "dto",maxLen,maxIdx)

overhead_dt = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c,"dt",maxLen,maxIdx)

overhead_wdto = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c,"wdto",maxLen,maxIdx)

overhead_pri_net = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c,"pri_net",maxLen,maxIdx)

overhead_sub_wdto = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c,"sub-wdto",maxLen,maxIdx)

# overhead_ridx = overhead_from_sorted_block(vec_swap,load_origin,vec_run,a,b,c,"r_idx",maxLen,maxIdx)

print "below is overheads--------------------"
print memLimit_list
print overhead_pri
print overhead_dto
print overhead_dt
print overhead_wdto
print overhead_pri_net
print overhead_sub_wdto
print "done --------------------------"

fig, ax = plt.subplots()
ax.plot(memLimit_list, overhead_dto, 'g--', label='overhead_dto')
ax.plot(memLimit_list, overhead_pri, 'r:', label='overhead_pri')
ax.plot(memLimit_list, overhead_dt, 'b:', label='overhead_dt')
ax.plot(memLimit_list, overhead_wdto, 'y--', label='overhead_wdto')
ax.plot(memLimit_list, overhead_pri_net, 'm--', label='overhead_pri_net')
ax.plot(memLimit_list, overhead_sub_wdto, 'k--', label='overhead_sub_wdto')
#ax.plot([400<<20], [205000], 'c--', label='overhead_r_idx')
legend = ax.legend(loc='upper right', shadow=True, fontsize='x-small')
# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#00FFCC')

plt.show()








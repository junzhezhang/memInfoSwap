import csv
import numpy as np
import matplotlib.pyplot as plt
from unit_functions import *

truePath ="/Users/junzhezhang/Downloads/offline-singa/"

smallest_block = 1<<20

fileName1 = truePath+"vec_block_fresh_vgg.csv"
fileName2 = truePath+"load_origin_vgg.csv"
maxLen = 3172
location = 6675
maxIdx = 1369
a = 280<<20
b = 680<<20
c = 10<<20

vec_run = csv_blockInfo_to_list(fileName1,maxLen)

load_origin = csv_load_to_list(fileName2)

maxLoad, maxIdx_t = load_peak(load_origin,maxLen)
print str(maxLoad)+"----- maxLoad"

distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)

vec_swap = get_swappable_blocks(distinct_blocks,maxIdx,smallest_block)

print "------ to get lowest memory"
lowest_memLimit = get_lowest_memLimit(vec_swap,load_origin,maxLen)

print "lowest memory limit: "+str(lowest_memLimit)


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





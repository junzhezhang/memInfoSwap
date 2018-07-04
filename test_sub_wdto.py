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

vec_run = csv_blockInfo_to_list(fileName1,maxLen)
load_origin = csv_load_to_list(fileName2)
distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)
vec_swap = get_swappable_blocks(distinct_blocks,maxIdx,smallest_block)
memLimit = 350<<20

# itm = vec_swap[0]
# print itm.r_idx,itm.d_idx,itm.size
# load_origin = csv_load_to_list(fileName2)
# load_updated = list(load_origin)
# load_update(load_updated,itm.r_idx,itm.d_idx,-1,itm.size,maxLen)
# x_list = range(0,len(load_origin))
# fig, ax = plt.subplots()
# ax.plot(x_list, load_origin, 'g--', label='overhead_dto')
# ax.plot(x_list, load_updated, 'r:', label='overhead_pri')
# legend = ax.legend(loc='upper right', shadow=True, fontsize='x-small')
# # Put a nicer background color on the legend.
# legend.get_frame().set_facecolor('#00FFCC')
# plt.show()

print "hello world"
print len(vec_swap)
vec_load = list(load_origin)
vec_swap_temp = list(vec_swap)
vec_swap = []
print len(vec_swap)
print len(vec_swap_temp)
sub_wdto_list = []

# x_list = range(0,len(load_origin))
# fig, ax = plt.subplots()
# ax.plot(x_list, load_origin, 'g--', label='overhead_dto')
# legend = ax.legend(loc='upper right', shadow=True, fontsize='x-small')
# # Put a nicer background color on the legend.
# legend.get_frame().set_facecolor('#00FFCC')
# plt.show()

while (len(vec_swap_temp) > 0):
    current_len = len(vec_swap_temp)
    for i in range(0,current_len):
      itm = vec_swap_temp[i]
      itm.sub_wdto = 0
      for j in range(itm.r_idx,itm.d_idx):
        itm.sub_wdto+=vec_load[j+maxLen]
      vec_swap_temp[i] = itm
    vec_swap_temp.sort(key=lambda x: x.sub_wdto, reverse=True)
    # print "-----------------------------"
    # print "size select "+str(vec_swap_temp[0].size)
    # print "select block ("+str(vec_swap_temp[0].r_idx)+" "+str(vec_swap_temp[0].d_idx)+")"+str(vec_swap_temp[0].sub_wdto)
    # print "reject block ("+str(vec_swap_temp[1].r_idx)+" "+str(vec_swap_temp[0].d_idx)+")"+str(vec_swap_temp[1].sub_wdto)    
    # vec_swap_temp[0].sub_wdto = 1/vec_swap_temp[0].sub_wdto #TODO note it's 1/sub_wdto
    sub_wdto_list.append(vec_swap_temp[0].sub_wdto)
    # print vec_swap_temp[0].sub_wdto
    # print vec_swap_temp[0].size 
    # print vec_swap_temp[0].r_idx,vec_swap_temp[0].d_idx,vec_swap_temp[0].size,maxLen
    # print "before update "+str(vec_load[vec_swap_temp[0].r_idx+maxLen])
    # load_update(load_updated,itm.r_idx,itm.d_idx,-1,itm.size,maxLen)
    load_update(vec_load,vec_swap_temp[0].r_idx,vec_swap_temp[0].d_idx,-1,vec_swap_temp[0].size,maxLen)
    # print "after update "+str(vec_load[vec_swap_temp[0].r_idx+maxLen])
    vec_swap.append(vec_swap_temp[0])
    vec_swap_temp.remove(vec_swap_temp[0])


def compute_wdto(vec_swap):
  for i in range(0, len(vec_swap)):
    itm = vec_swap[i]
    for j in range(itm.r_idx, itm.d_idx):
      itm.wdto+=vec_load[i]
    vec_swap[i] = itm

def comput_sub_wdto(vec_swap_temp):
  while (len(vec_swap_temp) > 0):
    current_len = len(vec_swap_temp)
    for i in range(0,current_len):
      itm = vec_swap_temp[i]
      itm.sub_wdto = 0
      for j in range(itm.r_idx,itm.d_idx):
        itm.sub_wdto+=vec_load[j+maxLen]
      vec_swap_temp[i] = itm
    vec_swap_temp.sort(key=lambda x: x.sub_wdto, reverse=True)
    sub_wdto_list.append(vec_swap_temp[0].sub_wdto)

    load_update(vec_load,vec_swap_temp[0].r_idx,vec_swap_temp[0].d_idx,-1,vec_swap_temp[0].size,maxLen)
    vec_swap.append(vec_swap_temp[0])
    vec_swap_temp.remove(vec_swap_temp[0])

  return vec_swap
# vec_swap = comput_sub_wdto(vec_swap)
vec_swap.sort(key=lambda x: x.sub_wdto, reverse=True)
vec_swap_selct, load_updated = swap_select(vec_swap,load_origin,memLimit,maxLen)
print "====== print select idx "+str(len(vec_swap_selct))
for i in range(0,len(vec_swap_selct)):
  print vec_swap_selct[i].r_idx
load_no_overhead,overhead,total_dt = swap_sched(vec_swap_selct,load_origin,vec_run,memLimit,
      "stick-to-limit",maxIdx,maxLen)
print "overhead "+str(overhead/1000000)



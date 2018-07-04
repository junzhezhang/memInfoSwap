import csv
import numpy as np
# import matplotlib.pyplot as plt
from unit_functions import *
from bayes_opt import BayesianOptimization

from bayes_opt import BayesianOptimization
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import gridspec
# %matplotlib inline


def target (a, b, c, d):
  b = 0
  for i in range(0,len(vec_swap)):
    itm = vec_swap[i]
    itm.bo = a*itm.pri_net + b*itm.dt + c*itm.wdto + d*itm.sub_wdto
    vec_swap[i] = itm
    # print itm.pri_net,itm.dt,itm.wdto,itm.sub_wdto
  vec_swap.sort(key=lambda x: x.bo, reverse=True)
  vec_swap_selct,load_updated = swap_select(vec_swap,load_origin,memLimit,maxLen)
  load_no_overhead,overhead,total_dt = swap_sched(vec_swap_selct,load_origin,vec_run,memLimit,
      "stick-to-limit",maxIdx,maxLen)
  return -(overhead)/1000000

# normalize the sorters
def compute_and_normalize_sorters(vec_swap):
  # pri, dto, dt pri_net computed.
  pri_list = []
  dto_list = []
  dt_list = []
  pri_net_list = []
  wdto_list = []
  for i in range(0, len(vec_swap)):
    pri_list.append(vec_swap[i].pri)
    dto_list.append(vec_swap[i].dto)
    dt_list.append(vec_swap[i].dt)
    pri_net_list.append(vec_swap[i].pri_net)
  pri_var = np.var(pri_list)
  pri_mean = np.mean(pri_list)
  dto_var = np.var(dto_list)
  dto_mean = np.mean(dto_list)
  dt_var = np.var(dt_list)
  dt_mean = np.mean(dt_list)
  pri_net_var = np.var(pri_net_list)
  pri_net_mean = np.mean(pri_net_list)
  # wdto
  for i in range(0, len(vec_swap)):
    itm = vec_swap[i]
    for j in range(itm.r_idx, itm.d_idx):
      itm.wdto+=load_origin[i]
    vec_swap[i] = itm
    wdto_list.append(itm.wdto)
  wdto_var = np.var(wdto_list)
  wdto_mean = np.mean(wdto_list)
  # sub_wdto
  vec_load = list(load_origin)
  vec_swap_temp = list(vec_swap)
  vec_swap = []
  sub_wdto_list = []
  # print "---------------------------------"
  while (len(vec_swap_temp) > 0):
    current_len = len(vec_swap_temp)
    # print "====="
    for i in range(0,current_len):
      itm = vec_swap_temp[i]
      itm.sub_wdto = 0
      for j in range(itm.r_idx,itm.d_idx):
        itm.sub_wdto+=vec_load[j+maxLen]
      vec_swap_temp[i] = itm
    vec_swap_temp.sort(key=lambda x: x.sub_wdto, reverse=True)

    # vec_swap_temp[0].sub_wdto = 1/vec_swap_temp[0].sub_wdto #TODO note it's 1/sub_wdto
    sub_wdto_list.append(vec_swap_temp[0].sub_wdto)
    # print vec_swap_temp[0].r_idx,vec_swap_temp[0].sub_wdto #TODO double print
    # print "b4 change "+str(vec_load[vec_swap_temp[0].r_idx+maxLen])
    load_update(vec_load,vec_swap_temp[0].r_idx,vec_swap_temp[0].d_idx,-1,vec_swap_temp[0].size,maxLen)
    # print "after chg " +str(vec_load[vec_swap_temp[0].r_idx+maxLen])
    vec_swap.append(vec_swap_temp[0])
    vec_swap_temp.remove(vec_swap_temp[0])
  sub_wdto_var = np.var(sub_wdto_list)
  sub_wdto_mean = np.mean(sub_wdto_list)
  # normalize
  for i in range(0,len(vec_swap)):
    vec_swap[i].pri = (vec_swap[i].pri-pri_mean)/np.sqrt(pri_var)
    vec_swap[i].dto = (vec_swap[i].dto-dto_mean)/np.sqrt(dto_var)
    vec_swap[i].dt = (vec_swap[i].dt-dt_mean)/np.sqrt(dt_var)
    vec_swap[i].pri_net = (vec_swap[i].pri_net-pri_net_mean)/np.sqrt(pri_net_var)
    vec_swap[i].wdto = (vec_swap[i].wdto-wdto_mean)/np.sqrt(wdto_var)
    # vec_swap[i].sub_wdto = (vec_swap[i].sub_wdto-sub_wdto_mean)/np.sqrt(sub_wdto_var)


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
compute_and_normalize_sorters(vec_swap) 

print "below is for BO ============="
ans_list = []
memLimit_list = range(280<<20,680<<20,10<<20)
for memLimit in memLimit_list:
  print "::::: memLimit "+str(memLimit>>20)
  bo = BayesianOptimization(target, {'a': (-1, 1),'b':(-1,1),'c':(-1,1),'d':(-1,1)})
  # bo.maximize(init_points=2, n_iter=0, acq='ucb', kappa=5)
  init_ans = max([target(1,0,0,0),target(0,1,0,0),target(0,0,1,0),target(0,0,0,1)])
  print init_ans
  if init_ans == 0:
    n =1
  else:
    n =20
  bo.explore({
               'a': [1,0,0,0],
               'b': [0,1,0,0],
               'c': [0,0,1,0],
               'd': [0,0,0,1]}, eager = True)
  ans = bo.maximize(init_points=0, n_iter=n, kappa=5)
  print "ans is "+str(ans)
  ans_list.append(ans)
print memLimit_list
print ans_list

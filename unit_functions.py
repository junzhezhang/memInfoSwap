import csv
import numpy as np


def full_list_to_full_load(vec_run_full):
  vec_load = []
  last_load = 0
  for itm in vec_run_full:
    if itm[1] == "Malloc":
      current_load = last_load + itm[3]
      last_load = current_load
      vec_load.append(current_load)
    elif itm[1] == "Free":
      current_load = last_load - itm[3]
      last_load = current_load
      vec_load.append(current_load)
    else:
      vec_load.append(last_load)
  return vec_load


def full_csv_blockInfo_to_full_list(fileName1):
  # full list from very biggining of the training.
  f2 = open(fileName1)
  rows = f2.read().splitlines()
  split_rows = []
  for row in rows:
    values = row.split(' ')
    split_rows.append([int(values[0]), values[1],values[2],int(values[3]),float(values[4])])
  return split_rows

def csv_blockInfo_to_list(fileName1,maxLen):
  # csv blockInfo 4-6 info to list, with t, exclude with smallest_block
  f2 = open(fileName1)
  rows = f2.read().splitlines()
  split_rows = []
  i = -maxLen
  time_remover = 0;
  for row in rows:
    values = row.split(' ')
    if i == -maxLen:
      time_remover = float(values[3])
    # if int(values[2]) >= smallest_block:
      #split_rows.append(values[0:-1]) # exclude last item, t
    split_rows.append([i, values[0],values[1],int(values[2]),float(values[3])-time_remover])
    i+=1
  return split_rows

def csv_load_to_list(fileName1):
  # csv load of 1-3 itr, to list of load in float. origin load.
  f2 = open(fileName1)
  rows = f2.read().splitlines()
  rows_float = []
  for row in rows:
    rows_float.append(float(row))
  return rows_float

def blockInfo_list_to_distinct_blocks(input_rows):
  # distinct block is list of list
  split_rows = list(input_rows)
  split_rows.sort(key = lambda x: x[2]) # sort in place, sort by ptr, then idx
  # print split_rows[0:3]
  # create blocks - new, should be no problem
  tempBlock = ''
  distinct_blocks = []
  current_block = []
  count = 0
  # print "no of rows in total: "+str(len(split_rows))
  for row in split_rows:
    if count == 0:
      current_block.append(row)
      count+=1
      tempBlock = row[2]
    else:
      if tempBlock == row[2]:
        if row[1] != 'Malloc':
          current_block.append(row)
          count+=1
        else:
          distinct_blocks.append(current_block)        
          current_block =[]
          current_block.append(row)
          count+=1
      else:
        distinct_blocks.append(current_block)
        current_block =[]      
        current_block.append(row)      
        count+=1
        tempBlock = row[2]
      if count == (len(split_rows)-1): # deal with last distinct block
        distinct_blocks.append(current_block) 
  # print "no of distinct blocks: "+str(len(distinct_blocks))
  sum_rows = 0
  for block in distinct_blocks:
    sum_rows+=len(block)
  # print "no of rows of all distinct blocks: "+str(sum_rows)
  return distinct_blocks

class SwapBlock:
  def __init__(self, ptr, size, r_idx, d_idx, r_t, d_t):
    self.ptr = ptr
    self.size = size
    self.r_idx = r_idx
    self.d_idx = d_idx
    self.r_t = r_t
    self.d_t = d_t
    self.dt = 0;
    self.dto = 0
    self.wdto = 0
    self.sub_wdto = 0
    self.pri = 0
    self.pri_net = 0
    self.bo = 0

    self.i1 = 0
    self.i1p = 0
    self.i2 = 0
    self.i2p = 0
    self.t1 = 0
    self.t2 = 0
    self.t1p = 0
    self.t2p = 0


def get_swappable_blocks(distinct_blocks,maxIdx,smallest_block):
  vec_swap =[]
  # i = 0
  for block in distinct_blocks:
    if (int(block[0][0]) <= maxIdx) and (int(block[-1][0]) >= maxIdx) and (block[0][3] >= smallest_block):
      last_row = block[0]
      for row in block:
        if (row != last_row) and int(last_row[0]) < maxIdx and int(row[0]) > maxIdx:
          # print "===================="+str(i)
          # print last_row
          # print row
          # i+=1
          # def __init__(self, ptr, size, r_idx, d_idx, r_t, d_t):
          tempSwapBlock = SwapBlock(row[2],row[3],last_row[0],row[0],last_row[4],row[4])
          tempSwapBlock.dto = tempSwapBlock.d_t - tempSwapBlock.r_t
          tempSwapBlock.pri = tempSwapBlock.dto*tempSwapBlock.size
          tempSwapBlock.dt = tempSwapBlock.dto - swap_out_dt(tempSwapBlock.size) 
          - swap_in_dt(tempSwapBlock.size)
          if tempSwapBlock.dt >= 0:
            tempSwapBlock.pri_net = tempSwapBlock.dt*tempSwapBlock.size
          else:
            tempSwapBlock.pri_net = tempSwapBlock.dt*1/tempSwapBlock.size

          vec_swap.append(tempSwapBlock)
        last_row = row
  return vec_swap

def swap_out_dt(size):
  ans = 0
  if (size==0):
    ans = 47200 
  else:
    ans = 0.0756 * size + 47200
  return ans;
def swap_in_dt(size):
  ans = 0
  if (size==0):
    ans = 9700
  else:
    ans = 0.0823 * size + 9700
  return ans

def load_over_limit(vec_load,memLimit,start_idx,end_idx,maxLen):
  # input: vec_load, memLimit, range [start_idx, end_idx]
  # return range overlimit [first_over_limit, first_below_limit)
  first_over_limit = start_idx
  first_below_limit = end_idx
  for i in range(start_idx+maxLen,end_idx+maxLen):
    if (vec_load[i] > memLimit):
      first_over_limit = i - maxLen
      break
  for i in range(end_idx+maxLen,first_over_limit+maxLen,-1):
    if (vec_load[i] > memLimit):
      first_below_limit = i - 1 - maxLen
      break
  if first_over_limit == start_idx:
    first_over_limit = -1
  if first_below_limit == end_idx:
    first_below_limit = -1
  return first_over_limit,first_below_limit

def load_update(updated_load,start_idx,end_idx,plusMinus,size,maxLen):
  # update [), pass by reference, no need return
  #updated_load = vec_load
  # print "------------------load update verify "
  # print updated_load[start_idx]
  for i in range(start_idx+maxLen,end_idx+maxLen):
    updated_load[i] = updated_load[i] + plusMinus*size
  # print updated_load[start_idx]


def load_peak(vec_load,maxLen):
  maxLoad = 0
  maxIdx = 0
  for i in range(maxLen,maxLen*2):
    if maxLoad <vec_load[i]:
      maxLoad = vec_load[i]
      maxIdx = i - maxLen
  return maxLoad, maxIdx

def swap_select(vec_swap,vec_load,memLimit,maxLen):
  load_updated = list(vec_load) ## NOTE: copy list without pass by reference
  SwapBlock_selected = []
  for i in range(0,len(vec_swap)):
    itm = vec_swap[i]
    load_update(load_updated,itm.r_idx,itm.d_idx,-1,itm.size,maxLen)
    SwapBlock_selected.append(itm)
    a,b = load_peak(load_updated,maxLen)
    if a <= memLimit:
      break
  return SwapBlock_selected,load_updated

def get_lowest_memLimit(vec_swap,vec_load,maxLen):
  load_updated = list(vec_load) ## NOTE: copy list without pass by reference
  lowest_memLimit, idx = load_peak(load_updated,maxLen)
  for i in range(0,len(vec_swap)):
    itm = vec_swap[i]
    load_update(load_updated,itm.r_idx,itm.d_idx,-1,itm.size,maxLen)
    a,b = load_peak(load_updated,maxLen)
    # print a
    if a < lowest_memLimit:
      lowest_memLimit = a

  return lowest_memLimit


def swap_sched(vec_swap_selct,load_origin,vec_run,memLimit,mode,maxIdx,maxLen):
# currently can dont return schedule, only return overhead
  total_out_dt = 0
  total_in_dt = 0
  overhead_out = 0
  overhead_in = 0
  load_updated = list(load_origin)
  if mode == "stick-to-limit":
    # swap-out
    # print "----------swap-out"
    vec_swap_selct.sort(key=lambda x: x.r_idx, reverse = False)
    for i in range(0, len(vec_swap_selct)):
      itm = vec_swap_selct[i]
      readyIdx = itm.r_idx
      if i>0:
        readyIdx = max(readyIdx,vec_swap_selct[i-1].i1p)
      itm.i1 = readyIdx
      itm.t1 = vec_run[readyIdx+maxLen][4]
      itm.t1p = itm.t1 + swap_out_dt(itm.size)
      total_out_dt+=swap_out_dt(itm.size)
      while (itm.t1p > vec_run[readyIdx+maxLen][4]):
        readyIdx+=1
      readyIdx = min(readyIdx,itm.d_idx-1)
      load_update(load_updated,readyIdx,itm.d_idx,-1,itm.size,maxLen)
      a, b = load_over_limit(load_updated,memLimit,0,maxLen,maxLen)
      if (a != -1 and a <= readyIdx):
        load_update(load_updated,a-1,readyIdx+1,-1,itm.size,maxLen)
        readyIdx = a - 1
      itm.i1p = readyIdx
      tempOverhead =  itm.t1p - vec_run[itm.i1p+maxLen][4]
      if tempOverhead > 0:
        overhead_out+=tempOverhead #TODO verify if correct or not
        # print itm.r_idx,itm.i1,itm.i1p,itm.size,tempOverhead
      vec_swap_selct[i] = itm
      # print itm.r_idx,itm.i1,itm.i1p,itm.size
    # swap-in
    # print "----------swap-in"
    vec_swap_selct.sort(key=lambda x: x.d_idx, reverse = True)
    for i in range(0,len(vec_swap_selct)):
      itm = vec_swap_selct[i]
      needIdx = itm.d_idx
      if (i > 0):
        needIdx = min(needIdx,vec_swap_selct[i-1].i2p)
      prepareTime = vec_run[needIdx+maxLen][4] - swap_in_dt(itm.size)
      total_in_dt+=swap_in_dt(itm.size)
      while(prepareTime<vec_run[needIdx][4]):
        needIdx-=1
      needIdx = max(needIdx,itm.r_idx)
      load_update(load_updated,needIdx,itm.d_idx,1,itm.size,maxLen)
      
      a, b = load_over_limit(load_updated,memLimit,0,maxLen,maxLen)
      if (b != -1 and b >= needIdx):
        load_update(load_updated,needIdx,b+1,-1,itm.size,maxLen)
        overhead_in+= vec_run[b+maxLen][4] - prepareTime
        # print vec_run[b+maxLen][4] - prepareTime
        # print str(vec_run[b+maxLen][4] - vec_run[readyIdx+maxLen][4])+"=========="
        # print swap_in_dt(itm.size)
        readyIdx = b  
      itm.i2p = needIdx
    
    # print "overhead out and in: "+str(overhead_out)+" "+str(overhead_in)+" "+str((overhead_out+overhead_in)/1000000)
    # print "swap out and in: "+str(total_out_dt)+" "+str(total_in_dt)+" "+str((total_out_dt+total_in_dt)/1000000)
    # print "one iteration is: "+str((vec_run[maxLen*2][4]-vec_run[maxLen][4])/1000000)
    # print "one iteration is: "+str((vec_run[maxLen][4]-vec_run[0][4])/1000000)
    # print "one iteration is: "+str((vec_run[maxLen*3-1][4]-vec_run[maxLen*2][4])/1000000)
    return load_updated,overhead_out+overhead_in,total_out_dt+total_in_dt

def overhead_from_sorted_block(vec_origin_swap,load_origin,vec_run,a,b,c,mode,maxLen,maxIdx):
  memLimit_list = []
  overhead_list = []
  swap_dt_list = []
  vec_swap = list(vec_origin_swap)
  vec_load = list(load_origin)
  if mode == "pri": vec_swap.sort(key=lambda x: x.pri, reverse=True)
  if mode == "dto": vec_swap.sort(key=lambda x: x.dto, reverse=True)
  if mode == "dt": vec_swap.sort(key=lambda x: x.dt, reverse=True)
  if mode == "pri_net": vec_swap.sort(key=lambda x: x.pri_net, reverse=True)
  if mode == "wdto":
      for i in range(0, len(vec_swap)):
        itm = vec_swap[i]
        for j in range(itm.r_idx, itm.d_idx):
          itm.wdto+=vec_load[i]
        vec_swap[i] = itm
      vec_swap.sort(key=lambda x: x.wdto, reverse = True)
  if mode == "sub-wdto": # O(n^3)
    vec_swap_temp = list(vec_swap)
    vec_swap = []
    while (len(vec_swap_temp) > 0):
      current_len = len(vec_swap_temp)
      for i in range(0,current_len):
        itm = vec_swap_temp[i]
        itm.sub_wdto = 0
        for j in range(itm.r_idx,itm.d_idx):
          itm.sub_wdto+=vec_load[j+maxLen]
        vec_swap_temp[i] = itm
      vec_swap_temp.sort(key=lambda x: x.sub_wdto, reverse=True)
      load_update(vec_load,vec_swap_temp[0].r_idx,vec_swap_temp[0].d_idx,-1,vec_swap_temp[0].size,maxLen)
      vec_swap.append(vec_swap_temp[0])
      vec_swap_temp.remove(vec_swap_temp[0])
    vec_swap.sort(key=lambda x: x.sub_wdto, reverse=True)   
  for memLimit in range(a,b,c):
    vec_swap_selct, load_updated = swap_select(vec_swap,load_origin,memLimit,maxLen)
    load_no_overhead,overhead,total_dt = swap_sched(vec_swap_selct,load_origin,vec_run,memLimit,
      "stick-to-limit",maxIdx,maxLen)
    # print mode+" bwhen memLimit is "+str(memLimit)+" overhead is "+str(overhead/1000000)
    memLimit_list.append(memLimit)
    overhead_list.append(overhead)
    swap_dt_list.append(total_dt)
  return overhead_list

# normalize the sorters
def compute_and_normalize_sorters(vec_swap,load_origin,maxLen):
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

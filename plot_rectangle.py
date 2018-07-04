import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from unit_functions import *
from random import shuffle


# reference https://stackoverflow.com/questions/14531346/how-to-add-a-text-into-a-rectangle 
# get rectangles
truePath ="/Users/junzhezhang/Downloads/offline-singa/"

smallest_block = 1<<20

fileName1 = truePath+"vec_block_fresh_vgg.csv"
fileName2 = truePath+"load_origin_vgg.csv"
maxLen = 3172
location = 6675
maxIdx = 1369
memLimit = 300

vec_run = csv_blockInfo_to_list(fileName1,maxLen)
load_origin = csv_load_to_list(fileName2)
distinct_blocks = blockInfo_list_to_distinct_blocks(vec_run)
print len(distinct_blocks)
new_list_distinct_blocks = []
count=0
size=0
size_list = []
x_bound = 0
y_bound = 0
for block in distinct_blocks:
  size_list.append(block[0][3])
  if ((2<<20)<block[0][3]<(20<<20) and block[0][0]>=0 and block[-1][0]<maxLen
    and (block[-1][0] -block[0][0]) >=10):
    
    new_list_distinct_blocks.append([block[0][0],block[-1][0],block[0][3]])
    count+=1
    size+=block[0][3]
print count
print str(size>>20) + " MB"
print new_list_distinct_blocks[0]


new_list_distinct_blocks.sort(key=lambda x: x[0], reverse=False)
x_shift = -new_list_distinct_blocks[0][0]
y_shift = 0

shuffle(new_list_distinct_blocks)
rectangles = []
count =0
for itm in new_list_distinct_blocks:
  rectangles.append(mpatch.Rectangle((itm[0]+x_shift,y_shift),itm[1]-itm[0],itm[2]>>20))
  y_shift += ((itm[2]>>20) +1)
  x_bound = max(x_bound,x_shift+itm[1])
  y_bound = max(y_bound,y_shift)
  count+=1
  if count>15:
    break


fig, ax = plt.subplots()

# rectangles = [mpatch.Rectangle((2,2), 8, 2), mpatch.Rectangle((4,6), 6, 6)]

for r in rectangles:
  ax.add_artist(r)

ax.set_xlim((0, x_bound))
ax.set_ylim((0, y_bound))
plt.xlabel("variable lifetime - operation index",fontsize =16)
plt.ylabel("size in MB",fontsize =16)
# ax.set_aspect('equal')
plt.show()
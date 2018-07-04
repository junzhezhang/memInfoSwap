import numpy as np
import random


print "hello"

random.seed(0)

images = np.empty((100, 3, 32, 32), dtype=np.uint8)
print type(images)
print images.shape

images2 = np.random.randn(10,3)
print images2

images3 = np.random.randint(0,255,(100,3,32,32),np.int64)
print images3.shape
print images3[1,1,1,1]
# print images3
images3 = np.array(images3,dtype =np.float32)

# shape and type of y
# (100, 1)
# <type 'numpy.ndarray'>

y =np.ones((10,1))
print y
print y.shape

y2 = np.random.randint(0,255,(10,),np.int64)
print y2.shape
print y2
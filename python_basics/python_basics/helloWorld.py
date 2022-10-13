# Comment: This is a fairly simple Python script
import numpy as np
neighbor = [0]*8
neighbor[0] = 0 
neighbor[1] = 0 
neighbor[2] = 1 
neighbor[3] = 1 
neighbor[4] = 1 
neighbor[5] = 0 
neighbor[6] = 1 
neighbor[7] = 1

test_list = [1, 0, 0, 1, 1, 0]
res = int("".join(str(x) for x in neighbor), 2)
print(2+5*5)

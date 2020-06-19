import sys
import math
import time
import datetime

print("wat is sys.maxsize ", sys.maxsize)
for i in range(1,sys.maxsize): # sys.maxsize gives maximum pointer value of machine, the width of the address register: the number of different memory locations that the processor can physically refer to. –
    key = str(i) # key+1 toevoegen loop
    d = {}  # aanmaken dictionary
    d[key] = key
    if math.log2(i) % 1 == 0:
        t1_start = time.perf_counter()
            #
        value = d[key]
            #
        t1_stop = time.perf_counter()
        elapsed_time = t1_stop - t1_start
        print("current key is ", key, " before placing key time is : ", t1_start," after placing key time is : ", t1_stop,  " & elapsed time is ", elapsed_time)
            

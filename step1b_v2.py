# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:32:39 2019

@author: newuser
"""
import math 
import numpy as np
from scipy.stats import binom


n=30000#template
P=4900#bits in a template
fp=0.10#FP for a single BF
e_over_P=0.16#Result of the experiments on the templates

##%%%%%%%%%%%%%%%%

prob_flip_level0=0.995; #Close to 1

l_0=math.log(1-prob_flip_level0)/math.log(1-e_over_P) #useful

N_init=math.ceil(P/l_0)

m=(math.log(fp)/math.log(0.6185))*n

k=math.ceil((m*math.log(2))/n)

pbf=1-(fp**(1/k))

p_oneBF=(1-pbf)**k

fp_HBF=fp-0.0001;#Worst case scenario: fp_HBF is only slightly better than fp

tt=1

N_list=(list (range (N_init, (N_init+11) ) ) )

X=np.zeros((1,len(N_list)))

X=[]
for i in range(len(N_list)):
    temp_N=N_list[i]
    temp_x=binom.ppf((1-fp_HBF), N_list[i], p_oneBF)
    X.append(temp_x)
 
#finding the min N
index_of_minX=[]
minX=min(X)
for i in range(len(X)):
    temp_x=X[i]
    if temp_x==minX:
        index_of_minX.append(i+1)

N_final=N_init+max(index_of_minX)       #useful
N_t=min(X) #Threshold   
   
N=N_final-N_init-1
#finding d and w
if (N > 0) and (N < (N_init/2)):
    d=3
    w=math.ceil(math.sqrt(P/(l_0)))
elif (N > 0) and (N > (N_init/2)):
    d=4
    w=math.ceil(math.sqrt(P/(l_0)))
    test=(l_0*N/P)-((1-((1/w)^(d-2)))/(w-1))
    while (test > 0):
        w=w+1
else:
    d=2



"""
File:   step4_analysis on HBF results to take final decision.py
Author: Sumaiya Shomaji
Date:   9/22/2019
Desc:   this code is enrolling data into HBF, performing query on tets data, and finally taking decsion whether a query person is a member of the databse or not
"""
#*************************************************************step1a: importing the enrollmnet and query templates here****************************
#reading the function titled as "step1a_load_enrollment_and_query_data" which load templates from people who will be enrolled and templates from people who will be queried 
import step1a_load_enrollment_and_query_data

#importing IDs and templates for people who are going to be Enrolled
textfile_name_of_people_for_enrollment='enrol_id_PinellasFRGC.txt'
textfile_template_people_for_enrollment='enrol_template_PinellasFRGC.txt'
enrollment_id,enrollment_data=step1a_load_enrollment_and_query_data.template_enrollment_data(textfile_name_of_people_for_enrollment,textfile_template_people_for_enrollment)

#importing IDs and templates for people who are going to be Queried
textfile_name_of_people_for_query='query_id_PinellasFRGC.txt'
textfile_template_people_for_query='query_template_PinellasFRGC.txt'
query_id,query_data=step1a_load_enrollment_and_query_data.template_query_data(textfile_name_of_people_for_query,textfile_template_people_for_query)


#************************************************************step1b: importing the parameters needed for designing Hierarchical Bloom Filter here****************************
#requiredSizeOfBF1,requiredHashNo1,total_level,d1_l,d1_BFs: thes eparametrs are dteremined from script step:1b
#run 1 b and find: m, k, d, [ l_0,l_0*w,len(full_template) ], and minX
# then use the values of thsoe paramters like these:
"""
requiredSizeOfBF1 = m
requiredHashNo1 = k
total_level = d
d1_l = [ l_0, l_0*w,len(full_template) ]
d1_BFs = [len(full template)/ l_0, len(fill template)/ l_0*w, len(full template)/ 1]
threshold = minX
"""

# determining paramteres for BF: n1, requiredSizeOfBF1, requiredHashNo1
n1=len(enrollment_data)
requiredSizeOfBF1=140530#m
requiredHashNo1=4#k

# determining paramteres for HBF: how mnay levels (total_level), # of BFs in each level (d1_BF), # of bits in each level (d1_BF)
total_level=3#set this first
d1=list(range(0,total_level))
d1_l=[32, 32*13, 4900]#num_of_bits_from_each_template_in_each_layer_for_a_BloomFilter
d1_BFs=[153, 11 , 1 ]#_num_of_BFs_in_each_layer


#***********************************************************step2: enrolling the "enrollment_data" into Hierarchical Bloom Filter here****************************
import csv
import numpy as np
import hashlib
import random
import fnv
import math

n=len(enrollment_data)
#preparing for hashing
check_hash_fnv_raw=[]
check_hash_fnv_bin_32bit=[]
check_xor_int=[]
check_fnv_modulus=[]
check_masking=[]
check_sha256_modulus=[]

#some more items that I will need
bits_to_take=math.floor(math.log2(requiredSizeOfBF1))
mask_bin=bits_to_take*'1'
mask_int=int(mask_bin,2)
key=[]  #we need to do hashing of a template "k" times. To hash k times, we use k no. of differents keys. Initializing key here.
key1= np.arange(1, requiredHashNo1+1, dtype=np.int)
for i in range (len(key1)):
    pp=bin(key1[i])[2:].zfill(8)
    key.append(pp)


#************Bloom Filter Design Starts from Here********************
#for i_layers in range(len(d)):
#    temp_level_ID = d[i_layers]
#    num_of_BFs_in_that_layer=d_BFs[i_layers]

#    for i_BFs_in_each_layer in range (num_of_BFs_in_that_layer):
#        biometric_template_enrolling_set_segmented=HBF_enrollingset_v1[i_layers][i_BFs_in_each_layer]
#        print(i_BFs_in_each_layer)
hash_output_enrolling=np.zeros((len(enrollment_data),len(key))).astype('int')
for i in range(len(key)):
    temp1_key=bytes(str(key[i]),'utf-8')#this is making each of the keys in --> b'key' type format 
    for j in range (len(enrollment_data)):
        temp2_msg_biometric_template=bytes(enrollment_data[j],'utf-8')#need to make b'message' too! that is why doing this
        hash1_biometric_template_enrol= hashlib.sha256(temp2_msg_biometric_template +temp1_key).hexdigest()
        temp3_msg_biometric_template=bytes(hash1_biometric_template_enrol,'utf-8')
        hash_fnv_raw=fnv.hash(temp3_msg_biometric_template, bits=32)#doing fnv#result comes in decimal#REMEMBER: this is not the FINAL HASH OUTPUT whcih gives unique result
        check_hash_fnv_raw.append(hash_fnv_raw)
        hash_fnv_bin_32bit="{0:32b}".format(hash_fnv_raw)#converting decimal result into 32 bit binary
        check_hash_fnv_bin_32bit.append(hash_fnv_bin_32bit)
        msg_int=int(hash_fnv_bin_32bit, 2)#converting 32bit binary fnv hash output into integer number
        msg_bitshift=msg_int>>bits_to_take#doing bitshift for x no. of bits (it is rule)
        xor_int= (msg_bitshift ^ msg_int)#doing xor
        check_xor_int.append(xor_int)
        masking=xor_int & mask_int#this is the FINAL HASH OUTPUT whcih gives unique result
        check_masking.append(masking)
        hash_output_enrolling[j][i]= masking
 
fnv_output_listOflist = hash_output_enrolling.tolist()
#now let's put the values in bf

fnv_output = sum(fnv_output_listOflist, [])

bins_list = list(range(0, requiredSizeOfBF1-1))

#
#
#import numpy as np
#import matplotlib.pyplot as plt
#fig = plt.figure(figsize = (15,6))
#ax = plt.hist(fnv_output, bins = bins_list)
##plt.hist(fnv_output, bins = [np.arange(0, requiredSizeOfBF1-1, 3)])
#plt.show()
#
#
#import numpy as np
#import matplotlib.pyplot as plt
#fig = plt.figure(figsize = (15,6))
#ax = plt.hist(fnv_output, bins = bins_list)
##plt.hist(fnv_output, bins = [np.arange(0, requiredSizeOfBF1-1, 3)])
#plt.show()






import numpy as np
import pylab
import matplotlib.pyplot as plt
fig = plt.figure(figsize = (17,5))
ax = plt.hist(fnv_output, bins = bins_list)
plt.xlabel('FNV Hash output',fontsize = 15)
plt.ylabel('Counts',fontsize = 15)
plt.xticks(fontsize = 15) # work on current fig
plt.yticks(fontsize = 15) # work on current fig
plt.title('Histogram Plot of FNV Hash Output',fontsize = 17)
plt.grid(True)
pylab.ylim(0, 7)
plt.show()






#*******************************how to split the items in Counter
from collections import Counter
unique_people=Counter(fnv_output)
uniq_people=list(unique_people)  
counter_split=[unique_people.keys(), unique_people.values()]  
list_ids=list(counter_split[0])
list_frequencies=list(counter_split[1])






































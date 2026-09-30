"""
File:   step2_enrollment.py
Author: Sumaiya Shomaji
Date:   9/11/2019
Desc:   this code is enrolling the "enrollment data" in HBF
"""
import csv
import numpy as np
import hashlib
import random
import fnv
import math
def bloom_filter_enrolling(d,d_BFs,d_l,biometric_template_enrolling_set,n,requiredSizeOfBF,requiredHashNo):
    #**************************Creating an architecture for the enrollment data**************
    HBF_enrollingset_v1 = [[] for x in range(len(d))]#initializing an empty array where we will store segment-wise template for everybody
    for i in range(len(d)):#d=index of levels # if there are 3 levels in total, d = [0,1,2]
        temp_levelID=d[i]
        num_of_BFs_in_that_layer=d_BFs[i]
        HBF_enrollingset_v1[temp_levelID]=[[] for x in range(num_of_BFs_in_that_layer)]

    #**************from now on we are going to work with segments
    for i in range(len(d)):#this loop will run to the number of levels
        temp_levelID=d[i]
        num_of_BFs_in_that_layer=d_BFs[i]
        len_of_each_block_from_template=d_l[i]
        c1=0
        for j in range (num_of_BFs_in_that_layer):
            if j ==num_of_BFs_in_that_layer:
                temp_inputs= [ii[c1:] for ii in biometric_template_enrolling_set]
            else:
                temp_inputs= [ii[c1:c1+len_of_each_block_from_template] for ii in biometric_template_enrolling_set]#taking a segment from biometric template
                c1=c1+len_of_each_block_from_template
                HBF_enrollingset_v1[i][j]=temp_inputs


    HBF_Enrolled = [[] for x in range(len(d))]
    for i in range(len(d)):
        temp_levelID=d[i]
        num_of_BFs_in_that_layer=d_BFs[i]
        HBF_Enrolled[temp_levelID]=[[] for x in range(num_of_BFs_in_that_layer)]


    n=len(biometric_template_enrolling_set)
    #preparing for hashing
    check_hash_fnv_raw=[]
    check_hash_fnv_bin_32bit=[]
    check_xor_int=[]
    check_fnv_modulus=[]
    check_masking=[]
    check_sha256_modulus=[]

    #some more items that I will need
    bits_to_take=math.floor(math.log2(requiredSizeOfBF))
    mask_bin=bits_to_take*'1'
    mask_int=int(mask_bin,2)
    key=[]  #we need to do hashing of a template "k" times. To hash k times, we use k no. of differents keys. Initializing key here.
    key1= np.arange(1, requiredHashNo+1, dtype=int)
    for i in range (len(key1)):
        pp=bin(key1[i])[2:].zfill(8)
        key.append(pp)


    #************Bloom Filter Design Starts from Here********************
    for i_layers in range(len(d)):
        temp_level_ID = d[i_layers]
        num_of_BFs_in_that_layer=d_BFs[i_layers]

        for i_BFs_in_each_layer in range (num_of_BFs_in_that_layer):
            biometric_template_enrolling_set_segmented=HBF_enrollingset_v1[i_layers][i_BFs_in_each_layer]
            print(i_BFs_in_each_layer)
            hash_output_enrolling=np.zeros((len(biometric_template_enrolling_set_segmented),len(key))).astype('int')
            for i in range(len(key)):
                temp1_key=bytes(str(key[i]),'utf-8')#this is making each of the keys in --> b'key' type format 
                for j in range (len(biometric_template_enrolling_set_segmented)):
                    temp2_msg_biometric_template=bytes(biometric_template_enrolling_set_segmented[j],'utf-8')#need to make b'message' too! that is why doing this
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
           
            #now let's put the values in bf
            bf=np.zeros(requiredSizeOfBF)#initializing an individual BF
            for jj in range(len( hash_output_enrolling)):
                for ii in range(len( hash_output_enrolling[0])):
                    bf[hash_output_enrolling[jj][ii]]=1#assign hash outputs in bf
            bf_enrolled= bf.astype("int") 

            HBF_Enrolled[i_layers] [i_BFs_in_each_layer]=bf_enrolled
    return (HBF_Enrolled) 


    

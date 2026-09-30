"""
File:   step3_query_perform.py
Author: Sumaiya Shomaji
Date:   9/11/2019
Desc:   this code is loading the HBF which is filled with enrollment people, and then performing membership query on the "query data" to check whether the query people are in HBF or not
"""
import csv
import numpy as np
import hashlib
import random
import fnv
import math
def bloom_filter_querying(HBF_Enrolled, Query_data,d,d_BFs,d_l,n,requiredSizeOfBF,requiredHashNo):

    #**************************Creating an architecture for the tetsing adtaset and outputs**************
    HBF_queryingset_v1 = [[] for x in range(len(d))]#initializing an empty array where we will store segment-wise template for everybody from the "query data" set
    for i in range(len(d)):#d=index of levels # if there are 3 levels in total, d = [0,1,2]
        temp_levelID=d[i]
        num_of_BFs_in_that_layer=d_BFs[i]
        HBF_queryingset_v1[temp_levelID]=[[] for x in range(num_of_BFs_in_that_layer)]

    #**************from now on we are going to work with segments
    for i in range(len(d)):
        temp_levelID=d[i]
        num_of_BFs_in_that_layer=d_BFs[i]
        len_of_each_block_from_template=d_l[i]
        c1=0
        for j in range (num_of_BFs_in_that_layer):
            if j ==num_of_BFs_in_that_layer:
                temp_inputs= [ii[c1:] for ii in Query_data]
            else:
                temp_inputs= [ii[c1:c1+len_of_each_block_from_template] for ii in Query_data]
                c1=c1+len_of_each_block_from_template
                HBF_queryingset_v1[i][j]=temp_inputs

    #preparing another item:HBF_levelwise_result : this will be the OutpuT file !!!
    HBF_levelwise_result = [[] for x in range(len(Query_data))]# this is the output #this tells us at each layer, how many BFs authenticated a query person
    for i in range(len(Query_data)):
        num_of_layer=len(d)
        HBF_levelwise_result[i]=[[] for x in range(num_of_layer)]
        
    #some more items that I will need
    bits_to_take=math.floor(math.log2(requiredSizeOfBF))
    mask_bin=bits_to_take*'1'
    mask_int=int(mask_bin,2)
    key=[]  #we need to do hashing of a template "k" times. To hash k times, we use k no. of differents keys. Initializing key here.
    key1= np.arange(1, requiredHashNo+1, dtype=int)
    for i in range (len(key1)):
        pp=bin(key1[i])[2:].zfill(8)
        key.append(pp)


    #************Bloom Filter querying Design Starts from Here********************
    for i_layers in range(len(d)):
        temp_level_ID = d[i_layers]
        num_of_BFs_in_that_layer=d_BFs[i_layers]

        for i_BFs_in_each_layer in range (num_of_BFs_in_that_layer):#dhori level = 3, tahole BF = 2ta
            querying_set_segmented=HBF_queryingset_v1[i_layers][i_BFs_in_each_layer]
            print(i_BFs_in_each_layer)
     #*********querying set
            hash_output_querying=np.zeros((len(querying_set_segmented),len(key))).astype('int')          
            for i in range(len(key)):
                temp1_key=bytes(str(key[i]),'utf-8')#this is making each of the keys in --> b'key' type format 
                for j in range (len(querying_set_segmented)):
                    temp2_biometric_template=bytes(querying_set_segmented[j],'utf-8')# i need to make b'key' too! that is why doing this
                    hash1_biometric_template_query=hashlib.sha256(temp2_biometric_template +temp1_key).hexdigest()
                    temp3_query=bytes(str(hash1_biometric_template_query),'utf-8')
                    hash_fnv_raw_query=fnv.hash(temp3_query, bits=32)#doing fnv#result comes in decimal
                    hash_fnv_bin_32bit_query="{0:32b}".format(hash_fnv_raw_query)#converting decimal result into 32 bit binary
                    msg_int_query=int(hash_fnv_bin_32bit_query, 2)#converting 32bit binary fnv hash output into integer number
                    msg_bitshift_query=msg_int_query>>bits_to_take#doing bitshift for x no. of bits (it is rule)
                    xor_int_query= (msg_bitshift_query ^ msg_int_query)#doing xor
                    masking_query=xor_int_query & mask_int
                    hash_output_querying[j][i]= masking_query
                    
                  
            #*************---->>>>>part3: comparing results and finding whetehr the query is on the list or not<<<----********
            comparison_matrix_template=np.zeros((len(hash_output_querying),len((hash_output_querying)[0]))).astype('int')
            for ii in range (len(comparison_matrix_template)):#person id in querying set
                for jj in range (len((comparison_matrix_template)[0])):#each col or hash output 
                    if HBF_Enrolled[i_layers][i_BFs_in_each_layer][hash_output_querying[ii][jj]]==1:
                        rsl_template=1
                        comparison_matrix_template[ii][jj]=rsl_template
                    else:
                        rsl_template=0
                        comparison_matrix_template[ii][jj]=rsl_template
            
            #*******
            decision_matrix_integer_template=np.zeros(len(comparison_matrix_template)).astype('int')
            
            for iii in range (len(comparison_matrix_template)):
                sum_template=0
                for jjj in range (len((comparison_matrix_template)[0])):
                    sum_template=sum_template+comparison_matrix_template[iii][jjj]
                decision_matrix_integer_template[iii]=sum_template
            
                    
            #*******
            decision_string_template=[]
            for iiii in range (len(comparison_matrix_template)):
                #print("i  value is  %s \n" %i)
                if decision_matrix_integer_template[iiii]==len(comparison_matrix_template[0]):
                    ans_template='Authenticated'
                    decision_string_template.append(ans_template)
                   
                else:
                    ans_template='Not Found'
                    decision_string_template.append(ans_template)   
            
            #*********counter for counting how many times it is authenticated
            for iiiii in range(len(decision_string_template)):
                person_i_am_talking_about=iiiii
                he_got_matched_or_not=decision_string_template[iiiii]
                HBF_levelwise_result[person_i_am_talking_about][i_layers].append(he_got_matched_or_not)
                

    return (HBF_levelwise_result)



    
    
    
    
    
    
    
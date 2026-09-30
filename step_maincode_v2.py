"""
File:   step4_analysis on HBF results to take final decision.py
Author: Sumaiya Shomaji
Date:   9/22/2019
Desc:   this code is enrolling data into HBF, performing query on tets data, and finally taking decsion whether a query person is a member of the databse or not
"""
#*************************************************************step1a: importing the enrollmnet and query templates here****************************
#reading the function titled as "step1a_load_enrollment_and_query_data" which load templates from people who will be enrolled and templates from people who will be queried 
import step1a_load_enrollment_and_query_data
import math
import numpy as np
#importing IDs and templates for people who are going to be Enrolled
textfile_name_of_people_for_enrollment='enrol_id_PinellasFRGC.txt'
textfile_template_people_for_enrollment='enrol_template_PinellasFRGC.txt'
enrollment_id,enrollment_data=step1a_load_enrollment_and_query_data.template_enrollment_data(textfile_name_of_people_for_enrollment,textfile_template_people_for_enrollment)

#importing IDs and templates for people who are going to be Queried
textfile_name_of_people_for_query='query_id_PinellasFRGC.txt'
textfile_template_people_for_query='query_template_PinellasFRGC.txt'
query_id,query_data=step1a_load_enrollment_and_query_data.template_query_data(textfile_name_of_people_for_query,textfile_template_people_for_query)


#************************************************************step1b: importing the parameters needed for designing Hierarchical Bloom Filter here****************************
#import step1b_load_parameters_for_designing_HBF

# determining paramteres for BF: n1, requiredSizeOfBF1, requiredHashNo1
n1=len(enrollment_data)
requiredSizeOfBF1=140530#m
requiredHashNo1=4#k

# determining paramteres for HBF: how mnay levels (total_level), # of BFs in each level (d1_BF), # of bits in each level (d1_BF)
total_level=3#set this first
d1=list(range(0,total_level))
d1_l=[32, 32*13, 4900]#num_of_bits_from_each_template_in_each_layer_for_a_BloomFilter
d1_BFs=[153, 11 , 1 ]#_num_of_BFs_in_each_layer


#***

n=len(enrollment_data)#template
P=4900#bits in a template
fp=0.10#FP for a single BF
e_over_P=0.16#Result of the experiments on the templates

##%%%%%%%%%%%%%%%%

prob_flip_level0=0.995; #Close to 1

l_0=math.log(1-prob_flip_level0)/math.log(1-e_over_P)

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

N_final=N_init+max(index_of_minX)       
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



#***























#***********************************************************step2: enrolling the "enrollment_data" into Hierarchical Bloom Filter here****************************
#reading the function titled as "bloom_filter_enrolling" which load peforms enrollment of the people called "enrllment data"
import step2_enrollment

#enrolling the"people to be enrolled" in HBF
HBF_enrolled=step2_enrollment.bloom_filter_enrolling(d1,d1_BFs,d1_l,enrollment_data,n1,requiredSizeOfBF1,requiredHashNo1)


#********************************************************step3: performing query on the "query_data" on the Hierarchical Bloom Filter which was filled with enrolled people in previous step****************************
#reading the function titled as "bloom_filter_enrolling" which load peforms enrollment of the people called "enrllment data"
import step3_query_perform

#querying the"people to be queried for membership check" in HBF just finished ennrolling the "enrolled_data"
HBF_levelwise_result1=step3_query_perform.bloom_filter_querying(HBF_enrolled, query_data,d1,d1_BFs,d1_l,n1,requiredSizeOfBF1,requiredHashNo1)


#*******************************************************step4: making final decison about every query person whether he is a member of the databse (= HBF) or not***********************
# this code need two parmatres:
#1. the level wise results from HBF's query which is "HBF_levelwise_result1"
#2. threshold with which we will compare the no. of bfs that that are authentication a query data
#"no. of bfs that that are authenticating a query data" will be calculated from "HBF_levelwise_result1"

from collections import Counter
import matplotlib.pyplot as plt

#*****************************calculating "no. of bfs that that are authenticating a query data" for all the query people*******************

#reading oupputs from step3:query
HBF_levelwise_result2= HBF_levelwise_result1.copy()  
   
result_from_in_165BFs=[] #initializing a list where we will store the no. of acceptance by BFs out of total BFs for every query person 
for i in range(len(HBF_levelwise_result2)):
    temp_QueryPersonID=i
    temp_result_for_thatID_from_allBFs_of_all_layer=HBF_levelwise_result2[i]
    flattened_result_for_that_person=[item for sublist in temp_result_for_thatID_from_allBFs_of_all_layer for item in sublist]
    counting_no_of_total_authetication=flattened_result_for_that_person.count('Authenticated')
    result_from_in_165BFs.append(counting_no_of_total_authetication)



#********************************************************************final decsion making***********************************
threshold =21
for i in range(len(query_data)):
    temp_frequency_of_bfs_autheticating_a_querydata=result_from_in_165BFs[i]
    if temp_frequency_of_bfs_autheticating_a_querydata>threshold:
        print ("Query Person with index "+ str(i)+" is a Member")
    else:
        print ("Query Person with index "+ str(i)+" is a Not a Member")
        
        
#plot showing the no. of BFs authenticatig a query person
y = result_from_in_165BFs
x=list(range(0,len(query_data)))

# plot the data
fig = plt.figure(figsize = (6,4))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('No. of Bloom Filters,', fontsize = 13)
ax.set_ylabel('Frequency of Individuals', fontsize = 13)
ax.set_title('Out of 165 BFs, how many authenticated a query person',fontsize = 15)
plt.xticks(fontsize = 13)
plt.yticks(fontsize = 13) 
plt.plot(x,result_from_in_165BFs)
plt.show()

#*******what this code is doing?
#Ans: this code is doing 2 things:
#step1a) loading input data for enrollment and query data for memebrship check in the HBF (data = quantized biomeric templates) 
#step1b) then based on the size of input data,  it determines the parameter of the Hierachical Bloom Filter
"""
File:   step1_provide_input_biometric_template.py
Author: Sumaiya Shomaji
Date:   9/11/2019
Desc:   this code is doing 2 things:
step1a) loading input data for enrollment and query data for memebrship check in the HBF (data = quantized biomeric templates) 
#step1b) then based on the size of input data,  it determines the parameter of the Hierachical Bloom Filter

    
"""


""" =======================  Import dependencies ========================== """

import csv
import numpy as np
import hashlib
import random
import fnv
import math
import json

#*****************************************step1a: Reading enrollment and query data*******************************
def template_enrollment_data(Textfile_name_of_people_for_enrollment,Textfile_template_people_for_enrollment):
    '''template_enrollment_data(list_name_of_the_people,list_template_of_the_people): importing the text file containing all indivdiuals name and file containing their biometric templates. These are the people who will be enrolled in a HBF''' 
    # reading IDs
    with open(Textfile_name_of_people_for_enrollment, 'r') as filehandle:  
        Enrollment_id = json.load(filehandle)
    # reading templates
    with open(Textfile_template_people_for_enrollment, 'r') as filehandle:  
        Enrollment_data = json.load(filehandle)
        
    return Enrollment_id,Enrollment_data

def template_query_data(Textfile_name_of_people_for_query,Textfile_template_people_for_query):
    '''template_query_data(list_name_of_the_people,list_template_of_the_people): importing the text file containing all indivdiuals name and file containing their biometric templates. These are the people who will be queried in a HBF''' 
    # reading IDs
    with open(Textfile_name_of_people_for_query, 'r') as filehandle:  
        Query_id = json.load(filehandle)
    # reading templates
    with open(Textfile_template_people_for_query, 'r') as filehandle:  
        Query_data = json.load(filehandle)

    return Query_id,Query_data



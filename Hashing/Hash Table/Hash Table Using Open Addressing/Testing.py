# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 22:02:15 2019

@author: Yuvraj
"""

# This Testing.py is just for testing purpose
# you just have to specify number of test cases and no of element to insert in each test case

import OpenAddressing as ht
from random import randrange, getrandbits
import time
    
############### All Below functions are just for testing purposes #############

def __add_testing__(h,key, value): # I use this add function so that it can return the number of probs 
    index = h.__getIndex__(key)    # took to insert the key
    i=1
    if(index == -1):
        flag = True
        while(flag):
            index = h._HashTable__quad_probing_(key,i)
            if(h._hashTable_[index][0] != None): 
                i += 1
                continue
            flag = False
    h._hashTable_[index][0] = ht.Node(key,value)
    h._hashTable_[index][1] = False
    h._occupied_ += 1
    h._alpha_ = h._occupied_ / h._size_
    if(h._alpha_ > h._alphaMax_):
        h.__update__(2)
    return i


def getRandomHashTable(path,no_of_elements):
    h = ht.HashTable(alphaMax=0.5) # Here alphaMax works as loadFactor
    s = time.time()
    probs = []
    i = 0
    while(i<no_of_elements):
#        print("ittr: "+str(i))
        no_of_bits = randrange(8,64)
        k, v = getrandbits(no_of_bits),getrandbits(8)
        probs.append(__add_testing__(h,k,v))
        i = len(h)
    e = time.time()
    f=open(path,'a')
    f.write("Adding: ,"+str(len(h))+", took ,"+str(e - s)+", sec\n")
    f.close()
    return h, probs
    
# =============================================================================

def removeHashTableRandomly(path,h):
    s = time.time()
    totalRemove = 0
    i = 0
    for k,v in h:
        i += 1
 #       print("Itter:",i)
        delete = getrandbits(1)
        if(delete == 1):
            totalRemove += 1
            del h[k]
    e = time.time()
    f=open(path,'a')
    f.write("Removal of: ,"+str(totalRemove)+", took ,"+str(e - s)+", sec\n")
    f.close()
            
# =============================================================================
 
def speedCheck(path,h):
    s = time.time()
    for k,v in h:
        t = h[k]
    e = time.time()
    f=open(path,'a')
    f.write("Serching:, "+str(len(h))+", took ,"+str(e - s)+", sec\n")
    f.close()

# =============================================================================

def createLogGetProb(path,test_case,no_element_per_test_case):
    f=open(path,'w')
    f.close()
    probs = []
    for i in range(test_case):
        print("Create Log Itter:",i,"of: ",test_case)
        h,p = getRandomHashTable(path,no_element_per_test_case)
        probs.append(p)
        speedCheck(path,h)
        removeHashTableRandomly(path,h)
    return probs

# =============================================================================

def testing(path):
    f = open(path,'r')
    s = f.read()
    s = s.split('\n')
    for i in range(len(s)):
        s[i] = s[i].split(',')
    s.pop()
    add,search,delete = [],[],[]
    count = 0
    for i in range(len(s)):
    	if(count==3): count = 0
    	if(count == 0): add.append(int(s[i][1]))
    	if(count == 1): search.append(int(s[i][1]))
    	if(count == 2): delete.append(int(s[i][1]))
    	count+=1
    
    add_t,search_t,delete_t = [],[],[]
    count = 0
    for i in range(len(s)):
    	if(count==3): count = 0
    	if(count == 0): add_t.append(float(s[i][3]))
    	if(count == 1): search_t.append(float(s[i][3]))
    	if(count == 2): delete_t.append(float(s[i][3]))
    	count+=1
    
    add = [int(i) for i in add]
    search = [int(i) for i in search]
    delete = [int(i) for i in delete]
    
    total_add = sum(add)
    total_search = sum(search)
    total_delete = sum(delete)
    
    total_add_time = sum(add_t)
    total_search_time = sum(search_t)
    total_delete_time = sum(delete_t)
    #print(total_add,total_add_time,total_delete,total_delete_time,total_search,total_search_time)
    print("Average Time spend per delete:",total_delete_time/total_delete," seconds")
    print("Average Time spend per insert ",total_add_time/total_add," seconds")
    print("Average Time spend per lookup :",total_search_time/total_search, "seconds")

###############################################################################
    
def run(path,test_case,no_element_per_test_case):
    probs = createLogGetProb(path,test_case,no_element_per_test_case)
    avg_list = []
    for i in range(len(probs)):
        avg_list.append(sum(probs[i])/len(probs[i]))    
    avg = sum(avg_list)/len(avg_list)
    mx = 0
    for i in range(len(probs)):
        mx2 = max(probs[i])
        if(mx2>mx):mx = mx2
    
    print("""
    These results get from """,test_case,""" test cases:
    each test case: insert """,no_element_per_test_case,"""elements
    And search for each and every element
    And randomly deleting nodes
    """)
    
    print("Acc to our test, OpenAddressing on average Took :",avg," probs")
    print("In our:",test_case," * ", no_element_per_test_case," Inserts maximum prob taken is:",mx)
    
    testing(path)

###############################################################################
    
path = 'C:\\Users\\Yuvraj\\Desktop\\py\\OpenAddressing\\log2.log'

test_case = 100
no_element_per_test_case = 1000000

start_time = time.time()
run(path,test_case,no_element_per_test_case)
print("Whole Testing took:", time.time() - start_time," sec")
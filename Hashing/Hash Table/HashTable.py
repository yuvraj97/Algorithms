# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 06:29:00 2019

@author: Yuvraj
"""

# If you wanna use numpy insted of list then here are only 2 difference
# Just uncomment line number 11,23,24,104,105 and comment line number 19 and 100

# import numpy as np
from lib.GenerateRandomPrime import generatePrimeNumber
from lib.LinkedList import LinkedList
from random import randrange

class HashTable():
    def __init__(self, size = 16, alphaMax = 0.5, alphaLowest = 0.25):
        self._size_ = size    # size define the size of the hash table
        self._hashTable_ = [LinkedList() for i in range(self._size_)]
        
        # If you wanna use Numpy insted of list then
        # Uncomment 2 lines below and comment the just above one
        # self._hashTable_ = np.empty(self._size_,dtype=LinkedList)
        # for i in range(self._size_):self._hashTable_[i] = LinkedList()
        
        self._occupied_ = 0   # occupied will keep track of how many of nodes are utilized
        # alpha define the current utilization of hashTable
        self._alpha_ = self._occupied_ / self._size_
        # alphaMax define that when did the size of hashTable doubles 0.5 mean when the hashtable is filled 50% size of hashTable doubles
        self._alphaMax_ = alphaMax
        # alphaLowest define that when did the size of hashTable reduces to half
        # 0.25 mean when the hashtable is left 25% of the size then size of hashTable reduces to half
        self._alphaLowest_ = alphaLowest
        # rand_a is used in multiplicationHash() is you wanna use multiplicationHash() insted of universalHashing() then uncomment it
        # self.rand_a = randrange(self._size_//2,self._size_) | 1   # it's for multiplicationHash, | is just to confirm that rand_a is odd
        # This is for Universal Hashes here our p can't exceed the word limit i.e. for a 64 bit architecture prime can't exceed 64 bit
        bitLength = self._size_.bit_length() + 1
        self._prime_ = generatePrimeNumber(bitLength) # primr is used by the hash function universalHashing()
        self._uni_a_ = randrange(0,self._prime_ - 1)    # uni_a and uni_b are used by the hash function universalHashing()
        self._uni_b_ = randrange(0,self._prime_ - 1)

# =============================================================================

    # Usage len(h) ; h:hashTable object and len(h) will return number of key, value pair inserted
    def __len__(self):
        return self._occupied_

# =============================================================================
    
    # Usage h[key] ; it will return value associated with key
    def __getitem__(self,key):
        index_i = self.__universalHash__(key)
        ith_linkedList = self._hashTable_[index_i]
        node = ith_linkedList.find(key)
        if(node == None):
            return None
        return node.value
    
# =============================================================================
    
    # Usage h[key] = value ; it will add a key, value pair in the hash table with given key, pair
    def __setitem__(self,key,value):
        self.__add__(key, value)

# =============================================================================

    # Usage del h[key] ; it will delete the key, value pair associated with the specified key
    def __delitem__(self,key):
        self.__remove__(key)

# =============================================================================
    
    # Usage:
    # for key,value in hashTable:
    #    operation_on_those_key_value_pair(key,value)
    def __iter__(self):
        for ith_linkedList in self._hashTable_:
            for i in ith_linkedList:
                yield i

# =============================================================================
    
    # Usage:
    # key in hashTable
    # It will return either True (if key is in hashTable) or False (if key is not in hashTable)
    def __contains__(self,key):
        isExist = self.__find__(key)
        if(isExist == None):
            return False
        return True

# =============================================================================
    
    # This function is used for extend or reduce the hash table
    # Depending on updateFactor: if its 2 then we will double the size of our hash table and rehash all nodes
    # And is updateFactor is 1/2 then we will reduce the size of our hash table and rehash all nodes
    def __update__(self,updateFactor):
        hashTableCopy = self._hashTable_          # updateFactor = 1/2 => reduce hashTable to half the size
        self._size_ = int(self._size_*updateFactor) # updateFactor = 2 => extend hashTable to twice the size
        self._hashTable_ = [LinkedList() for i in range(self._size_)]
        
        # If you wanna use Numpy insted of list then
        # Uncomment 2 lines below and comment the just above one
        # self._hashTable_ = np.empty(self._size_,dtype=LinkedList)
        # for i in range(self._size_):  self._hashTable_[i] = LinkedList()
        
        for i in range(self._size_):  self._hashTable_[i] = LinkedList()
        self._occupied_ = 0
        self._alpha_ = self._occupied_ / self._size_
        bitLength = self._size_.bit_length() + 1
        self._prime_ = generatePrimeNumber(bitLength)
        self._uni_a_ = randrange(0,self._prime_ - 1)
        self._uni_b_ = randrange(0,self._prime_ - 1)
        for ith_linkedList in hashTableCopy:
            if(ith_linkedList.head == None):
                continue
            curr = ith_linkedList.head
            while curr.next != None:
                self.__add__(curr.key, curr.value)
                curr = curr.next
            self.__add__(curr.key, curr.value)
            ith_linkedList.destroy()

# =============================================================================

# This method is just for testing    
#    def __traverse__(self):
#        i = 0
#        for ith_linkedList in self.hashTable:
#            #print("Index:",i,end=": ")
#            i += 1
#            ith_linkedList.traverse()

# =============================================================================

    # This Function remove key, value pair associated with the specified key
    def __remove__(self,key):
        if(self._occupied_ == 0):
            return
        index_i = self.__universalHash__(key)
        ith_linkedList = self._hashTable_[index_i]
        doesExist = ith_linkedList.remove(key)
        if(doesExist):
            self._occupied_ -= 1
            self._alpha_ = self._occupied_ / self._size_
            if(self._alpha_ < self._alphaLowest_):
                self.__update__(1/2)

# =============================================================================

    # This function will insert new key, value pair
    def __add__(self,key, value):
        index_i = self.__universalHash__(key)
        ith_linkedList = self._hashTable_[index_i]
        isAlreadyPresent = ith_linkedList.find(key) != None
        if(not isAlreadyPresent):
            self._occupied_ += 1
            self._alpha_ = self._occupied_ / self._size_
            ith_linkedList.add(key, value)
            if(self._alpha_ > self._alphaMax_):
                self.__update__(2)

# =============================================================================

    # This function will return Node associated with the specified key None otherwise
    def __find__(self,key):
        index_i = self.__universalHash__(key)
        ith_linkedList = self._hashTable_[index_i]
        return ith_linkedList.find(key)

# =============================================================================

    # Convert string into integer < given mod
    def __stringToInt__(self,s,mod):
        r = 0
        for i in range(0,len(s)-1):
            temp = ord(s[i])
            nextLen = len(str(ord(s[i+1])))
            r += temp
            r *= 10**nextLen
            r = r % mod
        r += ord(s[len(s) - 1]) 
        return r % mod

# =============================================================================

    def __simpleHash__(self,key,mod):
        if(type(key) == type(1)):  # it its of int type
            return key % mod
        elif(type(key) == type('str')):
            return self.__stringToInt__(key,mod)
        elif(type(key) == type(1.0)):
            return int(key) % mod
        return None

# =============================================================================

    def __multiplicationHash__(self,key):    # h(k) = [(a*k) mod(2^w)] >> (w-r)
        if(type(key) == str):
            key = self.__simpleHash__(key)
        if(type(key) == float):
            key = int(float)
        w = 1 << (key + 1)
        key = self.__simpleHash__(key,w)     # r: no. of bits that we want, w: rep. no. of bit in a number
        h = (self.rand_a * key)                # say k and w are w1 and w2 bit number so h is w1 + w2 bit length
        r = self._size_.bit_length()             # r: no of bits require that is equal to no. of bits in our table size
        if(h.bit_length() < 2*r):              # only drop upper half if there is room for r bits
            h >> (h.bit_length()-r)
        else:
            w = h.bit_length()//2              # here we drop upper half bits
            h = h %  (1 << w)                  # Now say our h is b bits long so here we drop last b - r bits
            h >> (h.bit_length()-r)            # so here we left w/ random r bits
        h %= self.size                         # it's just to make sure that our hash is < size of table
        return h

# =============================================================================

    def __universalHash__(self,key):
        key = self.__simpleHash__(key,self._prime_)
        h = (self._uni_a_ * key + self._uni_b_) % self._prime_
        return h % self._size_

# =============================================================================

# It is used to load any of the provided dataset
def load(filename='LargeDataset1.data'):
    import _pickle
    print("Loading...")
    with open(filename, 'rb') as f:
        h = _pickle.load(f)
    print("Loaded.")
    return h

# =============================================================================

################################## Simple Example #############################
'''
h = HashTable()
# Insertion
h[1] = 3
h[5] = 2
h[55] = 'ABC'
h['hello'] = 5
h[5] = h['hello']
# deletion 
del h[1]
del h['hello']
# Itterate over hashTable
for key,val in h:
    print(key,val)
# length of hash table
print(len(h))
# check wether a key is in hash table or not
key = 5
print(key in h) # True
'''


############### All Below functions are just for testing purposes #############
''' 
# =============================================================================
    
    def fillHashTableRandomly(self,no_of_elements,h,filename):
        from random import randrange, getrandbits
        counter,fileNo = 0,0
        for i in range(no_of_elements):
            counter += 1
            if(counter == 100000):
                fileNo += 1
                counter = 0
                print("Creating Dataset...")
                s = time.time()
                with open(filename+str(fileNo)+'.data', 'wb') as f:
                    _pickle.dump(h, f)  
                f1 = open("Time.txt",'a')
                f1.write("DataSet:"+str(fileNo)+"took: "+str(time.time() - s)+"sec.\n")
                f1.close()
                print("Dataset Created")
            print("ittr: "+str(i))
            no_of_bits = randrange(8,64)
            k, v = getrandbits(no_of_bits),getrandbits(8)
            self.__add__(k, v)

# =============================================================================

    def removeHashTableRandomly(self,no_of_elements):
        for i in range(no_of_elements):
            index = randrange(0,len(self.trash))
            ele = self.trash[index]
            print("remove:",ele)
            self.__remove__(ele)

# =============================================================================
 
def speedCheck(h):
    import time
    s = time.time()
    j=0
    for k,v in h:
        j+=1
        t = h[k]
    print("Time:",time.time() - s)
   
# =============================================================================

f1 = open("Time.txt",'w')
def dump(n = 12000000):
    start = time.time()
    h = HashTable()
    filename = 'LargeDataset'
    h.fillHashTableRandomly(n,h,filename)
    f1 = open("Time.txt",'a')
    f1.write("Time taken in creating "+str(n)+" key, val pair is: "+str(time.time()-start))
    f1.close()

# =============================================================================
'''
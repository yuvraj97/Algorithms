# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 00:41:20 2019

@author: Yuvraj
"""

from lib.GenerateRandomPrime import generatePrimeNumber
from random import randrange

class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
    def destroy(self):
        self.key = None
        self.value = None

# Arguments of HashTable:
# self._hashTable_ is a list index of the list will work as a key element of this list contains:
# 1st arg is value and 2nd arg is used to keep track if the key is deleted or not
# self.alpha define the current utilization of hashTable
# self.alphaMax define that when did the size of hashTable doubles
# 0.5 mean when the hashtable is filled 50% size of hashTable doubles
# self.alphaLowest define that when did the size of hashTable reduces to half
# 0.25 mean when the hashtable is left 25% of the size then size of hashTable reduces to half
# Below arguments are used by our Universal Hash function:
# self._prime1_ self._uni_a1_ self._uni_b1_ self._prime2_ self._uni_a2_ self._uni_b2_ 
class HashTable():
    def __init__(self, size = 16, alphaMax = 0.5, alphaLowest = 0.25):
        self._size_ = size    # size define the size of the hash table
        self._hashTable_ = [[None,False] for i in range(self._size_)]
        self._occupied_ = 0   # occupied will keep track of how many of nodes are utilized
        self._alpha_ = self._occupied_ / self._size_
        self._alphaMax_ = alphaMax
        self._alphaLowest_ = alphaLowest
        bitLength = self._size_.bit_length() + 1
        if(bitLength < 16): bitLength = 16
        self._prime1_ = generatePrimeNumber(bitLength)    
        self._uni_a1_ = randrange(1,self._prime1_ - 1)
        self._uni_b1_ = randrange(0,self._prime1_ - 1)
        self._prime2_ = generatePrimeNumber(bitLength)
        self._uni_a2_ = randrange(0,self._prime2_ - 1)
        self._uni_b2_ = randrange(0,self._prime2_ - 1)
        
# =============================================================================

    # Usage len(h) ; h:hashTable object and len(h) will return number of key, value pair inserted
    def __len__(self):
        return self._occupied_

# =============================================================================
    
    # Usage h[key] ; it will return value associated with key
    def __getitem__(self,key):
        return self.__find__(key)
    
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
        for node in self._hashTable_:
            node = node[0]
            if(node == None):
                continue
            yield node.key,node.value

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
        hashTableCopy = self._hashTable_            # updateFactor = 1/2 => reduce hashTable to half the size
        self._size_ = int(self._size_*updateFactor) # updateFactor = 2 => extend hashTable to twice the size
        self._hashTable_ = [[None,False] for i in range(self._size_)]
        
        self._occupied_ = 0
        self._alpha_ = self._occupied_ / self._size_
        bitLength = self._size_.bit_length() + 1
        bitLength = self._size_.bit_length() + 1
        if(bitLength < 16): bitLength = 16
        self._prime1_ = generatePrimeNumber(bitLength)
        self._uni_a1_ = randrange(1,self._prime1_ - 1)
        self._uni_b1_ = randrange(0,self._prime1_ - 1)
        self._prime2_ = generatePrimeNumber(bitLength)
        self._uni_a2_ = randrange(1,self._prime2_ - 1)
        self._uni_b2_ = randrange(0,self._prime2_ - 1)
        for node in hashTableCopy:
            node = node[0]
            if(node == None):
                continue
            self.__add__(node.key, node.value)

# =============================================================================

    # This function will insert new key, value pair
    def __add__(self,key, value):   # here we use our hash function yi.e. quadratic probing
        index = self.__getIndex__(key)
        if(index == -1):                # it's to check that the key does not exist
            flag = True                 # and if key does not exist then prob for the next free node
            i = 1
            while(flag):
                index = self.__quad_probing_(key,i)
                if(self._hashTable_[index][0] != None): 
                    i += 1
                    continue
                flag = False
        self._hashTable_[index][0] = Node(key,value)
        self._hashTable_[index][1] = False
        self._occupied_ += 1
        self._alpha_ = self._occupied_ / self._size_
        if(self._alpha_ > self._alphaMax_):
            self.__update__(2)

# =============================================================================

    # __universalHash2__  need to be co-prime with self.size
    # I had taken care of it in __universalHash2__()
    def __quad_probing_(self,key,i):        # Quadratic Probing:  [ h(k,i) = (h1(k) + i*h2(k)) mod m ]
        ans = ( self.__universalHash1__(key) + i * self.__universalHash2__(key) ) % self._size_
        return ans

# =============================================================================
    # This Function remove key, value pair associated with the specified key
    def __remove__(self,key):
        if(self._occupied_ == 0):
            return
        index = self.__getIndex__(key)
        if(index == -1): return
        self._hashTable_[index][0].destroy()
        self._hashTable_[index][0] = None
        self._hashTable_[index][1] = True
        self._occupied_ -= 1
        self._alpha_ = self._occupied_ / self._size_
        if(self._alpha_ < self._alphaLowest_):
            self.__update__(1/2)

# ==============================================================`===============
    
    def __getIndex__(self,key):
        i = 1
        while(True):
            index_i = self.__quad_probing_(key,i)
            node = self._hashTable_[index_i]
            if(node[0] == None):        # if there is no element on that index
                if(node[1] == True):    # and if that element is deleted
                    i += 1              # the continue probing
                    continue
                else:
                    return -1           # if there is no element on that index and if that element is not deleted => key is not in table so return None
            else:                       # if there is an element on that index
                if(node[0].key == key):     # and if that element is our key
                    return index_i      # then return tha
                else:
                    i+=1
                    continue

# =============================================================================

    # This function will return Node associated with the specified key None otherwise
    def __find__(self,key):
        index = self.__getIndex__(key)
        if(index == -1):
            return None
        return self._hashTable_[index][0].value

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

    def __universalHash1__(self,key):
        key = self.__simpleHash__(key,self._prime1_)
        h = (self._uni_a1_ * key + self._uni_b1_) % self._prime1_
        return h % self._size_

# =============================================================================
        
    # __universalHash2__  need to be co-prime with self.size for self.__quad_prob__()
    # our self.size if multiple of 2. so if we make our hash odd so we are done
    def __universalHash2__(self,key):
        key = self.__simpleHash__(key,self._prime2_)
        h = ( (self._uni_a2_ * key + self._uni_b2_) % self._prime2_ ) | 1 # it's to make our hash odd
        return h % self._size_

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

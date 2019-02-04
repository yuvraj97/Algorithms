# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 04:09:30 2019
@author: Yuvraj
Inspired by MIT 6.006: Introduction to Algorithms - MIT OpenCourseWare
This is a program to find a string in a given string using Karp Rabin Algorithm
Using:
Rolling Hashes
Rabin-Karp Algorithm for Pattern Searching
"""
from lib.gcd import modInverse
from lib.GenerateRandomPrime import generatePrimeNumber
class RollingHash():
    def __init__(self,base,p):
        self.p = p                # p: prime number
        self.base = base
        self.hash = 0
        self.magic = 1            # magic: (base^size) mod p
        #self.ibase = pow(self.base,self.p-2,self.p) 
        self.ibase = modInverse(self.base, self.p)  # ibase: (base^-1) mod p   => multiplicative inverse of base mod p
    def append(self,new):
        self.hash = (self.hash * self.base + new ) % self.p
        self.magic = (self.magic * self.base ) % self.p
    def skip(self,old):
        self.magic = (self.magic * (self.ibase % self.p)) % self.p
        self.hash = (self.hash - old*self.magic + self.p*self.base) % self.p
    
# It will give us the most optimal base
# it will search for the largest value associated with each charater in the txt
def getBaseByString(txt):
    base = 0
    for i in txt:
        if(ord(i)>base):
            base = ord(i)
    return base +1

def find(txt,pattern):
    base = getBaseByString(txt)
    #print("Base:",base)
    size = len(pattern)
    prime = generatePrimeNumber()
    rtxt=RollingHash(base,prime)
    rpat=RollingHash(base,prime)
    # Get hash of the pattern
    for i in range(size):
        rpat.append(ord(pattern[i]))
    # Get hash of the first (size) number of character string
    for i in range(size):
        rtxt.append(ord(txt[i]))
    if(rtxt.hash == rpat.hash):         # if the hashes matched confirm the match by comparing strings
        if(txt[0:size] == pattern):
            return 0
    old=ord(txt[0])                     # old is the first character of our sliding window that is to be remove
    # Now we slide our window to the given txt
    for i in range(size,len(txt)):
        new = ord(txt[i])               # new is the next character that is to be added in the window
        rtxt.append(new)                # adding new in our hash
        rtxt.skip(old)                  # remove old in our hash
        old = ord(txt[i - size + 1])    # old character that will be deleted in next itteration
        if(rtxt.hash == rpat.hash):     # As the hashes matched confirm the match by comparing string characters
            if(txt[i-size+1:i+1] == pattern):
                return i - size +1
    return -1

"""
# EXAMPLE
txt = "1[]2A{'}\tnB\0CE~ti4:?9,<4$!7e>)hg*f#78%#@hj@G!HU&*"
pattern = "hj@G!HU"
print(find(txt,pattern))
"""
"""
f=open("test.txt",'r')
txt = f.read()
pattern = "search"
print(find(txt,pattern))
"""

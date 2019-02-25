# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 10:56:09 2019

@author: Yuvraj
"""
# Starting at index i what is the Longest Increasing Subsequence

# It will return a list of random integers
def randomList(n,random_element_range = 100):
    from random import randrange
    l = []
    for i in range(n):  l.append(randrange(0,random_element_range))
    return l

# It will get the Longest Increasing Subsequence
def __Longest_Increasing_Subsequence__(l, record, i):
    if(i in record):
        return record[i]
    if(i == len(l) -1):
        record[i] = 1
        return 1
    max = 1
    for j in range(i+1,len(l)):
        lis = __Longest_Increasing_Subsequence__(l, record, j)
        if(l[j] > l[i]):
            if(lis >= max):  max = lis + 1
    record[i] = max
    return max

# It returns a list containing indices of Longest Increasing Subsequence
def Longest_Increasing_Subsequence(l,index):
    record = {}
    __Longest_Increasing_Subsequence__(l,record,index)
    lis = [index]
    max = record[index] - 1
    for i in range(index,len(l)):
        if(record[i] == max):
            lis.append(i)
            max -= 1
            if(max == 0): break
    return lis

# Example
# l = randomList(10,random_element_range=100)
# lis = Longest_Increasing_Subsequence(l,3)
# print("Longest Increasing Subsequence of:",l)
# print(lis)
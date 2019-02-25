# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:11:55 2019

@author: Yuvraj
"""

import numpy as np
from random import randrange
# =============================================================================
    
# cost of multiplying metrix1 * metrix2
# Number of operation perform: m1_rows * m1_column * m2_column
# Here m1_column == m2_rows
def cost(metrix1, metrix2):
    m1_rows, m1_column = metrix1[0], metrix1[1]
    m2_rows, m2_column = metrix2[0], metrix2[1]
    return m1_rows * m1_column * m2_column

# =============================================================================

# it will compute the optimal way to multiply matrices
# Sequence: it is the list of the dimensions of matrices
# Ex: sequence = [(4, 3), (3, 4), (4, 4), (4, 4), (4, 2)]
# ==> 5 matrices with respective dimensions
# record: records the cost of multiplying matrices
# parent: keep track a optimal path to multiplying a range of matrix
def __DP__(sequence, record, parent, i, j):
    if((i,j) in record):    return record[(i,j)]
    if(j - i == 1): # return cost and shape of multiplying two matrices
        cst, shape = cost(sequence[i],sequence[j]), (sequence[i][0],sequence[j][1])
        record[(i,j)] = (cst,shape)
        parent[(i,j)] = (i,j)
        return (cst,shape)
    elif(i == j):
        cst, shape = 0, sequence[i]
        record[(i,j)] = (cst,shape)
        parent[(i,j)] = (i,j)
        return (cst,shape)
    min, parentOf, resultMetrix = None, None, None
    for k in range(i+1, j+1):
        cost_i_k, shape_i_k = __DP__(sequence, record, parent, i, k-1)
        cost_k_j, shape_k_j = __DP__(sequence, record, parent, k, j) 
        cost_i_j = cost_i_k + cost_k_j + cost(shape_i_k,shape_k_j)
        if(min == None or cost_i_j < min):
            min = cost_i_j
            parentOf = ((i,k-1),(k,j))
            resultMetrix = (shape_i_k[0], shape_k_j[1])
    record[(i,j)] = (min,resultMetrix)
    parent[(i,j)] = parentOf
    return record[(i,j)]

# =============================================================================
    
def DP(sequence,metrices_sequence):
    record = {}
    parent = {}
    for i in range(len(sequence)):
        for j in range(i+1,len(sequence)):
            __DP__(sequence,record,parent,i,j)
    curr = (0,len(sequence) - 1)
    return __multiplyMetrices__(parent,metrices_sequence,curr)

# =============================================================================
    
# It will multiply matrices according to DP()
def __multiplyMetrices__(parent,metrices_sequence,curr):
    curr = parent[curr]
    if(type(curr[0]) == tuple): # There are 2 sequences, curr: ((Mi to Mk), (Mk to Mj))
        seq1, seq2 = curr[0],curr[1]
        if(seq1[0] == seq1[1]):
            m2 = __multiplyMetrices__(parent,metrices_sequence,seq2) # First solve for the parenthesis
            m1 = __multiplyMetrices__(parent,metrices_sequence,seq1) 
        elif(seq2[0] == seq2[1]):
            m1 = __multiplyMetrices__(parent,metrices_sequence,seq1) # First solve for the parenthesis
            m2 = __multiplyMetrices__(parent,metrices_sequence,seq2)
        else:
            m1 = __multiplyMetrices__(parent,metrices_sequence,seq1)
            m2 = __multiplyMetrices__(parent,metrices_sequence,seq2)
        return np.dot(m1,m2)
    else:
        if(curr[0] == curr[1]): # Mean single metrix
            return metrices_sequence[curr[0]]
        else:   # There are two metrices
            return np.dot(metrices_sequence[curr[0]],metrices_sequence[curr[1]])

# =============================================================================

# This function is just to give a list of random matrices
# Of a specified sequence
def getSequenceOfMetrices(sequence):
    sizes = sequence
    metrix_element_range, metrix = 10, []
    for size in sizes:
        sub_metrix = []
        for rows in range(size[0]):
            temp = []
            for column in range(size[1]):   temp.append(randrange(1,metrix_element_range))
            sub_metrix.append(np.array(temp))
        metrix.append(np.array(sub_metrix))
    return metrix

# =============================================================================

# It return tuples with random dimensions of matrices: [(row1, col1), (row2, col2), (row3, col3).....]
# Condition col1 == row2, col2 == row3, ......
def randomSeqMetricsSizes(no_of_metrices = 5, size_range_start = 10, size_range_end = 10):
    metrices_multiplication = []
    a0 = randrange(size_range_start,size_range_end)
    met1 = [a0,0]
    for i in range(no_of_metrices):
        temp = randrange(size_range_start,size_range_end)
        met1[1] = temp
        metrices_multiplication.append(tuple(met1))
        met1[0] = temp
    return metrices_multiplication

# =============================================================================

# It will linearly multiply the matrices
def multiplyMetricesLinearly(metrix_list):
    temp = metrix_list[0]
    for i in range(1,len(metrix_list)):   temp = np.dot(temp, metrix_list[i])
    return temp

# Example
no_of_metrices = 50
sequence_of_sizes_of_metrices = randomSeqMetricsSizes(no_of_metrices,100,600)
metrices_sequence = getSequenceOfMetrices(sequence_of_sizes_of_metrices)
m = DP(sequence_of_sizes_of_metrices,metrices_sequence)
print("Multiplication of matrices:")
print(m)

###############################################################################
############# Function Given below are just for Testing purposes ###############
###############################################################################

'''
# Given a list of matrices it returns the list of dimensions of the metrices respectively
def getShapesOfSequence(M):
    shapes = []
    for metrix in M:
        shapes.append(metrix.shape)
    return shapes

# It will check if two matrices are equal or not
def check(m1,m2):
    eq = m1 == m2
    for i in eq:
        for j in i:
            if(j == False):
                return False
    return True

def printMetrices(metrix_list):
    for metrix in metrix_list:
        print("Metrix w/ size:",metrix.shape)
        for rows in metrix: print(rows)

i = 0
while(True):
    print(i)
    i+=1
    no_of_metrices = 20
    sequence_of_sizes_of_metrices = randomSeqMetricsSizes(no_of_metrices)
    metrices_sequence = getSequenceOfMetrices(sequence_of_sizes_of_metrices)
    m1 = DP(sequence_of_sizes_of_metrices,metrices_sequence)
    m2 =multiplyMetricesLinearly(metrices_sequence)
    if(check(m1,m2) == False): break
'''

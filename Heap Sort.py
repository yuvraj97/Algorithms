# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 04:03:57 2018

@author: Vaio
"""

# This Function takes in a array 'a' and checks to its right child and left child
# if left child is bigger then it swap the value with left child and recurse to the left subtree to check if there any violation of our invariant.
#     If yes then it will recurse untill last parent node
# if right child is bigger then it swap the value with right child and recurse to the right subtree to check if there any violation of our invariant.
#     If yes then it will recurse untill last parent node
# Invariant: parent node must be Greater then or equal to the Child node
# The primary assumption here is that the right and left subtrees are the Max Heap.
# a: is the input array
# i: is index where we may have violation of our invarient and correct_violation() will remove the violation 
# n: is use for boundation: so that our correct_violation() will check the invariant in the array at nth element
#     -> Like in the heap_Sort() describes Later. For Example take any array with no. of element say 4
#           - We First call build_max_heap() (that takes an array and make it a MAX HEAP)
#           - Now we have max element of array at top or at index 0
#           - Now our strategy is take the max element and put it in last of array (And do it over and over)
#           - Now we achieve it by this correct_violation(). When we first call build_max_heap() we created a MAX HEAP
#           - Now we swap First element of array (that is the max element) with the last element.
#           - Now it may break our invarient at first element
#           - Then we call correct_violation() ( its primary assumption is satisfied already cause of build_max_heap() )
#           - Here n comes in role, Here n denotes index number till which we have to scan (excluding n) correct_violation()
#           - First we swap the first element with index n, then call correct_violation()
#           - so that it will again create MAX_HEAP array[0:n-1] and array[n:len(a)] is our sorted array.
#           - And iteratively we slides to left of array till we get the sorted array[0 : len(a)]
def correct_violation(a, n, i): # Time Complexity for correct_violation(a,n,i) is O( log(N) ) where N is the size of array

    #if(i > len(a)/2):   # This condition is True is all the parent nodes are verified (we don't have to do any thing with leaves because the are by defination heap)
    #    return;
    if(2*i +2 < n and a[i] < a[2*i + 2]):  # This condition checks the 
        a[i], a[2*i + 2] = a[2*i + 2], a[i] # swap the parent and the right child
        correct_violation(a, n, 2*i + 2);   # recurse on right sub tree
    if(2*i +1 < n and a[i] < a[2*i +1]):
        a[i], a[2*i + 1] = a[2*i + 1], a[i];   # swap the parent and the right child
        correct_violation(a, n, 2*i + 1);   # recurse on left sub tree

# This function generates a Max Heap of array a
# Time Complexity for build_max_heap(a) is O(N) where N is size of array a 
def build_max_heap(a):
    n=len(a)
    for i in range(int(n/2) - 1,-1,-1):
        correct_violation(a, n, i); # Time Complexity for correct_violation(a,i) is O( log(i) )
# It takes in an array a as input and sort it
def heap_Sort(a):   # Time Complexity of heap_Sort(a) is O( nlg(n) )  lg is log base 2
    n = len(a);
    build_max_heap(a);
    for i in range(len(a)):
        a[n - i - 1] ,a[0] = a[0] ,a[n - i - 1];
        correct_violation(a, n - i - 1, 0)  # Time Complexity for correct_violation(a,0) is O( log(N) ) where N is size of array a

# Example
array = [3,4,5,5,32,5,7,8,6,43,2,3,5,6,8,9,85,4,43,445,6,7,4,5,57,75,45,235,32,736,73,23,512,523,573,68,674]
#array = [16,4,8,3,8,12,13,2,1,5,6,10,11,9,12];
#array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
heap_Sort(array);
print(array)

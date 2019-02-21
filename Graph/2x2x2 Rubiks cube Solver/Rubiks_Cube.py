# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:26:48 2019

@author: Yuvraj
"""
I = [i for i in range(24)]
I=tuple(I)

def __inverse__(l):
    inv = [0]*len(l)
    for i in range(len(l)):
        inv[l[i]] = i
    return tuple(inv)
FC = (2,0,3,1,18,5,19,7,8,9,10,11,12,22,14,23,16,17,15,13,20,21,6,4)
FCC = __inverse__(FC)
RC = (0,23,2,21,6,4,7,5,19,9,10,17,12,13,14,15,16,1,18,3,20,8,22,11)
RCC = __inverse__(RC)
UC = (4,5,2,3,8,9,6,7,12,13,10,11,0,1,14,15,18,16,19,17,20,21,22,23)
UCC = __inverse__(UC)

def __rotate__(arrangement_to_be_rotate, which_direction):
    result = [0]*len(which_direction)
    for i in range(len(which_direction)):
        result[i] = arrangement_to_be_rotate[which_direction[i]]
    return tuple(result)

def random_shuffle_cube(arrangement_to_be_shuffle,n):
    start = arrangement_to_be_shuffle
    from random import randrange
    print("Shuffling: ",end="")
    for i in range(n):
        rand = randrange(0,600)
        if(rand>=0 and rand<100):
            print("RCC --> ",end="")
            start = __rotate__(start,RCC)
        elif(rand>=100 and rand<200):
            print("RC --> ",end="")
            start = __rotate__(start,RC)
        elif(rand>=200 and rand<300):
            print("UC --> ",end="")
            start = __rotate__(start,UC)
        elif(rand>=300 and rand<400):
            print("UCC -->",end="")
            start = __rotate__(start,UCC)
        elif(rand>=400 and rand<500):
            print("FC --> ",end="")
            start = __rotate__(start,FC)
        elif(rand>=500 and rand<600):
            print("FCC --> ",end="")
            start = __rotate__(start,FCC)
    print(" Shuffled :)")
    return start

def __neighbours__(arrangement):
    yield __rotate__(arrangement,FC),  'FC'
    yield __rotate__(arrangement,FCC), 'FCC'
    yield __rotate__(arrangement,UC),  'UC'
    yield __rotate__(arrangement,UCC), 'UCC'
    yield __rotate__(arrangement,RC),  'RC'
    yield __rotate__(arrangement,RCC), 'RCC'

def __shortestPath__(initial, final,forward_parent,backward_parent):
    forward_frontier = [initial]
    backward_frontier = [final]
    level = 0
    while(len(forward_frontier) != 0 and len(backward_frontier) != 0):
        forward_next =[]
        backward_next =[]
        for node in forward_frontier:
            for neig,label in __neighbours__(node):
                if neig not in forward_parent:
                    forward_parent[neig] = (node,label)
                    forward_next.append(neig)
        for node in backward_frontier:
            for neig,label in __neighbours__(node):
                if neig not in backward_parent:
                    backward_parent[neig] = (node,label)
                    backward_next.append(neig)
        for node in forward_parent:
            if node in backward_parent:
                return node
            
        forward_frontier = forward_next
        backward_frontier = backward_next
        level+=1

def __reverse__(label):
    if(label=='FCC'): return 'FC'
    if(label=='UCC'): return 'UC'
    if(label=='RCC'): return 'RC'
    if(label=='FC'):  return 'FCC'
    if(label=='UC'):  return 'UCC'
    if(label=='RC'):  return 'RCC'

def solveRubiksCube(initial,final):
    forward_parent,backward_parent={},{}
    forward_parent[initial] = (None,"Solved")
    backward_parent[final] = (None,"Solved")
    forw,back=[],[]
    node = __shortestPath__(initial,final,forward_parent,backward_parent)
    curr = node
    while(curr!=None):
        curr, label = forward_parent[curr]
        forw.append(__reverse__(label))
    forw.pop()
    curr = node
    while(curr!=final):
        curr, label = backward_parent[curr]
        back.append(label)
    back.reverse()
    back.extend(forw)
    
    s=""
    for i in range(len(back)):
        s = s + back[i] + " --> "
    s = s + "Solved :)"
    return s

def shuffleManually(l):
    start = I
    for step in l:
        s = step.lower()
        if(s == "rcc"):
            start = __rotate__(start,RCC)
        elif(s == "rc"):
            start = __rotate__(start,RC)
        elif(s == "uc"):
            start = __rotate__(start,UC)
        elif(s == "ucc"):
            start = __rotate__(start,UCC)
        elif(s == "fc"):
            start = __rotate__(start,FC)
        elif(s == "fcc"):
            start = __rotate__(start,FCC)
        else:
            raise ValueError('"'+ str(step) + '" is not a valid argument (')
    return start
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 22:24:56 2019

@author: Yuvraj
"""
import numpy as np
import csv

# =============================================================================

def load(path):
    data=open(path,'r');    # for example: open('/home/rajesh/Desktop/HackerRank/InterviewBit/Py/SpanningTree/SpanningTreeDataset.csv','r');
    dataList=list(csv.reader(data));
    dataArray=np.array(dataList);
    dataList=None;
    no_graphs=0;
    for i in range(len(dataArray)):
        if dataArray[i][0]=='#':
            no_graphs+=1;
    graph_array=[[[],[]] for i in range(no_graphs)]
    i=0;    # i is use for traversing dataArray
    for graph_counter in range(no_graphs):
        #print("Graph",graph_counter)
        i+=1        # here by incrementing we reach to no of vertices cell and in next line we access no of vertices
        graph_array[graph_counter][0] = int(dataArray[i][0])
        i+=1;       # now here by incrementing we reach to the edges connection so now we store edges in matrix
        while dataArray[i][0]!='#' and dataArray[i][0]!='!':
            graph_array[graph_counter][1].append((int(dataArray[i][0]), int(dataArray[i][1])))
            i+=1;
    return no_graphs , graph_array

# =============================================================================

def load2(path):
    data=open(path,'r');    # for example: open('/home/rajesh/Desktop/HackerRank/InterviewBit/Py/SpanningTree/SpanningTreeDataset.csv','r');
    dataList=list(csv.reader(data));
    data.close()
    dataArray=list(dataList);
    dataList=None;
    for i in range(len(dataArray)):
        while(True):
            if(dataArray[i][-1]==''):
                dataArray[i].pop()
                continue
            break
    dataArray.pop()
    vertices = dataArray[1]
    isWeightes = len(dataArray[2]) == 3
    edges = []
    if(isWeightes):
        for i in range(2,len(dataArray)):
            edges.append((dataArray[i][0],dataArray[i][1],int(dataArray[i][2])))
    else:
        for i in range(2,len(dataArray)):
            edges.append((dataArray[i][0],dataArray[i][1]))
    return vertices,edges

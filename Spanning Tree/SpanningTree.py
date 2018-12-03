# =============================================================================#!/usr/bin/env python2
    #!/usr/bin/env python2
    # -*- coding: utf-8 -*-
    # Created on Sat Jun  2 01:15:01 2018
    # @author: yuvraj
# =============================================================================

import numpy as np;
import warnings
import csv;
   
class AdjacencyMatrix():
    def __init__(self):
        self.matrix=None;
class Graph():
    def __init__(self):
        self.vertex=None;
        self.adjacency=AdjacencyMatrix();                  # AdjacencyMatrix
# =============================================================================
    def inputVertices(self,no_vertex):
        if no_vertex==0:
            return None;
        self.vertex=np.empty((no_vertex,1),int);
        for i in range(0,self.vertex.size):
            self.vertex[i][0]=i;
        self.adjacency=None;
# =============================================================================
    def printEdges(self):
        if self.vertex==None:
            print "There is No self.vertex first insert self.vertex";
            return None;
        if self.adjacency.matrix==None:
            print "There is No Edge first insert edge";
            return None;
        for i in range(0,self.vertex.size):
            for j in range(0,self.vertex.size):
                if i<j and self.adjacency.matrix[i][j]==1:
                    print i,"\t",j;
# =============================================================================
    def neighbour(self,n=None):
        if n!=None:
            if self.vertex==None:
                print "There is No self.vertex first insert self.vertex";
                return None;
            if self.adjacency.matrix==None:
                print "There is No Edge first insert edge";
                return None;
            if n<0 or n>self.vertex.size:
                return None;

            ret=np.zeros(self.vertex.size-1,int);
            for i in range(0,ret.size):
                ret[i]=-1;
            ret_count=0;
            for i in range(0,self.vertex.size):
                if self.adjacency.matrix[n][i]==1:
                    ret[ret_count]=i;
                    ret_count+=1;
            return ret;
# =============================================================================
    def path(self,start,end):
        isVisited=np.zeros(self.vertex.size,bool);
        seq=[];
        seq=self.pathSequence(start,end,isVisited,seq);
        return seq;
# =============================================================================
    def pathSequence(self,start,end,isVisited,seq):
        isVisited[start[0]]=True;
        seq.append(start[0]);
        neig=self.neighbour(start[0]);
        for i in range(neig.size):
            if neig[i]!=-1:
                if isVisited[neig[i]]==False:
                    if self.vertex[neig[i]]==end:
                        seq.append(end[0]);
                        return seq;
                    else:
                        res = self.pathSequence(self.vertex[neig[i]],end,isVisited,seq);
                        if res!= None:
                            return res;
            else:
                break;
        seq.pop();
        return None;
# =============================================================================    
    def isConnected(self):
        for i in range(self.vertex.size):
            for j in range(i+1,self.vertex.size):
                if self.path(self.vertex[i],self.vertex[j])==None:
                    return False;
        return True;
# =============================================================================
    def cycleSequence(self,start,end,isVisited,seq):
        isVisited[start[0]]=True;
        seq.append(start[0]);
        neig=self.neighbour(start[0]);
        for i in range(neig.size):
            if neig[i]!=-1:
                if isVisited[neig[i]]==False:
                    res = self.cycleSequence(self.vertex[neig[i]],end,isVisited,seq);
                    if res!= None:
                        return res;
                elif len(seq)>=3 and end[0]==self.vertex[neig[i]][0]:
                    seq.append(end[0]);
                    return seq;
            else:
                break;
        seq.pop();
        return None;
        # =============================================================================
    def cycle(self,start):
        isVisited=np.zeros(self.vertex.size,bool);
        seq=[];
        seq=self.cycleSequence(start,start,isVisited,seq);
        if seq!=None and seq[0]==seq[-1]:
            return seq;
        return None;
# =============================================================================
    def isCycleExist(self):
        for i in range(self.vertex.size):
            path=self.cycle(self.vertex[i]);
            if path != None:
                return True;
        return False;
# =============================================================================
    def spanningTree(self):
        if self.isConnected()==False:
            return None
        dummy=np.zeros((self.vertex.size,self.vertex.size),int);
        for i in range(0,self.vertex.size):
            for j in range(0,self.vertex.size):
                dummy[i][j]=self.adjacency.matrix[i][j];
        g1=Graph();
        g1.inputVertices(self.vertex.size);
        g1.adjacency=AdjacencyMatrix();
        g1.adjacency.matrix=dummy;
        for i in range(0,g1.vertex.size):
            for j in range(0,g1.vertex.size):
                if g1.adjacency.matrix[i][j]==1:
                    g1.adjacency.matrix[i][j]=0;
                    g1.adjacency.matrix[j][i]=0;
                    if g1.isConnected()==False:
                        g1.adjacency.matrix[i][j]=1;
                        g1.adjacency.matrix[j][i]=1;
        if g1.isCycleExist():
            return None;
        return dummy;
# =============================================================================
def getSpanningTreeOfDataSet(path):
    data=open(path,'r');    # for example: open('/home/rajesh/Desktop/HackerRank/InterviewBit/Py/SpanningTree/SpanningTreeDataset.csv','r');
    dataList=list(csv.reader(data));
    dataArray=np.array(dataList);
    dataList=None;
    
    # No. of Graphs:
    no_graphs=0;
    for i in range(len(dataArray)):
        if dataArray[i][0]=='#':
            no_graphs+=1;
    # Creating Array of graphs
    graph_array=np.empty(no_graphs,object);
    graph_count=0;
    
    #Assigning each Graph it's Properties
    i=0;    # i is use for traversing dataArray
    for graph_counter in range(no_graphs):
        g=Graph();
        i+=1        # here by incrementing we reach to no of vertices cell and in next line we access no of vertices
        g.inputVertices(int(dataArray[i][0]))
        g.adjacency=AdjacencyMatrix();
        # Initializing AdjacencyMatrix
        g.adjacency.matrix=np.zeros((g.vertex.size,g.vertex.size),int);
        i+=1;       # now here by incrementing we reach to the edges connection so now we store edges in matrix
        while dataArray[i][0]!='#' and dataArray[i][0]!='!':
            g.adjacency.matrix[int(dataArray[i][0])][int(dataArray[i][1])]=1;
            g.adjacency.matrix[int(dataArray[i][1])][int(dataArray[i][0])]=1;
            i+=1;
        graph_array[graph_count]=g;
        graph_count+=1;
        g=None; # releasing memory stored by g
    return no_graphs , graph_array

# =============================================================================
    
if __name__ == "__main__":
# ----------------------------------------
    with warnings.catch_warnings():         # this is to supress warning of None comparisionthat occure mostly and the warning is:
        warnings.simplefilter("ignore")     # FutureWarning: comparison to `None` will result in an elementwise object comparison in the future.
# -----------------------------------------
        path=raw_input("Enter absolute path of the DataSet:");
            
        no_graphs, graph_array=getSpanningTreeOfDataSet(path);
        
        for graph_counter in range(no_graphs):
            g1=graph_array[graph_counter];
            if g1.isConnected()==False:
                print "The Graph:",graph_counter+1,"is disconnected so is does not have a SpanningTree";
                continue;
            g2=Graph()
            g2.inputVertices(g1.vertex.size);
            g2.adjacency=AdjacencyMatrix();
            g2.adjacency.matrix=g1.spanningTree();
            print "For Graph:",graph_counter+1,"SpanningTree's Edges Will be:";
            g2.printEdges();

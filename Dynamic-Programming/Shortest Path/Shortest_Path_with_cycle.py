# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 03:01:01 2019

@author: Yuvraj
"""
import lib.Graph as graph

# Here in return we use boolean to track that is there startVertex in the path(traversing up)
# if there is startVertex in the path then only relax the neighbour
# cost_memo is used to record the evaluated shortest path
def __DP_Shortest_Path_with_cycle__(g,startVertex,endVertex,parent,cost_memo,k):
    if((k,endVertex) in cost_memo): return cost_memo[(k,endVertex)]
    if(endVertex == startVertex):   return 0, True
    if(k == 0): return 0,False
    min, parentIs, boolean = None, None, False
    for neig,weight in g.reverseNeighbour(endVertex):
        shortest_path_from_vertex_to_neig, b = __DP_Shortest_Path_with_cycle__(g,startVertex,neig,parent,cost_memo,k-1)
        if(shortest_path_from_vertex_to_neig == None):  shortest_path_from_vertex_to_neig = 0
        cost = shortest_path_from_vertex_to_neig + weight
        if(b):
            boolean = True
            if(min == None or cost < min):  parentIs, min = neig, cost
    if(boolean):
        parent[endVertex] = parentIs
        cost_memo[(k,endVertex)] = (min,boolean)
    return min, boolean

def DP_Shortest_Path_with_cycle(g,startVertex,endVertex):
    if(g.isUndirectedGraph): raise ValueError("Graph must be Undirected")
    if(not g._isWeighted_): raise ValueError("Graph must be weighted")
    if(startVertex==endVertex): return None
    parent = graph.ht.HashTable()
    cost_memo = graph.ht.HashTable()
    cost,t = __DP_Shortest_Path_with_cycle__(g,startVertex,endVertex,parent,cost_memo,g.noOfVertices()-1)    
    if(cost == None):
        return None
    curr = endVertex
    l = []
    while(curr!=None):
        l.append(curr)
        curr = parent[curr]
    l.reverse()
    return l,cost

#path = 'C:\\Users\\Yuvraj\\Desktop\\py\\Dynamic Programming\\Cycle.csv'
#g = graph.load(path,isUndirected=False)
#print(DP_Shortest_Path_with_cycle(g,'B','C'))

'''
for  u in g.vertices():
    for v in g.vertices():
        r = DP_Shortest_Path_with_cycle(g,u,v)
        if(r !=None):
            print("Path from:",u,"to:",v,":",end = ' ')
            print(r)
'''
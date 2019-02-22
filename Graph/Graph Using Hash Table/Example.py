# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 06:27:43 2019

@author: Yuvraj
"""

import GraphUsingHashTable as graph



# Currently implemented Data Structures:
# Hash Table(Using Open Addressing)
# Binary Heap(Used in Dijkstra)

# Currently implemented Algorithms:
# Open Addressing(Double Hashing as a hash function): for Hash Table
# Depth-First-Search: Used in methos                AdjacencyList.isCycleExist() method
# Breath-First-Search: Used in a method             __ShortestPath__.shortestPathWeighted() method
# Topological Sort
# Dijkstra Algorithm: Using HashTable in method:    __ShortestPath__.dijkstraV1()
# Dijkstra Algorithm: Using Binary Heap in method:  __ShortestPath__.dijkstraV2()
# Bellman-Ford in method:                           __ShortestPath__.bellman_ford()

################################## Example ####################################

                                        # The Graph lools like
vertices = [0,1,2,3,4]                  #        0            
edges=[                                 #       /|\
(0,1),                                  #      / | \
(0,2),                                  #     /  |  \
(0,3),                                  #    /   |   \
(1,2),                                  #   1----2----3
(1,4),                                  #   \    |   /
(2,3),                                  #    \   |  /
(2,4),                                  #     \  | /
(3,4)                                   #      \ |/
]                                       #        4

g = graph.AdjacencyList(vertices,edges,isUndirectedGraph=True,dtype=int)

# To get summery of graph g 
print(g)
# Output:
'''
{
        1: [0, 2, 4]
        4: [1, 2, 3]
        2: [4, 0, 1, 3]
        3: [0, 2, 4]
        0: [1, 3, 2]
}
'''

# Iterrate over the graph
for neig in g:
    print(neig)
# Output:
# ['4', ['1', '2', '3']]
# ['0', ['1', '2', '3']]
# ['2', ['0', '1', '3', '4']]
# ['3', ['0', '2', '4']]
# ['1', ['0', '2', '4']]

# To determine number of vertices: g.noOfVertices()
print(g.noOfVertices())

# To determine number of edges: g.noOfEdges()
print(g.noOfEdges())

# To get neighbour of any vertex V/ say V = 3
# 1st way:      [neig for neig in g[V]]
# 2nd way:      g.getNeighbour(V)
neig = [neig for neig in g[3]]
print("Neighbour of 3:",neig)   # Output: ['0', '2', '4']
print("Neighbour of 3:",g.getNeighbour(3))

# To add a new edge There are 2 options Lets say you wanna make a edge b/w 1 and 4:
# 1st way:      g[startVertex] = endVertex
# 2nd way:      g.addNewEdge((startVertex,endVertex))
g[1] = 4
g.addNewEdge((1,4))

# To add a new vertex There is 1 options Lets say you wanna make a vertex say 5:
# g.addNewVertex(5)
g.addNewVertex(5)

# To delete a vertex there a 2 options Let say you wanna delete vertex 2:
# 1st way   del g[vertex]
# 2nd way   g.deleteVertex(vertex)
del g[2]
g.deleteVertex(2)

# To delete an edge There is 1 options Lets say you wanna delete edge b/w 0 and 1:
# g.deleteEdge((startVertex,endVertex))
g.deleteEdge((0,1))

# To get the vertices:
# 1st way: generator: Usage:    V = [vert for vert in g.vertices()]
# 2nd way: method:    Usage:    V = g.getVertices()
V = [vert for vert in g.vertices()]
V = g.getVertices()

# To get the shortest path b/w 2 nodes Lets say you wanna find shortest path b/w 1 and 3
# g.shortestPath((startVertex,endVertex))   # Argument is a tuple. It will return a list of vertices showing path
# This method will automatically detect that is the graph was directed or have a negative edge and according to that it will return the shortest path.
# for a unweighted graph: it will use BFS technique
# for a weighted graph(with non negative edges) it will use Dijkstra Algorithm
# for a weighted graph(with negative edges) it will use Bellman-Ford Algorithm
# these parameters are automatically detected you wont have to specify it, you just have to call graph.shortestPath((startVertex,endVertex))
g = graph.AdjacencyList(vertices,edges)
l = g.shortestPath((1,3))
print("Shortest Path from 1 to 3:",l)

# To get the DFS of a vertex there are two ways, Let say you wanna find DFS of vertex V
# 1st way: genertor: Usage:     dfs_V = [vert for vert in g.DFS(V)]
# 2nd way: method    Usage:     dfs_V = g.getDFS(V)
dfs_V = [vert for vert in g.DFS(6)]
dfs_V = g.getDFS(6)
print("DFS on 6:",dfs_V)

# To get value(cost) of an edge
# Use: g.getValueOf(edge): edge is a tuple of start and end vertex, if your graph is weighted then it will return value(cost), None otherwise
g.getValueOf((1,2))

# To set value(cost) of an edge
# Use: g.setValueOf(edge): edge is a tuple of start and end vertex
g.setValueOf((1,2),4)
g.setValueOf((1,2),None)

# To check if the graph has a cycle
# g.isCycleExist()
print("CycleExist:",g.isCycleExist())

# To copythe graph g:
# Use: g.copy()
g1 = g.copy()


# To get a scheduled job for a graph g
# Usage:    g.topologicalSort()
print(g.topologicalSort())


######################## If you have the Graph in a file ##########################

pathNegative  = 'C:\\Users\\Yuvraj\\Documents\\GitHub\\Algorithms\\Graph\\Graph Using Hash Table\\DataSet\\Weigted\\Negative Graph 3.csv'
pathUD        = 'C:\\Users\\Yuvraj\\Documents\\GitHub\\Algorithms\\Graph\\Graph Using Hash Table\\DataSet\\Undirected Graph\\Graph 4.csv'
pathWeighted  = 'C:\\Users\\Yuvraj\\Documents\\GitHub\\Algorithms\\Graph\\Graph Using Hash Table\\DataSet\\Weigted\\Graph 1.csv'
pathD         = 'C:\\Users\\Yuvraj\\Documents\\GitHub\\Algorithms\\Graph\\Graph Using Hash Table\\DataSet\\Directed Graph\\DirectedGraph3.csv'
pathDAG       = 'C:\\Users\\Yuvraj\\Documents\\GitHub\\Algorithms\\Graph\\Graph Using Hash Table\\DataSet\\DAG\\DAG-2.csv'
gNegative     = graph.load(pathNegative,isUndirected=False)
gUD           = graph.load(pathUD,      isUndirected=True)
gWeighted     = graph.load(pathWeighted,isUndirected=False)
gD            = graph.load(pathD,       isUndirected=False)
gDAG          = graph.load(pathDAG,     isUndirected=False)

gNegative_path = gNegative.shortestPath(('C','D'))
gUD_path       = gUD.shortestPath((2,3))
gWeighted_path = gWeighted.shortestPath(('A','C'))
gD_path        = gD.shortestPath(('G','D'))
gDAG_path      = gDAG.shortestPath(('O','G' ))

print(gNegative_path)
print(gUD_path)
print(gWeighted_path)
print(gD_path)
print(gDAG_path)

'''
for u in gNegative.vertices():
    for v in gNegative.vertices():
        print("Path from:",u, " to:",v,end=" ::")
        print(gNegative.shortestPath((u,v)))
for u in gUD.vertices():
    for v in gUD.vertices():
        print("Path from:",u, " to:",v,end=" ::")
        print(gUD.shortestPath((u,v)))
for u in gWeighted.vertices():
    for v in gWeighted.vertices():
        print("Path from:",u, " to:",v,end=" ::")
        print(gWeighted.shortestPath((u,v)))
for u in gD.vertices():
    for v in gD.vertices():
        print("Path from:",u, " to:",v,end=" ::")
        print(gD.shortestPath((u,v)))
for u in gDAG.vertices():
    for v in gDAG.vertices():
        print("Path from:",u, " to:",v,end=" ::")
        print(gDAG.shortestPath((u,v)))
'''
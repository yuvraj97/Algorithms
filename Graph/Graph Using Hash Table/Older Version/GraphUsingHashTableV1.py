# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 05:00:16 2019

@author: Yuvraj
"""

# Here we uses Hash Table to implement Adjacency List
# vertices works as key (indexof hashTable) and the neighbours as there values
# each neighbour has its own value initially it's None but we can use it in numerous ways
# like when solving for travelling salesman value of each neighbour represents
# cost from the key to it's value. Mean cost associated  from one node to the another

# to use OpenAddressing Hash Table just uncomment line number 16 and comment line number 17
# to use Chaining Hash Table just uncomment line number 17 and comment line number 16
import lib.OpenAddressing as ht
#import lib.HashTable as ht
import lib.LinkedList as ll
import lib.load

# Arguments in AdjacencyList
# Here vertices is a list,array of vertices(that can be int or string)
# edges should be a list or array(numpy) of edge, containing a list,tuple,array of two vertices
# and 3rd item(i.e. value of the edge) IF IT EXIST
# that can be like cost of the edge like in minimum spanning tree 
# isUndirectedGraph represent is the graph is directed or not if value set to False => Directed Graph

class AdjacencyList():    
    def __init__(self, vertices = None, edges = None, isUndirectedGraph = True, dtype=str):
        self._hashTable_ = ht.HashTable()
        self.noVertices = 0
        self.noEdges = 0
        self.dtype = dtype
        self.isUndirectedGraph = isUndirectedGraph
        if(vertices!=None):
            self.initializeVertices(vertices)
        if(edges!=None):
            self.initializeEdge(edges)

# =============================================================================

    # Usage: len(a)
    # a: AdjacencyList object and len(a) will return number of vertices
    def __len__(self):
        return self.noVertices

# =============================================================================
    
    # Usage:
    # for neig in a[V]:
    #    operation_wanna_performe_on_that_neighbour(neig)
    # here a: AdjacencyList object, and let say e wanna find neighbours of a vertex say V
    # It will return a itterator that will give you neighbours associated with given vertex
    def __getitem__(self,vertex):
        vertex = self.dtype(vertex)
        llist = self._hashTable_[vertex]    # self._hashTable_[vertex] will give us a itterator of LinkedList
        if(llist == None): return
        for node in llist:   
            yield node

# =============================================================================
    
    # Usage: a[startVertex] = endVertex
    # it will create a edge in b/w startVertex and endVertex, here a: AdjacencyList object
    def __setitem__(self,startVertex,endVertex):
        self.addNewEdge((startVertex,endVertex))

# =============================================================================

    # Usage: del h[vertex]
    # it will delete the vertex and all the edge connected to that vertex
    def __delitem__(self,key):
        self.deleteVertex(key)

# =============================================================================

    def noOfEdges(self):
        return self.noEdges
    
    def noOfVertices(self):
        return self.noVertices
# =============================================================================
    
    # Usage: here a: AdjacencyList object
    #    for list_of_vertex_with_its_neig in a:
    #        operation_wanna_performe_on_that_list(list_of_vertex_with_its_neig)
    def __iter__(self):
        for key_Vertex, value_LinkedList in self._hashTable_:   # here we ittertively get key, value pair of our hashTable; key is the vertex and the value is LinkedList of neighbours
            y = [key_Vertex,[]]                                 # In y we store a vertex as it's 1st element and list of the neighbours of that vertex as 2nd element
            for key, val in value_LinkedList:                   # Here now LinkedList will ittertively get it's nodes key, value pair
                y[1].append(key)                                # we has stored neighbours as key
            yield y

# =============================================================================

    # Usage: a.initializeVertices(vertices_list)
    # Here vertices is a list of vertices(that can be int or string)
    def initializeVertices(self,vertices_list):
        if(len(vertices_list) == 0): return
        for vertex in vertices_list:
            self.addNewVertex(vertex)

# =============================================================================
            
    # Usage: a.initializeEdge(edges_list):
    # Edges should be a list or array(numpy) of edge
    # edge contains a list,tuple,array of two vertices
    # and 3rd item(i.e. value of the edge) IF IT EXIST
    # that can be like cost of the edge like in minimum spanning tree
    def initializeEdge(self,edges_list):
        if(len(edges_list)==0): return
        for edge in edges_list:
            self.addNewEdge(edge)

# =============================================================================
    
    # Usage: a.addNewVertex(vertex)
    # vertex can be int or string
    def addNewVertex(self,vertex):
        vertex = self.dtype(vertex)
        if(self._hashTable_[vertex] == None):
            self.noVertices += 1
        self._hashTable_[vertex] = ll.LinkedList()

# =============================================================================
    
    # edge must be a tuple of size either 2(startVertex, endVertex) or 3(startVertex, endVertex, value)
    def addNewEdge(self,edge):
        if(type(edge) != tuple or len(edge) == 0):
            return
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        if(len(edge)==3):
            value = edge[2]
        else:
            value = None
        llist = self._hashTable_[startVertex]  # # llist specifies LinkedList object
        if(llist == None): return
        if(llist.find(endVertex) != None): return
        self.noEdges += 1
        #print("Adding edge:",startVertex,endVertex)
        llist.add(endVertex,value)
        if(self.isUndirectedGraph):
            llist = self._hashTable_[endVertex]
            if(llist == None): return
            if(llist.find(startVertex) != None): return
            llist.add(startVertex,value)
            #print("Adding edge:",endVertex,startVertex)
            
# =============================================================================
    
    # vertex can be int or string
    def neighbour(self,vertex):
        vertex = self.dtype(vertex)
        llist = self._hashTable_[vertex]    # self._hashTable_[vertex] will give us a itterator of LinkedList
        if(llist == None): return
        for node in llist:   
            yield node

# =============================================================================
    
    # vertex can be int or string
    def deleteVertex(self,vertex):
        vertex = self.dtype(vertex)
        # Here we visit all of its neighbour and remove vertex from there neighbour
        for neig_key,neig_val in self[vertex]:
            llist = self._hashTable_[neig_key] # llist specifies LinkedList object
            llist.remove(vertex)
        del self._hashTable_[vertex]

# =============================================================================

    def deleteEdge(self,edge):
        if(type(edge) != tuple or len(edge) == 0):
            return
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        llist = self._hashTable_[startVertex]
        llist.remove(endVertex)
        if(self.isUndirectedGraph):
            llist = self._hashTable_[endVertex]
            llist.remove(startVertex)

# =============================================================================
    
    def BFS(self,vertex):
        vertex = self.dtype(vertex)
        # Here we require to index by our vertices but its not sure that our vertices are represented by numbers
        # thats why we use hashTable otherwise there is a simpler implementation of same code using list,numpy array insted of hashtable :)
        # so we use hashTable insted
        level,parent = ht.HashTable(),ht.HashTable()
        i = 1
        level[vertex] = 0
        parent[vertex] = None
        frontier = [vertex]
        while(frontier):
            next = []
            for u in frontier:
                for v_key,v_value in self[u]:
                    if v_key not in level:
                        level[v_key] = i
                        parent[v_key] = u
                        next.append(v_key)
            frontier = next
            i += 1
        return level, parent

# =============================================================================
    
    def shortestDistance(self,startVertex,endVertex):
        startVertex,endVertex = self.dtype(startVertex), self.dtype(endVertex)
        level, parent = self.BFS(startVertex)
        l = []
        while endVertex != None:
            l.append(endVertex)
            temp = parent[endVertex]
            endVertex = temp
        if(len(l) == 1 ): return
        l.reverse()
        return l

# =============================================================================

def createRandomGraph(no_of_vertices=3100,no_of_edges=3200):
    from random import randrange
    g = AdjacencyList(dtype=int)
    vertices = [i for i in range(no_of_vertices)]
    g.initializeVertices(vertices)
    ittr = 0
    #print(i, no_of_edges)
    while(ittr < no_of_edges):
        startVertex = randrange(0,no_of_vertices)
        endVertex = randrange(0,no_of_vertices)
        g.addNewEdge((startVertex,endVertex))
        ittr = g.noOfEdges()
    return g

# =============================================================================

# If we have data of graphs in a file as shown in GraphDataset.csv and SingleDataset.csv file
# It will take input a list that contain multiple lists or single graph.
# Elements of this List contains a list that contains 2 lists
# One list contain list of vertices and Second contains list of edges
def load(path):
    print("Loading DataSet...")
    no_graphs, graph_array=lib.load.load2(path);
    if(no_graphs == 1): return AdjacencyList(graph_array[0][0],graph_array[0][1])
    obj = []
    for i in range(len(graph_array)):
        obj.append(AdjacencyList(graph_array[i][0],graph_array[i][1]))
    print("DataSet Loaded.")
    return obj

# =============================================================================

################################## Example ####################################
'''
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

g = AdjacencyList(vertices,edges)

# Iterrate over the graph
for neig in g:
    print(neig)
# Output:
# ['4', ['1', '2', '3']]
# ['0', ['1', '2', '3']]
# ['2', ['0', '1', '3', '4']]
# ['3', ['0', '2', '4']]
# ['1', ['0', '2', '4']]

# To get neighbour of any vertex V say V = 3
neig = [key for key,val in g[3]]
print(neig)   # Output: ['0', '2', '4']

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

# To get the shortest distance b/w 2 nodes Lets say you wanna find shortest distance b/w 1 and 3
# g.shortestDistance(startVertex,endVertex)             # It will return a list of vertices showing path
g = AdjacencyList(vertices,edges)
l = g.shortestDistance(1,3)
print(l)
'''

######################## If you have the node in a file ##########################

'''
#path = 'C:\\Users\\Yuvraj\\Desktop\\py\\Graph\\SpanningTree\\SpanningTreeDataset2.csv'
path = 'C:\\Users\\Yuvraj\\Desktop\\py\\Graph\\SingleDataset.csv'
g = load(path) # Say if you have only 1 graph in your file
#print(g)        # Out: <__main__.AdjacencyList at 0xb0798d0>

# Now you have your variable g now you can do as describe above
'''
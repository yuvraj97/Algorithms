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

import lib.OpenAddressing as ht
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
        self._isNegativeEdges_ = False
        self._isWeighted_ = False
        self.isUndirectedGraph = isUndirectedGraph
        self._order_ = []
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
        return self.__neighbourVert__(vertex)

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
        for k in self._order_:
            key_Vertex, value = k, self._hashTable_[k]
            y = [key_Vertex,[]]
            for key, val in value:
                if(val != None):
                    y[1].append((key,val))
                else:
                    y[1].append(key)
            yield y

# =============================================================================

    def __str__(self):
        s = '{\n'
        flag = False
        for v,e in self:
            s = s + '\t' + str(v) + ": ["
            for edge in e:
                s = s + str(edge) + ', '
                flag = True
            if(flag):
                s = s[:-2]
            s += ']'
            flag = False
            s += '\n'
        s += '}'
        return  s
            
# =============================================================================

    def vertices(self):
        for vert,edge in self:
            yield vert

    def edges(self):
        for vertex,neig in self._hashTable_:
            for k,v in neig:
                yield (vertex,k,v)
    
    def getVertices(self):
        return [ v for v in self.vertices() ]

    def getEdges(self):
        return [e for e in self.edges()]
    
# =============================================================================

    def copy(self):
        g = AdjacencyList(self.getVertices(), self.getEdges(), isUndirectedGraph=self.isUndirectedGraph, dtype=self.dtype)
        return g

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
        self._hashTable_[vertex] = ht.HashTable()
        self._order_.append(vertex)

# =============================================================================

    def __edgeCondition__(self,edge):
        if(type(edge) != tuple): raise ValueError('Argument must be tuple')
        if(len(edge) == 0): raise ValueError('Length of tuple must not be 0')
        if(len(edge) > 3):  raise ValueError('Length of tuple must not be greater then 3')
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        if startVertex not in self._hashTable_: raise ValueError(startVertex,' is not a Vertex')
        if endVertex not in self._hashTable_: raise ValueError(endVertex,' is not a Vertex')
        
    # edge must be a tuple of size either 2(startVertex, endVertex) or 3(startVertex, endVertex, value)
    def addNewEdge(self,edge):
        self.__edgeCondition__(edge)
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        if(self._hashTable_[startVertex][endVertex] != None): return
        if(len(edge)==3):
            value = edge[2]
            if(value != None):
                self._isWeighted_ = True
                if(value < 0):
                    self._isNegativeEdges_ = True
        else:
            value = None
        table = self._hashTable_[startVertex]
        if(table == None): return
        if(table[endVertex] != None): return
        self.noEdges += 1
        table[endVertex] = value
        if(self.isUndirectedGraph):
            table = self._hashTable_[endVertex]
            if(table == None): return
            if(table[startVertex] != None): return
            table[startVertex] = value

    def getValueOf(self,edge):
        self.__edgeCondition__(edge)
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        return self._hashTable_[startVertex][endVertex]
    
    def setValueOf(self,edge,value):
        self.__edgeCondition__(edge)
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        self._hashTable_[startVertex][endVertex] = value
        if(value == None and self.isUndirectedGraph):
            print("Warning: your graph is undirected and you had set a value to an edge")
            print("You can undo it by again setting the value to None")

# =============================================================================
    
    # vertex can be int or string
    def __neighbourNode__(self,vertex):
        vertex = self.dtype(vertex)
        table = self._hashTable_[vertex]    # self._hashTable_[vertex] will give us a itterator of LinkedList
        if(table == None): return
        for node in table:   
            yield node
    
    def __neighbourVert__(self,vertex):
        for k, v in self.__neighbourNode__(vertex):
            yield k

    def getNeighbour(self,vertex):
        return [n for n in self[vertex]]
    
# =============================================================================
    
    # vertex can be int or string
    def deleteVertex(self,vertex):
        vertex = self.dtype(vertex)
        # Here we visit all of its neighbour and remove vertex from there neighbour
        for neig_key in self[vertex]:
            table = self._hashTable_[neig_key] # llist specifies LinkedList object
            del table[vertex]
        del self._hashTable_[vertex]

# =============================================================================

    def deleteEdge(self,edge):
        self.__edgeCondition__(edge)
        if(type(edge) != tuple or len(edge) == 0):
            return
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        table = self._hashTable_[startVertex]
        del table[endVertex]
        if(self.isUndirectedGraph):
            table = self._hashTable_[endVertex]
            del table[startVertex]
    
# =============================================================================
    
    def __cycleDFSHelper__(self,vertex,parent,l):
        for neig_vert in self[vertex]:
            if neig_vert not in parent:
                parent[neig_vert] = vertex
                l.append(neig_vert)
                yield neig_vert
                yield from self.__cycleDFSHelper__(neig_vert,parent,l)
                l.pop()

# =============================================================================

    def isCycleExist(self):             # Time complexity O(|V| + |E|), Space complexity O(|V|)
        parent = ht.HashTable()         # parent is a HashTable of visited vertices Space Complexity: O(|V|)
        for vertex in self.vertices():  # Time complexity O(|V|), Space complexity O(|V|)
            l = [vertex]                # l is a list of vertices reachable from vertex Space Complexity: O(|V|)
            if vertex not in parent:    # parent is a HashTable so Time complexity O(1)
                parent[vertex] = None
                for next_vert in self.__cycleDFSHelper__(vertex,parent,l):  # Space Complexity: O(1), Time Complexity: O(|V|)
                    for i in range(len(l)):   # in case of unDirected we dont check for last vertex in l
                        if(self.isUndirectedGraph == True and i == len(l) - 2): continue
                        startVert, endVert = next_vert, l[i]
                        table = self._hashTable_[startVert]
                        if(endVert in table):   return True   # table  is a HashTable so Time complexity O(1)
        return False

# =============================================================================

    def __topologicalSort__(self,vertex,parent,l):
        for neig in self[vertex]:
            if neig not in parent:
                parent[neig] = None
                self.__topologicalSort__(neig,parent,l)
                l.append(neig)
    
# =============================================================================

    def topologicalSort(self):
        if(self.isUndirectedGraph): return
        if(self.isCycleExist()): return
        parent = ht.HashTable()
        l = []
        for vert in self.vertices():
            if(vert not in parent):
                parent[vert] = None
                self.__topologicalSort__(vert,parent,l)
                l.append(vert)
        l.reverse()
        return l

# =============================================================================

    def shortestPath(self,startVertex,endVertex):
        path = self.topologicalSort()
        dist, parent = ht.HashTable(),ht.HashTable()
        dist[startVertex] = 0
        parent[startVertex] = None
        startVertexFound = False
        for vertex in path:
            if(vertex == startVertex): startVertexFound = True
            if(not startVertexFound):  continue
            if(dist[vertex] == None): continue
            for neig,weight in self.__neighbourNode__(vertex):
                if(dist[neig] == None or dist[neig] > dist[vertex] + weight):
                    dist[neig] = dist[vertex] + weight
                    parent[neig] = vertex
        l=[]
        startVertexFound = False
        curr = endVertex
        wt = 0
        while(curr !=None):
            l.append(curr)
            end = curr
            curr = parent[curr]
            if(curr!=None): wt += self.getValueOf((curr,end))
            if(curr == startVertex):
                startVertexFound = True
                l.append(startVertex)
                break
        l.reverse()
        if(startVertexFound):
            return l,wt
        else:
            return None

# =============================================================================
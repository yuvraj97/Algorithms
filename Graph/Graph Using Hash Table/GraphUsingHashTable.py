# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 05:00:16 2019

@author: Yuvraj
"""

# Main diffrence in this and previous version is that I replaced LinkedList with HashTable
# And also implemented some more methods like for: BFS, DFS, Cycle Detection

# Here we uses Hash Table to implement Adjacency List
# vertices works as key (indexof hashTable) and the neighbours as there values
# each neighbour has its own value initially it's None but we can use it in numerous ways
# like when solving for travelling salesman value of each neighbour represents
# cost from the key to it's value. Mean cost associated  from one node to the another

# to use OpenAddressing Hash Table just uncomment line number 19 and comment line number 20
# to use Chaining Hash Table just uncomment line number 20 and comment line number 19
import lib.OpenAddressing as ht
#import lib.HashTable as ht
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
        for key_Vertex, value in self._hashTable_:   # here we ittertively get key, value pair of our hashTable; key is the vertex and the value is LinkedList of neighbours
            y = [key_Vertex,[]]                                 # In y we store a vertex as it's 1st element and list of the neighbours of that vertex as 2nd element
            for key, val in value:                   # Here now LinkedList will ittertively get it's nodes key, value pair
                y[1].append(key)                                # we has stored neighbours as key
            yield y

# =============================================================================

    def vertices(self):
        for vert,edge in self:
            yield vert

    def edges(self):
        for vertex,neig in self._hashTable_:
            for k,v in neig:
                yield (vertex,k)
    
    def getVertices(self):
        return [ v for v in self.vertices() ]

    def getEdges(self):
        return [e for e in self.edges()]
    
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

# =============================================================================

    def __edgeCondition__(self,edge):
        if(type(edge) != tuple): raise ValueError('Argument must be tuple')
        if(len(edge) == 0): raise ValueError('Length of tuple must not be 0')
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
        else:
            value = None
        table = self._hashTable_[startVertex]  # # llist specifies LinkedList object
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
        if(type(edge) != tuple or len(edge) == 0):
            return
        startVertex, endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        table = self._hashTable_[startVertex]
        del table[endVertex]
        if(self.isUndirectedGraph):
            table = self._hashTable_[endVertex]
            del table[startVertex]

# =============================================================================
    
    def BFS(self,vertex):
        vertex = self.dtype(vertex)
        # Here we require to index by our vertices but its not sure that our vertices are represented by numbers
        # thats why we use hashTable otherwise there is a simpler implementation of same code using list,numpy array insted of hashtable :)
        # so we use hashTable insted
        level,parent = ht.HashTable(),ht.HashTable()
        i = 1
        level[vertex], parent[vertex] = 0, None
        frontier = [vertex]
        while(frontier):
            next = []
            for u in frontier:
                for v_key in self[u]:
                    if v_key not in level:
                        level[v_key] = i
                        parent[v_key] = u
                        next.append(v_key)
            frontier = next
            i += 1
        return level, parent

# =============================================================================
    
    def shortestPathBFS(self,startVertex,endVertex):
        for v,e in self._hashTable_:
            for k,v in e:
                if(v!=None): raise ValueError('Graph Must Not be Weighted. For Weighted Graph you can use shortestPathWeighted() method')
                break
            break
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

    # Usage:
    # for vert in g.DFS(vertex):
    #    operation_with_vert(vert)     
    def DFS(self,v):
        if(type(v) == list):
            yield from self.__DFS_List__(v)
        else:
            vertex = self.dtype(v)
            parent = ht.HashTable()
            parent[vertex] = None
            yield vertex
            yield from self.__DFS_Vertex__(vertex,parent)

    def __DFS_List__(self,vertices):
        #vertex = self.dtype(vertex)
        parent = ht.HashTable()
        for vertex in vertices:
            if vertex not in parent:
                l=[vertex]
                parent[vertex] = None
                for v in self.__DFS_Vertex__(vertex,parent): l.append(v)
                yield l

    def __DFS_Vertex__(self,vertex,parent):
        for neig_vert in self[vertex]:
            if neig_vert not in parent:
                parent[neig_vert] = vertex
                yield neig_vert
                yield from self.__DFS_Vertex__(neig_vert,parent)

    def __getDFSParentHashTable__(self,vertex):
        vertex = self.dtype(vertex)
        parent = ht.HashTable()
        parent[vertex] = None
        [ next_vert for next_vert in self.__DFS_Vertex__(vertex,parent)]
        return parent

    # It will return list of DFS of the vertex
    def getDFS(self,vertex):
        vertex = self.dtype(vertex)
        return [i for i in self.DFS(vertex)]

    def __cycleDFSHelper__(self,vertex,parent,l):
        for neig_vert in self[vertex]:
            if neig_vert not in parent:
                parent[neig_vert] = vertex
                l.append(neig_vert)
                yield neig_vert
                yield from self.__cycleDFSHelper__(neig_vert,parent,l)
                l.pop()

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
    
    def __jobSchedule__(self,vertex,parent,l):
        for neig in self[vertex]:
            if neig not in parent:
                parent[neig] = None
                self.__jobSchedule__(neig,parent,l)
                l.append(neig)
    
    def jobSchedule(self):
        if(self.isUndirectedGraph): return
        if(self.isCycleExist()): return
        parent = ht.HashTable()
        l = []
        for vert in self.vertices():
            if(vert not in parent):
                parent[vert] = None
                self.__jobSchedule__(vert,parent,l)
                l.append(vert)
        l.reverse()
        return l

# =============================================================================

    # 8-Feb-2019    
    # Here we uses BFS technique but we had handeled the repetation of path in an efficient manner
    def __shortestPathWeighted__(self,startVertex,parent,record,recursionTrace,rescueRepetition):
        for neig in self[startVertex]:
            if(neig not in recursionTrace):
                weight = self._hashTable_[startVertex][neig]
                if(record[neig] == None):
                    record[neig] = weight + record[startVertex]
                    parent[neig] = startVertex
                elif(record[neig] > weight + record[startVertex]):
                    record[neig] = weight + record[startVertex]
                    parent[neig] = startVertex
                elif(record[neig] <= weight + record[startVertex]):     # Here we are recording the that has weight > current weight
                    if(startVertex not in rescueRepetition):            # In recursive call we will make sure that these edges should not be taken into consideraton
                        rescueRepetition[startVertex] = ht.HashTable()
                        rescueRepetition[startVertex][neig] = None
                    else:
                        rescueRepetition[startVertex][neig] = None
        for neig in self[startVertex]:
            if(neig not in recursionTrace):# and neig not in rescueRepetition):
                if(startVertex in rescueRepetition and neig in rescueRepetition[startVertex]):
                    pass
                else:
                    recursionTrace[neig] = startVertex
                    self.__shortestPathWeighted__(neig,parent,record,recursionTrace,rescueRepetition)
                    del recursionTrace[neig]
                if(startVertex in rescueRepetition and neig in rescueRepetition[startVertex]):
                    del rescueRepetition[startVertex][neig]

    def shortestPathWeighted(self,startVertex,endVertex):
        for v,e in self._hashTable_:
            for k,v in e:
                if(v==None): raise ValueError('Graph Must be Weighted. For an unweighted Graph you can use  shortestPathBFS() method')
                break
            break
        record, parent = ht.HashTable(), ht.HashTable()
        record[startVertex] = 0
        parent[startVertex] = None
        recursionTrace,rescueRepetition = ht.HashTable(), ht.HashTable()
        self.__shortestPathWeighted__(startVertex,parent,record,recursionTrace,rescueRepetition)
        l=[endVertex]
        while(endVertex!=None):
            endVertex=parent[endVertex]
            l.append(endVertex)
        l.pop()
        l.reverse()
        return l
    
# =============================================================================

def createRandomGraph(no_of_vertices=3100,no_of_edges=3200,isUndirected = True):
    from random import randrange
    g = AdjacencyList(dtype=int,isUndirectedGraph=isUndirected)
    vertices = [i for i in range(no_of_vertices)]
    g.initializeVertices(vertices)
    ittr = 0
    while(ittr < no_of_edges):
        startVertex = randrange(0,no_of_vertices)
        endVertex = randrange(0,no_of_vertices)
        g.addNewEdge((startVertex,endVertex))
        ittr = g.noOfEdges()
    return g

# =============================================================================

# If we have data of graphs in a file as shown in DataSet
def load(path,isUndirected = True):
    print("Loading DataSet...")
    vertices,edges=lib.load.load2(path);
    return AdjacencyList(vertices,edges,isUndirectedGraph=isUndirected)    

# =============================================================================

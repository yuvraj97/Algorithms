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

# to use OpenAddressing Hash Table just comment 'import lib.HashTable as ht' and uncomment 'import lib.OpenAddressing as ht'
# to use Chaining Hash Table just comment import lib.OpenAddressing as ht and uncomment 'import lib.HashTable as ht'
import lib.OpenAddressing as ht
#import lib.HashTable as ht
import lib.load
# Use of lib.HashTable is not supported more you may face errors using lib.HashTable
# But you can use it for learning

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
            y = [key_Vertex,[]]                      # In y we store a vertex as it's 1st element and list of the neighbours of that vertex as 2nd element
            for key, val in value:
                if(val != None):
                    y[1].append((key,val))
                else:
                    y[1].append(key)
            yield y

# =============================================================================

    def __str__(self):
        s = '{\n'
        for v,e in self:
            s = s + '\t' + str(v) + ": ["
            for edge in e:
                s = s + str(edge) + ', '
            s = s[:-2]
            s += ']\n'
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
    
    def __shortestPathBFS__(self,edge):
        if(self._isWeighted_): raise ValueError('Graph Must Not be Weighted. For Weighted Graph you can use shortestPath() method')
        self.__edgeCondition__(edge)
        startVertex,endVertex = self.dtype(edge[0]), self.dtype(edge[1])
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
    
    def __topologicalSort__(self,vertex,parent,l):
        for neig in self[vertex]:
            if neig not in parent:
                parent[neig] = None
                self.__topologicalSort__(neig,parent,l)
                l.append(neig)
    
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

    def shortestPath(self,edge,whichMethod="None"):
        self.__edgeCondition__(edge)
        if(not self._isWeighted_):
            return self.__shortestPathBFS__(edge)
        whichMethod = whichMethod.lower()
        startVertex,endVertex = self.dtype(edge[0]), self.dtype(edge[1])
        if(startVertex == endVertex): 
            val = self._hashTable_[startVertex][startVertex]
            if(val == None): val = 0
            return ([startVertex,startVertex],val)
        s = __ShortestPath__()
        if(whichMethod=="t"):
            return s.byTransformation(self,startVertex,endVertex)
        elif(whichMethod=='d'):
            return s.dijkstra(self,startVertex,endVertex)
        elif(whichMethod=='test'):
            return s.shortestPathWeighted(self,startVertex,endVertex)
        elif(whichMethod=='d1'):
            if(self._isNegativeEdges_): raise ValueError("Dijkstra don't accept negative vertices")
            return s.dijkstraV1(self,startVertex,endVertex)
        elif(whichMethod=='d2'):
            if(self._isNegativeEdges_): raise ValueError("Dijkstra don't accept negative vertices")
            return s.dijkstraV2(self,startVertex,endVertex)
        elif(whichMethod=='b'):
            return s.bellman_ford(self,startVertex,endVertex)
        if(not self._isNegativeEdges_):
            return s.dijkstraV2(self,startVertex,endVertex)
        else:
            return s.bellman_ford(self,startVertex,endVertex)

# =============================================================================

# If we have data of graphs in a file as shown in DataSet
def load(path,isUndirected = True):
    print("Loading DataSet...")
    vertices,edges=lib.load.load2(path);
    return AdjacencyList(vertices,edges,isUndirectedGraph=isUndirected)    

# #############################################################################
# ######################## Shortest Path Algorithms ###########################
# #############################################################################
    
class __ShortestPath__:
    
    # 8-Feb-2019
    def __shortestPathWeighted__(self,graph,startVertex,parent,record,recursionTrace,rescueRepetition):
        for neig in graph[startVertex]:
            if(neig not in recursionTrace):
                weight = graph._hashTable_[startVertex][neig]
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
        for neig in graph[startVertex]:
            if(neig not in recursionTrace):# and neig not in rescueRepetition):
                if(startVertex in rescueRepetition and neig in rescueRepetition[startVertex]):
                    pass
                else:
                    recursionTrace[neig] = startVertex
                    self.__shortestPathWeighted__(graph,neig,parent,record,recursionTrace,rescueRepetition)
                    del recursionTrace[neig]
                if(startVertex in rescueRepetition and neig in rescueRepetition[startVertex]):
                    del rescueRepetition[startVertex][neig]

# =============================================================================
            
    def shortestPathWeighted(self,graph,startVertex,endVertex):
        record, parent = ht.HashTable(), ht.HashTable()
        record[startVertex] = 0
        parent[startVertex] = None
        recursionTrace,rescueRepetition = ht.HashTable(), ht.HashTable()
        self.__shortestPathWeighted__(graph,startVertex,parent,record,recursionTrace,rescueRepetition)
        l=[endVertex]
        while(endVertex!=None):
            endVertex=parent[endVertex]
            l.append(endVertex)
        l.pop()
        l.reverse()
        return l

# =============================================================================
    
    def byTransformation(self,graph,startVertex,endVertex):
        new_edges=[]
        new_vertices=[]
        for start,end,val in graph.edges():
            if(val > 1):
                prev_v = start
                next_v = str('%')+str(start)+str(end)+str(0)
                for i in range(val-1):
                    new_vertices.append(next_v)
                    new_edges.append((prev_v,next_v))
                    prev_v = next_v
                    next_v = str('%')+str(start)+str(end)+str(i+1)
                new_vertices.append(next_v)
                new_edges.append((prev_v,end))
        new_vertices.extend(graph.getVertices())
        g1 = AdjacencyList(new_vertices,new_edges)
        path = g1.getBFSPath((startVertex,endVertex))
        l = []
        for s in path:
            if s[0] != '%':
                l.append(s)
        return l

# =============================================================================

    # 10-Feb-2019
    # O(V^2 + E)
    def dijkstraV1(self,graph,startVertex,endVertex):
        if(startVertex == endVertex): return [startVertex,endVertex], 0
        if(graph._isNegativeEdges_): return
        def extract_min(dist,Q):    # O(|V|)
            minimum, ret_vert = None, None
            for vert, dump in Q:
                weight = dist[vert]
                if(weight == None): continue
                if(minimum == None):
                    minimum = weight
                    ret_vert = vert
                else:
                    if(weight < minimum):
                        minimum = weight
                        ret_vert = vert
            return minimum,ret_vert
        # Initialization
        V = graph.getVertices()
        Q = ht.HashTable()
        for vert in V:  Q[vert] = None
        parent = ht.HashTable()
        for vert in V:  parent[vert] = None
        dist = ht.HashTable()
        for vert in V:  dist[vert] = None
        dist[startVertex] = 0
        
        # Dijkstra Algorithm
        while(len(Q) != 0):
            minimum, vert = extract_min(dist,Q)
            if(vert == None): break
            del Q[vert]
            for vertex,weight in graph.__neighbourNode__(vert):
                if(dist[vertex] == None or dist[vertex] >  dist[vert] + weight):
                    dist[vertex] = dist[vert] + weight
                    parent[vertex] = vert
        return self.__htable_to_list__(parent,dist,endVertex)
        
# =============================================================================
    
    # 11-Feb-2019
    # O( V*lg(V) + E*lg(V) )
    def dijkstraV2(self,graph,startVertex,endVertex):
        # =====================================================================
        def extract_min(q):
            q[-1][3]=0
            q[0],q[-1] = q[-1], q[0]
            ret = q.pop()
            min_heapify(q,len(q),0)
            return ret
        # =====================================================================
        def min_heapify(a,n,i):     # O(lg(V))
            if(2*i + 1 < n):
                if(a[i][0] == None and a[2*i + 1][0] != None):
                    a[i], a[2*i + 1] = a[2*i + 1], a[i]
                    a[i][3], a[2*i + 1][3] = a[2*i + 1][3], a[i][3]
                    min_heapify(a,n,2*i + 1)
                elif(a[i][0]!=None and a[2*i + 1][0] !=None):
                    if(a[i][0] > a[2*i + 1][0]):
                        a[i], a[2*i + 1] = a[2*i + 1], a[i]
                        a[i][3], a[2*i + 1][3] = a[2*i + 1][3], a[i][3]
                        min_heapify(a,n,2*i + 1)
            if(2*i + 2 < n):
                if(a[i][0] == None and a[2*i + 2][0] != None):
                    a[i], a[2*i + 2] = a[2*i + 2], a[i]
                    a[i][3], a[2*i + 2][3] = a[2*i + 2][3], a[i][3]
                    min_heapify(a,n,2*i + 2)
                elif(a[i][0] != None and a[2*i + 2][0] != None):
                    if(a[i][0] > a[2*i + 2][0]):
                        a[i], a[2*i + 2] = a[2*i + 2], a[i]
                        a[i][3], a[2*i + 2][3] = a[2*i + 2][3], a[i][3]
                        min_heapify(a,n,2*i + 2)
        # =====================================================================
        def move_up(Q,H,vertex):    #O(lg(V))
            vertex = vertex[1]
            curr_Q = H[vertex]
            index = curr_Q[3]
            while(index>0):
                parent_index = (index - 1)//2
                if(Q[parent_index][0] == None or Q[parent_index][0] > Q[index][0]):
                    Q[parent_index], Q[index] =  Q[index], Q[parent_index]
                    Q[parent_index][3], Q[index][3] =  Q[index][3], Q[parent_index][3]
                else:
                    break
                index = parent_index
        # =====================================================================
        def relax(u,v,weight,Q,H):    # O(lg(V))
            curr_Q_value_v = H[v]     # it will go to H and return list refrence from Q of vertex v
            curr_Q_value_u = H[u]
            if(curr_Q_value_v[0] == None or curr_Q_value_v[0] > curr_Q_value_u[0] + weight):
                curr_Q_value_v[0] = curr_Q_value_u[0] + weight
                curr_Q_value_v[2] = u
                move_up(Q,H,curr_Q_value_v)
        # =====================================================================
        
        if(graph._isNegativeEdges_):
            return
        # Initialization
        Q = [[0,startVertex,None,0]] # Here Q will record the distance path b/w vertices 1st element: cost, 2nd element: vertex, 3rd element: parent, 4th element: index
        H = ht.HashTable()           # we require this hashTable cause in relax part if we don't use hash table then
                                     # to updating the cost of vertex v in Q we have to scan whole array Q to find v and then update cost
        i = 0                        # H provides us element of Q in O(1) i.e. it will give us Q[v] in O(1)
        H[startVertex] = Q[i] 
        for vertex in graph.vertices():
            if(vertex == startVertex):  continue
            i += 1
            Q.append([None,vertex,None,i])
            H[vertex] = Q[i]
        S = []
        
        # Dijkstra Algorithm
        while(len(Q) != 0):
            u = extract_min(Q)
            S.append(u)
            if(u[0] == None): break
            for vertex,weight in graph.__neighbourNode__(u[1]):
                relax(u[1],vertex,weight,Q,H)
                
        # Finally return the path
        parent = ht.HashTable()
        weig = ht.HashTable()
        for i in range(len(S)):
            parent[S[i][1]] = S[i][2]
            weig[S[i][1]] = S[i][0]
        return self.__htable_to_list__(parent,weig,endVertex)

# =============================================================================
    
    # 11-Feb-2019
    def bellman_ford(self,graph,startVertex,endVertex):
        def relax(u,v,w,dist,parent):
            if(dist[u] == None): return
            if(dist[v] == None or dist[v] > dist[u] + w):
                dist[v] = dist[u] + w
                parent[v] = u

        # Initialization
        parent = ht.HashTable()
        dist = ht.HashTable()
        for vert in graph.vertices():
            parent[vert],dist[vert] = None,None
        dist[startVertex] = 0
        
        # Bellman-Ford Algo
        for _ in range(graph.noOfVertices()):
            for u,v,w in graph.edges():
                relax(u,v,w,dist,parent)
        # Check  if there is any -ve cycle in path of startVertex
        for u,v,w in graph.edges():
            if(dist[u] == None):continue
            if(dist[v] > dist[u] + w):  return None
        return self.__htable_to_list__(parent,dist,endVertex)

# =============================================================================
    
    def __htable_to_list__(self,parent,dist,endVertex):
        l = [endVertex]
        weight = dist[endVertex]
        while(endVertex != None):
            endVertex = parent[endVertex]
            l.append(endVertex)
        l.pop()
        l.reverse()
        if(len(l)==1): return  None
        return (l,weight)

###############################################################################
'''
path = 'C:\\Users\\Yuvraj\\Desktop\\py\\Graph\\Weigted\\Graph 1.csv'
g = load(path,isUndirected=False)
u,v = 'S','E'
p1 = g.shortestPath((u,v))
print(p1)
'''
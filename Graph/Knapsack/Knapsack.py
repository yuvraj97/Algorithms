# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 01:43:42 2019

@author: Yuvraj
"""

import lib.Graph as graph

# Given weight and values of n items, put them in a Knapsackz of fixed capacity and return:
# 1. the items to put into Knapsack and
# 2. maximum total value. We can get by putting those items into that Knapsack(with fix capacity)


# It return a dictionary of items with random weights and prices
def getRandomItems(capacity = 5, no_of_items = 3, max_price = 10):
    from random import randrange
    items = {}
    for i in range(no_of_items):
        s = "Item:" + str(i + 1)
        price, weight = randrange(0,max_price + 1), randrange(0, capacity + 1)
        items[s] = (price, weight)
    return items

class Knapsack:
    def __init__(self):
        self._items_ = {}
        self._lable_ = {}
        self.capacity = None
        self._graph_ = None
        self._totalItems_  = 0
        self._isInitialized_ = False
        
    def initialize(self,items,capacity):
        self._isInitialized_ = True
        i = 1
        for key in items:
            self._lable_[i] = key
            self._items_[i] = items[key]
            i += 1
        self._totalItems_ = i - 1
        self.capacity = capacity
        self.__buildGraph__()
        
    def updateCapacity(self,capacity):
        if(self._isInitialized_ == False): raise ValueError('Knapsack is not Initialized')
        self.capacity = capacity
        self.__buildGraph__()
        
    def updateItems(self,items):
        if(self._isInitialized_ == False): raise ValueError('Knapsack is not Initialized')
        self.initialize(items,self.capacity)
        
    def __buildGraph__(self):
        self._graph_ = graph.AdjacencyList(isUndirectedGraph=False,dtype=tuple)
        self.__addVertices__()
        self.__addEdges__()
    def __addVertices__(self):
        self._graph_.addNewVertex(("Source",0))
        self._graph_.addNewVertex(("Destination",0))
        for key in self._items_:
            for weight in range(self.capacity + 1):
                self._graph_.addNewVertex((key, weight))
        for i in range(self.capacity + 1):
            self._graph_.addNewVertex((key+1, i))
        
    def __addEdges__(self):
        self.__addEdgesRecursive__(1,0)
        u, v = ("Source",0), (1,0)
        self._graph_.addNewEdge((u, v, 0))
        
        # Connect all Done vertices to destination vertex
        for i in range(self.capacity + 1):
            u, v = (self._totalItems_ + 1, i) , ("Destination",0)
            self._graph_.addNewEdge((u,v,0))
            
    def __addEdgesRecursive__(self, item, currentWeight):
        if(item > self._totalItems_): return
        if(self._items_[item][1] == 0):
            u, v = (item,currentWeight), (item + 1, currentWeight)
            self._graph_.addNewEdge((u,v,-self._items_[item][0]))
            self.__addEdgesRecursive__(item + 1, currentWeight)
        else:
            # Either Don't take the item
            u, v = (item,currentWeight), (item + 1, currentWeight)
            self._graph_.addNewEdge((u,v,0))
            self.__addEdgesRecursive__(item + 1, currentWeight)
            
            # Or take the item
            if(currentWeight + self._items_[item][1] <= self.capacity):
                u, v = (item,currentWeight), (item + 1, currentWeight + self._items_[item][1])
                self._graph_.addNewEdge((u,v,-self._items_[item][0]))
                self.__addEdgesRecursive__(item + 1, currentWeight + self._items_[item][1])
    
    # It will return a list containing 2 things
    # 1st: list items that you should pick to get maximum profit
    # 2nd: amount of profit you are going to make
    def whichItems(self):
        if(self._isInitialized_ == False): raise ValueError('Knapsack is not Initialized')
        u, v = ("Source",0),("Destination",0)
        shortestPath, weight = self._graph_.shortestPath(u,v)
        #print("SP:",shortestPath)
        l = []
        for i in range(len(shortestPath) -1):
            u,v = shortestPath[i],shortestPath[i+1]
            if(self._graph_.getValueOf((u,v)) != 0):
                l.append(shortestPath[i][0])
        l2 = []
        for i in l:
            l2.append(self._lable_[i])
        return l2,-weight
        
# Example:

'''
items = {
        'Golden Statue' : (10,4),    # Golden Statue with price $10 and weight 4lb
        'Crystall ball' : (4, 2),    # Crystall ball with price $4  and weight 2lb
        'Fountain Pen'  : (7, 3),    # Fountain Pen  with price $7  and weight 3lb
        }
capacity = 5                        # Knapsack maximum capacity is 5 lb
k = Knapsack()
k.initialize(items,capacity)
items_to_pick, value = k.whichItems()
print("Pick these items:",items_to_pick)
print("Total value made:",value)
'''


capacity = 5
items = getRandomItems(capacity, no_of_items=5)
for k in items:
    print(k,":",items[k])
k = Knapsack()
k.initialize(items,capacity)
items_to_pick, value = k.whichItems()
print("Pick these items:",items_to_pick)
print("Total value made:",value)

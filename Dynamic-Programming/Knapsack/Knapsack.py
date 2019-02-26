# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 08:12:49 2019

@author: Yuvraj
"""

# Dynamic Programming approch:
# Given weight and values of n items, put them in a Knapsackz of fixed capacity 
# And return maximum total value. We can get by putting those items into that Knapsack(with fix capacity)

# It return a dictionary of items with random weights and prices
def getRandomItems(capacity = 5, no_of_items = 3, max_price = 10):
    from random import randrange
    items = {}
    for i in range(no_of_items):
        s = "Item:" + str(i)
        price, weight = randrange(0,max_price + 1), randrange(0, capacity + 1)
        items[s] = (price, weight)
    return items

class Knapsack:
    def __init__(self):
        self._dp_table_ = []
        self._items_ = {}
        self.capacity = None
        self._totalItems_  = 0
        self._isInitialized_ = False
        self._totalCost_ = 0
        
    def initialize(self,items,capacity):
        self._isInitialized_ = True
        i = 0
        for key in items:
            self._items_[i] = items[key]
            i += 1
        self._totalItems_ = i
        self.capacity = capacity
        self._dp_table_ = [[0]*(self._totalItems_ + 1) for i in range(self.capacity + 1)]
        self._totalCost_ = self.__DP__()
        
    def updateCapacity(self,capacity):
        if(self._isInitialized_ == False): raise ValueError('Knapsack is not Initialized')
        self.capacity = capacity
        self.initialize(self._items_,capacity)
        
    def updateItems(self,items):
        if(self._isInitialized_ == False): raise ValueError('Knapsack is not Initialized')
        self.initialize(items,self.capacity)

    def __DP__(self):
        for i in range(self._totalItems_ - 1, -1, -1):
            for j in range(self.capacity + 1):
                not_take_i     = self._dp_table_[j][i + 1]
                value_of_i, weight_of_i = self._items_[i]
                if(j - weight_of_i < 0): take_i = 0
                else:  take_i = value_of_i + self._dp_table_[j - weight_of_i][i + 1]
                if(take_i > not_take_i):  self._dp_table_[j][i] = take_i
                else:   self._dp_table_[j][i] = not_take_i
        return self._dp_table_[self.capacity][0]
    
    def totalCost(self):
        return self._totalCost_


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
for rows in k._dp_table_:
    print(rows)
print("Max cost you can get:",k.totalCost())
'''


capacity = 5
items = getRandomItems(capacity, no_of_items=3)
for key in items:
    print(key,":",items[key])
k = Knapsack()
k.initialize(items,capacity)
print("Max cost you can get:",k.totalCost())

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 19:39:30 2019

@author: Yuvraj
"""

class Node:
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next
    def destroy(self):
        self.key = None
        self.value = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, key, value):
        if self.head == None:
            self.head = Node(key, value)
            return
        curr = self.head
        while curr.next != None:
            curr = curr.next
        curr.next = Node(key, value)

    def destroy(self):
        curr = self.head
        if(curr == None):
            return
        self.head = None
        while(curr != None):
            temp = curr.next
            curr.destroy()
            curr = temp

    def __iter__(self):
        if(self.head == None):
            return []
        curr = self.head
        while curr.next != None:
            yield (curr.key,curr.value)
            curr = curr.next
        yield (curr.key,curr.value)
        

    def traverse(self):
        if(self.head == None):
            #print("Empty")
            return
        curr = self.head
        while curr.next != None:
            print((curr.key,curr.value),end=", ")
            curr = curr.next
        print((curr.key,curr.value))
        
    def find(self, key):
        curr = self.head
        while curr != None and curr.key != key:
            curr = curr.next
        return curr

    def remove(self, key):
        curr = self.head
        prev = None
        while(curr != None and curr.key != key):
            prev = curr
            curr = curr.next
        if(curr != None):
            if(prev == None):
                self.head = curr.next
            else:
                prev.next = curr.next
                curr.next = None
            return True             # to indicate that key is here
        return False                # to indicate that key isn't here
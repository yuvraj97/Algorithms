# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 16:25:26 2019

@author: Yuvraj
"""

def gcd(a,b):
    if(a==0):
        return b
    if(b==0):
        return a
    if(a<b):
        return gcd(a, b%a)
    else:
        return gcd(a%b, b)


#This modInverse() is taken from:
#https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
# inverse of a under modulo m 
# Assumption: m is prime 
def modInverse(a, m) : 
    g = gcd(a, m) 
    if (g != 1) : 
        return None
    else : 
        # If a and m are relatively prime, 
        # then modulo inverse is a^(m-2) mode m 
        return power(a, m - 2, m)
      
# To compute x^y under modulo m
#This power() is taken from:
#https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
def power(x, y, m) : 
      
    if (y == 0) : 
        return 1
          
    p = power(x, y // 2, m) % m 
    p = (p * p) % m 
  
    if(y % 2 == 0) : 
        return p  
    else :  
        return ((x * p) % m) 

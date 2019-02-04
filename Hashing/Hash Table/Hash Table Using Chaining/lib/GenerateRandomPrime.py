# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:45:36 2019

@author: Yuvraj
"""

from random import randrange, getrandbits

# This isPrime is implemented using Miller-Rabin Algorithm
# Miller-Rabin is more advanced than Fermat’s primality test.
# Carmichael numbers are the problem in Fermat’s primality test
# For Miller-Rabin, we need to find r and s such that (n-1) = r*(2^s), with r odd.
# n: number we wanna check whether is prime or not
# The goal of Miller-Rabin is to find a nontrivial square roots of 1 modulo n.
# For example:
# 3² = 9 = 1 (mod 8)
# so 3 is a non trivial square root of 1 modulo 8
def isPrime(n, k=128):     # n: no. of check whether prime or not, k: no. of test
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:   # This loop is to reduce r by r/2 untill we get an odd r
        s += 1          # For Miller-Rabin, we need to find r and s such that (n-1) = r*(2^s), with r odd
        r =  r//2       # 
    for i in range(k):
        a = randrange(2, n - 1) # get a random no. in b/w 2 and n-1
        x = pow(a, r, n)        # x = (a^r) mod n 
        if x != 1 and x != n - 1:   # if x == 1 or x == n - 1  => maybe prime
            j = 1
            # if we encounter a^((2^j)r) != n - 1 (mod n) for any of j such that 0 ≤ j ≤ s-1
            # if ∃j 0 ≤ j ≤ s-1 , s.t. a^((2^j)r) != n - 1 (mod n) => the n is not prime
            while j < s and x != n - 1:     # Here we check for a^((2^j)r) != n - 1 (mod n) for  0 ≤ j ≤ s-1
                x = pow(x, 2, n)            # x = x^((2^j)r) != n - 1 (mod n)  #  for j = 1, x = (a^r) mod n
                if x == 1:                  # Here we check for a^((2^j)r) == 1 (mod n) , for 0 ≤ j ≤ s-1
                    return False            # if a^((2^j)r) == 1 (mod n) then n is a composite number
                j += 1
            # If we reach this line => the line  "return False" isn't visited
            # so x != 1(mod n) so x must be: x = -1(mod n) => x = n - 1(mod n)
            if x != n - 1:                  # Here we check a^((2^j)r) != n - 1 (mod n) for j==s
                return False                # And if a^((2^j)r) != n - 1 (mod n) for j==s
                                            # => a^((2^s)r) != n - 1 (mod n)
                                            # => a^(n-1) ! = n - 1 (mod n)
    return True
def getRandomOddNumber(l): # It will return a Random Odd Number of length:(l)
    # generate random bits
    p = getrandbits(l)
    #Set First and last bit to 1
    p = p | (1 << l - 1)   # set First bit to 1
    p = p | 1                   # set Last bit to 1
    return p
def generatePrimeNumber(l=64):
    p = getRandomOddNumber(l)
    while not isPrime(p, 128):
        p = getRandomOddNumber(l)
    return p

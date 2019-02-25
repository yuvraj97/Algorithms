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
'''
s="32416187567 32416188223 32416188809 32416189391 32416187627	32416188227	32416188839	32416189459 32416187651	32416188241	32416188859	32416189469 32416187659	32416188257	32416188877	32416189493 32416187701	32416188269	32416188887	32416189499 32416187719	32416188271	32416188899	32416189511 32416187737	32416188331	32416188949	32416189573 32416187747	32416188349	32416189019	32416189633 32416187761	32416188367	32416189031	32416189657 32416187773	32416188397	32416189049	32416189669 32416187827	32416188449	32416189061	32416189681 32416187863	32416188451	32416189063	32416189717 32416187893	32416188491	32416189079	32416189721 32416187899	32416188499	32416189081	32416189733 32416187927	32416188517	32416189163	32416189753 32416187929	32416188527	32416189181	32416189777 32416187933	32416188583	32416189193	32416189853 32416187953	32416188589	32416189231	32416189859 32416187977	32416188601	32416189261	32416189867 32416187987	32416188647	32416189277	32416189877 32416188011	32416188689	32416189291	32416189909 32416188037	32416188691	32416189321	32416189919 32416188113	32416188697	32416189349	32416189987 32416188127	32416188767	32416189361	32416190039 32416188191	32416188793	32416189381	32416190071"# 32416188193	32416188795	32416189383	32416190073 308004653277945 1334686830871095 13654872961988895 13449536526470265 14270882268544785"
s=s.split()
s=[int(i) for i in s]
true,false=0,0
for i in s:
    t=isPrime(i)
    if(t==True):
        true+=1
    else:
        false+=1
print("true:",true)
print("Flase:",false)

print(generatePrimeNumber(100))
'''
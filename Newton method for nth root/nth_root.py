# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:50:54 2019

@author: Yuvraj
"""

# This program Uses Newton's Method to find nth root of a number(base 10)
# Use: nth_root() method
# It takes 3 arguments:
# 1st arg: n: number whose nth root is to be find
# 2nd arg: nthRoot: This specifies which root you want to find (2 for square root, 3 for cube root, 4 for 4th root, etc)
# 3rd arg: precision: It specifies digits of precision you want after decimal

# noOfDigits() will return number of digits in a number: n with base: base
# Ex:
# base = 25
# n = 19*(25**6) + 20*(25**4) + 4*(25**3) + 2*25 + 10
# base 10 representation of n: 4646546935
# n contain 7 digits in base 25
# noOfDigits(n,base)    # it will output: 7
def __noOfDigits__(n,base=10):
    if(base == 1):
        return -1
    temp = n
    count = 0
    while temp > 0:
        temp //= base
        count += 1
    return count

# It will return list containing digits of the number n whose base can be any base
def __base_10_to_base_b__(n,base=10):
    l = []
    while(n>0):
        lastdigit = n % base
        n = n//base
        l.append(lastdigit)
    l.reverse()
    return l

# Here l is the list of digits of a number in base: b 
def __base_b_to_base_10__(l,base):
    result=0
    length = len(l)
    for i in range(length - 1, -1, -1):
        power = length - 1 - i
        result = result + l[i]*(base**power)
    return result
    
def __binary_search__(start,end,digit,nth_root,base):
    mid = (end+start)//2
    guess_sqr = mid**nth_root
    if(guess_sqr == digit): return mid
    elif(start == mid or end == mid):
        err_start = abs(start**nth_root - digit)
        err_end = abs(end**nth_root - digit)
        if(err_start<err_end):  return start
        else:                   return end
    elif(guess_sqr < digit):  return __binary_search__(mid,end,digit,nth_root,base)
    elif(guess_sqr > digit):  return __binary_search__(start,mid,digit,nth_root,base)

def __guess__(n,nth_root,base=10):
    digits = __base_10_to_base_b__(n,base)
    noOfDigits = len(digits) // nth_root - 1
    firstDigit = digits[0]
    firstDigitGuess = __binary_search__(0,firstDigit,firstDigit,nth_root,base)
    if(noOfDigits<0): return firstDigitGuess
    return firstDigitGuess*(base**noOfDigits)
    
def __conertToString__(n,precision):
    a = str(n)
    a1 = a[:len(a)-precision]
    a1 += '.'
    a1 = a1 + a[len(a)-precision:]
    return a1

# It will return a string 
def nth_root(n,nthRoot,precision=20):
    base = 10
    n = n *(base**(nthRoot*precision))
    guess = __guess__(n,nthRoot,base)
    prevGuess = guess
    while(True):
        guess = guess - (guess**nthRoot - n)//(nthRoot*(guess**(nthRoot - 1)))
        if(guess==prevGuess):break
        prevGuess  = guess
    return __conertToString__(guess,precision)

# Example:
# Find square root of 2
# n = 2
# nthRoot = 2       # It specifies we are finding square root
# precision = 20    # 20 digit of precision after decimal
# print(nth_root(n, nthRoot, precision))

# Find cube root of 2
# n = 2
# nthRoot = 3       # It specifies we are finding cube root
# precision = 10    # 10 digit of precision after decimal
# print(nth_root(n, nthRoot, precision))

# Find 4th root of 2
# n = 2
# nthRoot = 4       # It specifies we are finding 4th root
# precision = 1000  # 1000 digit of precision after decimal
# print(nth_root(n, nthRoot, precision))
# .
# .
# .
# .
# .
# Limitation: Currently this program works with base 10 numbers only

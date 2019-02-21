# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:51:56 2019

@author: Yuvraj
"""

import Rubiks_Cube as cube

l =["RC","FCC","UCC","RC","FC","RC","FC","UC","RC","UC"]
final   = cube.shuffleManually(l)
initial = cube.I
s = cube.solveRubiksCube(initial,final)
print("To reach from final configuration to initial configuration perform these steps:")
print(s)

final   = cube.random_shuffle_cube(cube.I,7)
initial = cube.I
s = cube.solveRubiksCube(initial,final)
print("To reach from final configuration to initial configuration perform these steps:")
print(s)

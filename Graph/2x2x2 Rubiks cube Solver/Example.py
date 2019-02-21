# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 18:51:56 2019

@author: Yuvraj
"""

import Rubiks_Cube as cube

# RC stands for Right Clockwise Rotation          == Left Counter Clockwise Rotation
# UC stands for Upper Clockwise Rotation          == Down Counter Clockwise Rotation
# FC stands for Front Clockwise Rotation          == Back Counter Clockwise Rotation
# RCC stands for Right Counter Clockwise Rotation == Left Clockwise Rotation
# UCC stands for Upper Counter Clockwise Rotation == Down Clockwise Rotation
# FCC stands for Front Counter Clockwise Rotation == Back Clockwise Rotation


l =["RC","FCC","UCC","RC","FC","RC","FC","UC","RC","UC"]
final   = cube.shuffleManually(l)
initial = cube.I
s = cube.solveRubiksCube(initial,final)
print("To reach from final configuration to initial configuration perform these steps:")
print(s)

print("# ---------------------------------------\n")

final   = cube.random_shuffle_cube(cube.I,7)
initial = cube.I
s = cube.solveRubiksCube(initial,final)
print("To reach from final configuration to initial configuration perform these steps:")
print(s)

print("# ---------------------------------------\n")

final   = ["UCC", "FC", "UCC", "FCC", "FCC", "RCC", "FCC", "RCC"]
initial = ["RC","FCC","UCC","RC","FC","RC","FC","UC","RC","UC"]
initial = cube.shuffleManually(initial)
final   = cube.shuffleManually(final)
s = cube.solveRubiksCube(initial,final)
print("To reach from final configuration to initial configuration perform these steps:")
print(s)

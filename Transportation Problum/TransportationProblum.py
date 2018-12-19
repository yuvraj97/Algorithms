# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 18:29:09 2018
Updated on Wed Dec 19 15:09:55 2018

@author: Yuvraj
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 18:29:09 2018

@author: Vaio
"""
import numpy as np
import sys

def NorthwestCornerCell(supply,demand,cost):
    rows = cost.shape[0]
    column = cost.shape[1]
    output = np.zeros(cost.shape)
    total_cost = 0
    for i in range(rows):            # ith row is related to ith Supply
        if(supply[i] == 0):
            continue
        for j in range(column):      # jth row is related to jth Demand
            if(demand[j] == 0):
                continue
            if(demand[j] < supply[i]):
                total_cost += demand[j] * cost[i,j]
                supply[i] -= demand[j]
                output[i,j] = demand[j]
                demand[j] = 0
            elif(supply[i] < demand[j]):
                total_cost += supply[i] * cost[i,j]
                demand[j] -= supply[i]
                output[i,j] = supply[i]
                supply[i] = 0
            else:
                total_cost += supply[i] * cost[i,j]
                output[i,j] = supply[i]
                supply[i] = demand[j] = 0
    return output,total_cost

def checkNonZero(array):
    for i in range(len(array)):
        if(array[i] != 0):
            return True
    return False

def LeastCostCell(supply,demand,cost):
    def getMinLocation(matrix):
        min = np.inf
        mini = minj = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
               if(matrix[i,j] < min):
                   min = matrix[i,j]
                   mini, minj = i, j
        return (mini,minj)
    def getMaxLocation(matrix):
        max = -np.inf
        maxi = maxj = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
               if(matrix[i,j] > max):
                   max = matrix[i,j]
                   maxi, maxj = i, j
        return (maxi, maxj)
    Infinity = cost[getMaxLocation(cost)] + 1
    costCopy = cost.copy()
    output = np.zeros(cost.shape)
    total_cost = 0
    while(checkNonZero(supply) and checkNonZero(demand)):
        mini,minj = getMinLocation(costCopy)
        if(supply[mini] == 0):
            costCopy[mini,minj]=Infinity
            continue
        if(demand[minj] == 0):
            costCopy[mini,minj]=Infinity
            continue
        if(demand[minj] < supply[mini]):
            total_cost += demand[minj] * cost[mini,minj]
            supply[mini] -= demand[minj]
            output[mini,minj] = demand[minj]
            demand[minj] = 0
        elif(supply[mini] < demand[minj]):
            total_cost += supply[mini] * cost[mini,minj]
            demand[minj] -= supply[mini]
            output[mini,minj] = supply[mini]
            supply[mini] = 0
        else:
            total_cost += supply[mini] * cost[mini,minj]
            output[mini,minj] = supply[mini]
            supply[mini] = demand[minj] = 0
        costCopy[mini,minj]=Infinity
    return output,total_cost

def VogalsApproximation(supply,demand,cost):
    def updateCostFalse(cost):
        costCopy = []
        for i in range(len(cost)):
            temp = []
            for j in range(len(cost[i])):
                temp.append([cost[i,j],False])
            costCopy.append(temp)
        return np.array(costCopy)
    def get2Min(array):     # I/P array will bew 2D where 2nd dimention is used to check if the element is visited or not
        min1 = np.inf
        min2 = np.inf
        min1j = min2j = 0
        for i in range(len(array)):
            if(array[i][1] == True):
                continue
            if(array[i][0] < min1):
                min1 = array[i][0]
                min1j = i
        for i in range(len(array)):
            if(array[i][1] == True):
                continue
            if(array[i][0] < min2 and i != min1j):
                min2 = array[i][0]
                min2j = i
        return min1j, min2j
    def maxOfRowColDiff(row_diff,col_diff):
        isRowMax = True
        max = -np.inf
        position = None
        for i in range(len(row_diff)):
            if(row_diff[i]  > max):
                max = row_diff[i]
                position = i
                isRowMax = True
        for i in range(len(col_diff)):
            if(col_diff[i]  > max):
                max = col_diff[i]
                position = i
                isRowMax = False
        return position, isRowMax       # isRowMax is used to indicate wather the max is from row_diff or col_diff
    def abs(a):
        if(a>0):
            return a
        else:
            return -a
    def getMin(array):
        min = np.inf
        for i in range(len(array)):
            if(array[i][1] == True):
                continue
            if(array[i][0] < min):
                min = array[i][0]
                position = i
        return position
    
    costCopy = updateCostFalse(cost)
    rows = cost.shape[0]
    column = cost.shape[1]
    output = np.zeros(cost.shape)
    total_cost = 0
    while(checkNonZero(supply) and checkNonZero(demand)):
        row_diff_position = []
        col_diff_position = []
        for i in range(rows):
            minr1 ,minr2 = get2Min(costCopy[i])
            row_diff_position.append([(i,minr1),(i,minr2)])
        for i in range(column):
            minc1, minc2 = get2Min(costCopy[:,i])
            col_diff_position.append([(minc1,i),(minc2,i)])
        row_diff_element = []
        for i in range(len(row_diff_position)):
            row_diff_element.append([costCopy[row_diff_position[i][0]], costCopy[row_diff_position[i][1]]])
        col_diff_element = []
        for i in range(len(col_diff_position)):
            col_diff_element.append([costCopy[col_diff_position[i][0]], costCopy[col_diff_position[i][1]]])
        row_diff_arrray = []    
        for i in range(len(row_diff_position)):
            row_diff_arrray.append(abs(costCopy[row_diff_position[i][0]][0] - costCopy[row_diff_position[i][1]][0]))
        col_diff_arrray = []    
        for i in range(len(col_diff_position)):
            col_diff_arrray.append(abs(costCopy[col_diff_position[i][0]][0] - costCopy[col_diff_position[i][1]][0]))
        max_i, isRow = maxOfRowColDiff(row_diff_arrray,col_diff_arrray)
        if(isRow):
            getLeastFrom = costCopy[max_i]
            leastPosition = getMin(getLeastFrom)
            i,j = max_i, leastPosition
        else:
            getLeastFrom = costCopy[:,max_i]
            leastPosition = getMin(getLeastFrom)
            i,j = leastPosition, max_i
        costCopy[i][j][1] = True        
        if(supply[i] == 0):
            continue
        if(demand[j] == 0):
            continue
        if(demand[j] < supply[i]):
            total_cost += demand[j] * cost[i,j]
            supply[i] -= demand[j]
            output[i,j] = demand[j]
            demand[j] = 0
        elif(supply[i] < demand[j]):
            total_cost += supply[i] * cost[i,j]
            demand[j] -= supply[i]
            output[i,j] = supply[i]
            supply[i] = 0
        else:
            total_cost += supply[i] * cost[i,j]
            output[i,j] = supply[i]
            supply[i] = demand[j] = 0
    return output,total_cost    


def read(filename):
    print("Loading Dataset...")
    f=open(filename,'r');
    s=f.read()
    s=s.split("\n")
    for i in range(len(s)):
        s[i] = s[i].split(",")
    while(s[-1][0] == ''):
        s.pop()
    for i in range(len(s)):
        while(s[i][-1] == ''):
            s[i].pop()
    cost = s[1:len(s)-1]
    for i in range(len(cost)):
        cost[i] = cost[i][1:len(cost[i])-1]
    for i in range(len(cost)):
        for j in range(len(cost[i])):
            cost[i][j] = int(cost[i][j])
    demand = s[-1]
    while(demand[-1] == ''):
        demand.pop()
    demand = demand[1:len(demand)]
    for i in range(len(demand)):
        demand[i] = int(demand[i])
    supply = []
    for i in range(1,len(s)-1):
        supply.append(int(s[i][-1]))
    f.close()
    print("Dataset Loaded.")
    return np.array(supply), np.array(demand), np.array(cost)

def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j],end="\t")
        print()
    
def main():
    if len(sys.argv) != 3:
        print("Usage: ",sys.argv[0],"  argument(NWC/LCC/VAM)    Dataset.csv");
        exit(0)
    supply, demand, cost = read(sys.argv[2])
    if(supply.sum() != demand.sum()):
        print("Currently this program is for balanced Transportation Problum")
        print("This program does not support Unbalanced Transportation Problum")
        exit(0)
    if(sys.argv[1].lower()=="nwc"):
        output,total_cost = NorthwestCornerCell(supply,demand,cost)
        print("Occupied matrix of NorthwestCornerCell:")
        printMatrix(output)
        print("Total cost of NorthwestCornerCell:", total_cost)
    elif(sys.argv[1].lower()=="lcc"):
        output,total_cost = LeastCostCell(supply,demand,cost)
        print("Occupied matrix of LeastCostCell:")
        printMatrix(output)
        print("Total cost of LeastCostCell:", total_cost)
    elif(sys.argv[1]=="vam"):
        output,total_cost = VogalsApproximation(supply,demand,cost)
        print("Occupied matrix of VogalsApproximation:")
        printMatrix(output)
        print("Total cost of VogalsApproximation:", total_cost)
    else:
        print("Invalid Input");
        
if __name__ == "__main__":
    main()

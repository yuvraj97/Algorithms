# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 18:29:09 2018
@author: Yuvraj

"""

import numpy as np
import sys
import time
start = time.time()

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

#This VAM method is too slow an updated method is given below
def VogalsApproximationV1(supply,demand,cost):
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
        position = None
        for i in range(len(array)):
            if(array[i][1] == True):
                continue
            if(array[i][0] < min):
                min = array[i][0]
                position = i
        return position
    
    costCopy = updateCostFalse(cost)
    supplyCopy = supply.copy()
    demandCopy = demand.copy()
    rows = cost.shape[0]
    column = cost.shape[1]
    output = np.zeros(cost.shape)
    total_cost = 0
    while(checkNonZero(supplyCopy) and checkNonZero(demandCopy)):
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
        if(leastPosition == None):
            continue
        costCopy[i][j][1] = True        
        if(supplyCopy[i] == 0):
            continue
        if(demandCopy[j] == 0):
            continue
        if(demandCopy[j] < supplyCopy[i]):
            total_cost += demandCopy[j] * cost[i,j]
            supplyCopy[i] -= demandCopy[j]
            output[i,j] = demandCopy[j]
            demandCopy[j] = 0
        elif(supplyCopy[i] < demandCopy[j]):
            total_cost += supplyCopy[i] * cost[i,j]
            demandCopy[j] -= supplyCopy[i]
            output[i,j] = supplyCopy[i]
            supplyCopy[i] = 0
        else:
            total_cost += supplyCopy[i] * cost[i,j]
            output[i,j] = supplyCopy[i]
            supplyCopy[i] = demandCopy[j] = 0
    return output,total_cost    

def VogalsApproximationV2(supply,demand,cost):
    def get2MinRow(array):     # I/P array will bew 2D where 2nd dimention is used to check if the element is visited or not
        min1 = np.inf
        min2 = np.inf
        min1j = min2j = -1
        for i in range(len(array)):
            if(array[i] <= min1):
                min1 = array[i]
                min1j = i
        for i in range(len(array)):
            if(array[i] <= min2 and i != min1j):
                min2 = array[i]
                min2j = i
        return min1j, min2j
    def get2MinColumn(matrix,col):     # I/P array will bew 2D where 2nd dimention is used to check if the element is visited or not
        min1 = np.inf
        min2 = np.inf
        min1j = min2j = -1
        noRows = matrix.shape[0]
        for i in range(noRows):
            if(matrix[i,col] <= min1):
                min1 = matrix[i,col]
                min1j = i
        for i in range(noRows):
            if(matrix[i,col] <= min2 and i != min1j):
                min2 = matrix[i,col]
                min2j = i
        return min1j, min2j
    def maxOfRowColDiff(row_diff,col_diff):
        isRowMax = True
        max = -np.inf
        position = -1
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
    def getMinRow(array):
        min = np.inf
        position = -1
        for i in range(len(array)):
            if(array[i] < min):
                min = array[i]
                position = i
        return position
    def getMinColumn(matrix,col):
        min = np.inf
        position = -1
        noRows = matrix.shape[0]
        for i in range(noRows):
            if(matrix[i,col] < min):
                min = matrix[i,col]
                position = i
        return position
    
    costCopy = cost.copy()
    supplyCopy = supply.copy()
    demandCopy = demand.copy()
    rows = cost.shape[0]
    column = cost.shape[1]
    output = np.zeros(cost.shape)
    total_cost = 0
    while(checkNonZero(supplyCopy) and checkNonZero(demandCopy)):
        row_diff_position = []
        col_diff_position = []
        for i in range(rows):
            if(supplyCopy[i] != 0):
                minr1 ,minr2 = get2MinRow(costCopy[i])
                row_diff_position.append([(i,minr1),(i,minr2)])
            else:                                           # supplyCopy == 0 mean that whole row[i] is infinity
                row_diff_position.append([(i,0),(i,0)])
        for i in range(column):
            if(demandCopy[i] != 0):
                minc1, minc2 = get2MinColumn(costCopy,i)
                col_diff_position.append([(minc1,i),(minc2,i)])
            else:                                           # demandCopy == 0 mean that whole column[i] is infinity
                col_diff_position.append([(0,i),(0,i)])
        row_diff_arrray = []    
        for i in range(len(row_diff_position)):
            min1, min2 = costCopy[row_diff_position[i][0]], costCopy[row_diff_position[i][1]]
            if(min1 == np.inf and min2 == np.inf):
                row_diff_arrray.append(-np.inf)
            elif(min1 != np.inf and min2 == np.inf):
                row_diff_arrray.append(abs(min1))
            else:
                row_diff_arrray.append(abs(min1 - min2))
        col_diff_arrray = []
        for i in range(len(col_diff_position)):
            min1, min2 = costCopy[col_diff_position[i][0]], costCopy[col_diff_position[i][1]]
            if(min1 == np.inf and min2 == np.inf):
                col_diff_arrray.append(-np.inf)
            elif(min1 != np.inf and min2 == np.inf):
                col_diff_arrray.append(abs(min1))
            else:
                col_diff_arrray.append(abs(min1 - min2))
        max_i, isRow = maxOfRowColDiff(row_diff_arrray,col_diff_arrray)
        if(isRow):
            leastPosition = getMinRow(costCopy[max_i])
            i,j = max_i, leastPosition
        else:
            leastPosition = getMinColumn(costCopy, max_i)
            i,j = leastPosition, max_i
        if(leastPosition == -1):
            continue
        costCopy[i,j] = np.inf
        if(supplyCopy[i] == 0):
            continue
        if(demandCopy[j] == 0):
            continue
        if(demandCopy[j] < supplyCopy[i]):
            total_cost += demandCopy[j] * cost[i,j]
            supplyCopy[i] -= demandCopy[j]
            output[i,j] = demandCopy[j]
            demandCopy[j] = 0
            deleteCol = 1
        elif(supplyCopy[i] < demandCopy[j]):
            total_cost += supplyCopy[i] * cost[i,j]
            demandCopy[j] -= supplyCopy[i]
            output[i,j] = supplyCopy[i]
            supplyCopy[i] = 0
            deleteCol = 0
        else:
            total_cost += supplyCopy[i] * cost[i,j]
            output[i,j] = supplyCopy[i]
            supplyCopy[i] = demandCopy[j] = 0
            deleteCol = 2
        if(deleteCol == 1):          # delete column
            for ittr in range(rows):
                costCopy[ittr, j] = np.inf
        elif(deleteCol == 0):        # delete row
            for ittr in range(column):
                costCopy[i, ittr] = np.inf
        elif(deleteCol == 2):        # delete row and column
            for ittr in range(rows):
                costCopy[ittr, j] = np.inf
            for ittr in range(column):
                costCopy[i, ittr] = np.inf        
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
def checkAnswer(supply, demand, output):
    rows = output.shape[0]
    columns= output.shape[1]
    #Checking Column validity(Demand)
    for j in range(columns):
        jthSum =0
        for i in range(rows):
            jthSum += output[i][j]
        if(jthSum != demand[j]):
            return False
    #Checking Rows Valdity (Supply)
    for i in range(rows):
        ithRow = 0
        for j in range(columns):
            ithRow += output[i][j]
        if(ithRow != supply[i]):
            return False
    return True
            
        
        
def main():
    if len(sys.argv) != 3:
        print("Usage: ",sys.argv[0],"  argument(NWC/LCC/VAM)    Dataset.csv");
        exit(0)
    supply, demand, cost = read(sys.argv[2])
    cost = cost.astype(float)
    total_supply = supply.sum()
    total_demand = demand.sum()
    extra = total_supply - total_demand
    if(total_supply > total_demand):
        row = cost.shape[0]
        temp = np.zeros((row,1))
        cost = np.append(cost,temp,axis=1)
        demand = np.append(demand, extra)
        print("Supply > Demand So a dummy column is added in last")
    elif(total_supply < total_demand):
        col = cost.shape[1]
        temp = np.zeros(col)
        cost = np.vstack([cost,temp])
        supply = np.append(supply, -extra)
        print("Demand > Supply So a dummy row is added in last")
    #printMatrix(cost)
    method = ""
    if(sys.argv[1].lower()=="nwc"):
        output,total_cost = NorthwestCornerCell(supply,demand,cost)
        method = "NorthwestCornerCell"
    elif(sys.argv[1].lower()=="lcc"):
        output,total_cost = LeastCostCell(supply,demand,cost)
        method = "LeastCostCell"
    elif(sys.argv[1]=="vam"):
        output,total_cost = VogalsApproximationV2(supply,demand,cost)
        method = "VogalsApproximation"
    else:
        print("Invalid Input");
        exit(0)
    print("Occupied matrix of ",method,":")
    printMatrix(output)
    print("Total cost of ",method,":", total_cost)
    print("Checking Validity of answer")
    validity = checkAnswer(supply,demand,output)
    if(validity):
        print("Answer is Valid")
    else:
        print("Answer is Invalid")

if __name__ == "__main__":
    main()

end = time.time()
print("Execution Time:",end - start)

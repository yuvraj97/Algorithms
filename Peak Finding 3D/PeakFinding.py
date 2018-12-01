# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:58:23 2018
@author: Vaio
"""
import sys;
from random import randint;

'''
    Layman approch to find a peak
    Time Complexity O(n)
    We will return the position and the value
'''
def linear_peak(array):            
    if(array[0]>array[1]):              # Boundary condition
        return 0, array[0];
    elif(array[-1] > array[-2]):        # Boundary condition
        return len(array)-1, array[-1];
    for i in range(1,len(array)-1):     # range is form 1 till 2nd last element of array (inclusive)
        if(array[i]>array[i-1] and array[i]>array[i+1]):
            return i, array[i];
'''
    This approch is some how like binary search 
    Time Complexity (log(n))
    We will return the position and the value
'''

def rand_array(n):                 # Return arrray with random element of specified size(n)
    array=[];
    for i in range(0,n):
        array.append(randint(0, 1000)); # randint(0,1000) return random number between 0 and 1000
    return array;

def show1D(array):
    for ele in array:
        print(ele,",  ",end="");
    print();

def _find1DPeak_(array,start,end):
    mid=start + int((end-start)/2);
    if(start == end):
        return mid,array[mid];
    elif(array[mid]<array[mid+1]):
        return _find1DPeak_(array,mid+1,end);
    elif(array[mid]<array[mid-1]):
        return _find1DPeak_(array,start,mid-1);
    else:
        return mid,array[mid];

# Checking the Boundary Condition
# if there is no peak at boundary then we send it to the rest of the array
def find1DPeak(array):
    if(array[0]>array[1]):              # Boundary Condition check
        return 0, array[0]; 
    elif(array[-1] > array[-2]):        # Boundary Condition check
        return len(array)-1, array[-1];
    else:                               # Send to rest of the array
        return _find1DPeak_(array,0,len(array)-1);

'''
    Here we find a 2D peak:
    First we took a column find a 1D peak (as shown above) in that column, save that index(say that we save it in variable i)
    Then we traverse in column like a binary search using the 1D peak.
    We look at left and right of that 1D peak and traverse to the side which have a greater value.
    And eventually we will find the 2D peak.
    
    Time Complexity:
        If N represent number of rows and M represent number of column
        Time complexity for 1D peak finding per column is O(log(M))
        And in total we took log(N) number of column to find 1D peak
        So the overall time complexity of our 2D peak finding algorithm is:
        log(N) x log(M)
        if N = M so the time complexity will be
        (log(N))^2
'''

def _find2DPeak_(matrix,start,end,mid):
    array=[row[mid] for row in matrix];
    i=find1DPeak(array)[0];
    if(start == end):
        return (i,mid) , matrix[i][mid];
    if(mid < end):
        if(matrix[i][mid] < matrix[i][mid+1]):
            next_mid=start+int((end-start)/2) +1;
            return _find2DPeak_(matrix,mid+1,end,next_mid);
    if(mid > start):
        if(matrix[i][mid] < matrix[i][mid-1]):
            next_mid=start+int((end-start)/2);
            return _find2DPeak_(matrix,start,mid-1,next_mid);
    return (i,mid) , matrix[i][mid];

# Checking the Boundary Condition
# if there is no peak at boundary then we send it to the rest of the matrix
def find2DPeak(matrix):
    no_col=len(matrix[0]);
    array=[row[0] for row in matrix];
    peak1D_0=find1DPeak(array);        #It's 1D peak of first column
    array=[row[no_col-1] for row in matrix];
    peak1D_n=find1DPeak(array);        #It's 1D peak of last column
    if(matrix[peak1D_0[0]][0] > matrix[peak1D_0[0]][1]):    # Here we check that is the first column peak is the 2D peak
        return (peak1D_0[0],0), matrix[peak1D_0[0]][0];
    elif(matrix[peak1D_n[0]][no_col - 1] > matrix[peak1D_n[0]][no_col - 2]):  # Here we check that is the last column peak is the 2D peak
        return (peak1D_n[0],no_col - 1), matrix[peak1D_n[0]][no_col - 1];
    else:
        return _find2DPeak_(matrix,0,no_col - 1,no_col//2);

# This function returns 2D matrix w/ n rows and m column
def rand_2D(n,m):
    matrix=[];
    for i in range(n):      # no. of column
        temp=[];
        for j in range(m):  # no. of rows
            temp.append(randint(0, 1000));
        matrix.append(temp);
    return matrix;

# This function prints the 2D matrix
def show2D(matrix):
    for rows in matrix:
        for i in rows:
            print(i,"  ",end="");
        print();
'''
    3D Peak Finding:
    Let's assume a 3x3x3 Rubix Cube and at each piece put a number
    And in those numbers a number that is grater with respect to there neighbours is a Peak
    Here we represented cube by taking slices of it plane by plane(each plane).
    
    In this we have l x b x h 3D dataset 
    h: height(depth or plane)
    l: length(no. of rows per plane)
    b: breadth(no. of column)(no. of element per row)
    
    Time Complexity:
        If R represent number of rows and C represent number of column and H represent height(depth)
        Time complexity for 1D peak finding per column is O(log(R) x log(C))
        And in total we took log(H) number of planes to find 3D peak
        So the overall time complexity of our 3D peak finding algorithm is:
        log(R) x log(C) x log(H)
        if R = C = H = N so the time complexity will be
        (log(N))^3


'''
def find3DPeak(cubic):
    height=len(cubic);
    peak_0=find2DPeak(cubic[0]);
    peak_n=find2DPeak(cubic[height - 1]);
    i0,j0=peak_0[0][0],peak_0[0][1];
    i_n,j_n=peak_n[0][0],peak_n[0][1];
    if(cubic[0][i0][j0] > cubic[1][i0][j0]):    # Checking that is plane 0's peak is a 3D peak if yes then return its position and value
        return (0,i0,j0), cubic[0][i0][j0];
    elif(cubic[height-1][i_n][j_n] > cubic[height - 2][i_n][j_n]):
        return (height - 1, i_n, j_n), cubic[height - 1][i_n][j_n];
    else:
        return _find3DPeak_(cubic,0,height-1,height//2);

def _find3DPeak_(cubic,start,end,mid):
    plane=cubic[mid];
    peak=find2DPeak(plane);
    i,j=peak[0][0],peak[0][1];
    if(start == end):
        return (mid,i,j), cubic[mid][i][j];
    if(mid < end):
        if(cubic[mid][i][j] < cubic[mid+1][i][j]):
            next_mid = start + int((end-start)/2) +1;
            return _find3DPeak_(cubic,mid+1,end,next_mid);
    if(mid > start):
        if(cubic[mid][i][j] < cubic[mid-1][i][j]):
            next_mid = start + int((end-start)/2);
            return _find3DPeak_(cubic,start,mid-1,next_mid);
    return (mid,i,j), cubic[mid][i][j];     #Here mid is depth(plane i), i is row number ot that plane and j is the column number of that row

# It return 3D matrix of random numbers
def rand3D(l,b,h):
    cubic=[];
    for i in range(h):
        tempi=[];
        for j in range(l):
            tempj=[];
            for k in range(b):
                tempj.append(randint(0,1000));
            tempi.append(tempj);
        cubic.append(tempi);
    return cubic;

# It writes a 3D dataset into a file(HardDrive) name cube3D_dataset.csv
def write_cube3D(cubic):
    h, l, b = len(cubic), len(cubic[0]), len(cubic[0][0]);
    file_w = "";
    for i in range(h):                  # h defines depth, height (plane h)
        for j in range(l):              # l define number of rows on that plane
            for k in range(b):          # b define number of column (element) on that row
                file_w += str(cubic[i][j][k]) + ",";
            file_w += "\n";
        file_w += "!\n";        # Here '!' is use to seprate two planes
    #print(file_w)
    try:
        file = open(".//cube3D_dataset.csv",'w');
        file.write(file_w);
        file.close();
    except IOError:
        print("Error creating or writing file: cube3D_dataset.csv");
        sys.exit();


def read1D(filename):
    import csv
    try:
        data=[];
        f=open(filename,'r');
        dataList=list(csv.reader(f));
        for i in range(len(dataList[0])):
            data.append(int(dataList[0][i]));
        f.close();
        dataList=None;
        return data;
    except IOError:
        print("Error opening or reading file: ",filename);
        sys.exit();
    
def read2D(filename):
    import csv
    try:
        f=open(filename,'r');
        dataList=list(csv.reader(f));
        for i in range(len(dataList)):
            for j in range(len(dataList[i])):
                dataList[i][j]=int(dataList[i][j]);
        f.close();
        return dataList;
    except IOError:
        print("Error opening or reading file: ",filename);
        sys.exit();
    
def read3D(filename):
    import csv;
    try:
        file=open(filename,'r');
        dataList=list(csv.reader(file));
        file.close();
    except IOError:
        print("Error opening or reading file: ",filename);
        sys.exit();
    cubic=[];
    plane=[];
    array=[];
    for i in range(len(dataList)):
        for j in range(len(dataList[i])):
            if(dataList[i][j]!='!' and dataList[i][j]!=''):
                dataList[i][j]=int(dataList[i][j]);
                array.append(dataList[i][j]);
            if(dataList[i][j]=="!"):
                cubic.append(plane);
                plane=[];
        if(len(array)!=0):
            plane.append(array);
            array=[];
    return cubic;

def show3D(cubic):
    planecount=0;
    print("Visualization of a 3D dataset on a 2D screen");
    for matrix in cubic:
        print("Plane",planecount+1);
        for array in matrix:
            for element in array:
                print(element,"\t",end="");
            print();
        print("################################################")
        planecount+=1;

# It verifies that is our calculated peak is really a peak
def isvalid(cubic,h,r,c):           # h: height,  r: row,   c:column
    max_h, max_r, max_c = len(cubic)-1, len(cubic[0])-1, len(cubic[0][0])-1;
    hupper=hlower=rupper=rlower=cupper=clower=1;
    if(h==0):
        hlower = -1;
    elif(h==max_h)    :
        hupper = -1;
    if(r==0):
        rlower = -1;
    elif(r==max_r)    :
        rupper = -1;
    if(c==0):
        clower = -1;
    elif(c==max_c)    :
        cupper = -1;
    if(cubic[h][r][c] > cubic[h+hupper][r][c] and cubic[h][r][c] > cubic[h-hlower][r][c]):
        if(cubic[h][r][c] > cubic[h][r+rupper][c] and cubic[h][r][c] > cubic[h][r-rlower][c]):
            if(cubic[h][r][c] > cubic[h][r][c+cupper] and cubic[h][r][c] > cubic[h][r][c-clower]):
                return True;
    return False;

def main():
    if len(sys.argv) != 3:
        print("Usage: peakFinding.py   argument(1D/2D/3D)    filename");
    elif(sys.argv[1]=="3D" or sys.argv[1]=="3d"):
        filename = sys.argv[2];
        cubical = read3D(filename);
        show3D(cubical);
        peak = find3DPeak(cubical);
        print("3D peak of the input file is: ",peak[1],);
        print( "And location is depth(plane): ", peak[0][0] +1, " row no:", peak[0][1]+1," and column no:",peak[0][2]+1);
    elif(sys.argv[1]=="2D" or sys.argv[1]=="2d"):
        filename = sys.argv[2];
        matrix = read2D(filename);
        show2D(matrix);
        peak = find2DPeak(matrix);
        print("2D peak of the input file is: ",peak[1],);
        print( "And location is row no:",peak[0][0]+1," and column no:",peak[0][1]+1);
    elif(sys.argv[1]=="1D" or sys.argv[1]=="1d"):
        filename = sys.argv[2];
        array = read1D(filename);
        show1D(array);
        peak = find1DPeak(array);
        print("1D peak of the input file is: ",peak[1],);
        print( "And location is index:",peak[0]);
    else:
        print("Invalid Input");

if __name__ == "__main__":
    import profile;
    profile.run("main()");
    
    
'''    
for ittr in range(100000):
    print(ittr)
    cubic = rand3D(10,10,10);
    write_cube3D(cubic);
    a=find3DPeak(cubic)
    if(not isvalid(cubic,a[0][0],a[0][1],a[0][2])):
        exit(0);
    file = open(".//cube3D_dataset.csv",'a')
    file.write(str(a[0][0]) + " - "+ str(a[0][1]) + " - "+ str(a[0][2]) + " - "+ str(a[1])+"\n");
    file.close();
'''

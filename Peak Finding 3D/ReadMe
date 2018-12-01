PeakFinding.py is a program to find the 1D, 2D and 3D Peak.
It can be access by terminal as:
# python PeakFinding.py <arg 1D/2D/3D> filename.csv
for example:

# python PeakFinding.py  1D  1D_dataset.csv
# python PeakFinding.py  2D  2D_dataset.csv
# python PeakFinding.py  3D  3D_dataset.csv

Here argument 1D is used if input file contain of 1D data
Here argument 2D is used if input file contain of 2D data
Here argument 3D is used if input file contain of 3D data

The file is of csv type.
In 1D simply comma seprated integers
In 2D data file is also simple example file is provided.
In 3D data the matrices are seprated using '!' symbol.
  3D dataset is represennted by multiple matrices.
  That you can think as slices of a cube.
Let's assume a 3x3x3 Rubix Cube and at each piece put a number
And in those numbers a number that is grater with respect to there neighbours is a Peak
Here we represented cube by taking slices of it plane by plane(each plane).

In this we have l x b x h 3D dataset 
h: height(depth or plane)
l: length(no. of rows per plane)
b: breadth(no. of column)(no. of element per row)

Time Complexity:
    If R represent number of rows and C represent number of column and H represent height(depth)
    Time complexity for 2D peak finding per plane is O(log(R) x log(C))
    And in total we took log(H) number of planes to find 3D peak
    So the overall time complexity of our 3D peak finding algorithm is:
    log(R) x log(C) x log(H)
    if R = C = H = N so the time complexity will be
    (log(N))^3

#!/usr/bin/env python

import time
import random
import datavision as datavision

def main():

    print("plot 3 x 3 list")
    matrix1 = [[ 1,  2,  3 ],
               [ 4,  5,  6 ],
               [ 7,  8,  9 ]]
    datavision.plotList(listObject = matrix1)
    
    print("plot 4 x 4 list")
    matrix2 = [[ 1,  2,  3,  4 ],
              [  5,  6,  7,  8 ],
              [  9, 10, 11, 12 ],
              [ 13, 14, 15, 16 ]]
    datavision.plotList(listObject = matrix2)
    
    print("plot 5 x 5 list")
    matrix3 = [[  1,  2,  3,  4,  5 ],
               [  6,  7,  8,  9, 10 ],
               [ 11, 12, 13, 14, 15 ],
               [ 16, 17, 18, 19, 20 ],
               [ 21, 22, 23, 24, 25 ]]
    datavision.plotList(listObject = matrix3)

    print("plot 1 x 3 list")
    matrix4 = [[1],
               [2],
               [3]]
    datavision.plotList(listObject = matrix4)

    print("plot 3-element list as 3 x 1 list")
    matrix5 = [1, 2, 3]
    datavision.plotList(listObject = matrix5)

    input("Press Enter to continue.")

    print("print and plot 10 x 10 matrix")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 50,
        numberOfRows = 50,
        randomise = True
    )
    print(matrix)
    matrix.plot()

    input("Press Enter to continue.")

    matrix.closePlot()
    
    print("plot 2 x 2 matrix and display it changing in a loop")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 2,
        numberOfRows = 2,
        randomise = True
    )
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print("update matrix")
            matrix[row][column] = 10
            matrix.plot()
            time.sleep(1)

    input("Press Enter to continue.")

    matrix.closePlot()

    print("plot 10 x 10 matrix and display it changing in a loop")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 10,
        numberOfRows = 10,
        randomise = True
    )
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print("update matrix")
            matrix[row][column] = random.uniform(-1, 1)
            matrix.plot()
            #time.sleep(0.01)
    
    matrix.closePlot()

    input("Press Enter to terminate.")

if __name__ == '__main__':
    main()

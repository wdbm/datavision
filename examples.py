#!/usr/bin/env python

import time
import datavision as datavision

def main():

    print("plot 3 x 3 list")
    matrix1 = [[ 1,  2,  3 ],
               [ 4,  5,  6 ],
               [ 7,  8,  9 ]]
    datavision.plotList(list = matrix1)
    
    print("plot 4 x 4 list")
    matrix2 = [[ 1,  2,  3,  4 ],
              [  5,  6,  7,  8 ],
              [  9, 10, 11, 12 ],
              [ 13, 14, 15, 16 ]]
    datavision.plotList(list = matrix2)
    
    print("plot 5 x 5 list")
    matrix3 = [[  1,  2,  3,  4,  5 ],
               [  6,  7,  8,  9, 10 ],
               [ 11, 12, 13, 14, 15 ],
               [ 16, 17, 18, 19, 20 ],
               [ 21, 22, 23, 24, 25 ]]
    datavision.plotList(list = matrix3)

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
    
    matrix.closePlot()

    input("Press Enter to terminate.")

if __name__ == '__main__':
    main()

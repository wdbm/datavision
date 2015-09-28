#!/usr/bin/env python

import sys
import time
import random
import datavision as datavision

def pause(
    text = "\nPress Enter to continue."
    ):
    if sys.version_info >= (3, 0):
        input(text)
    else:
        raw_input(text)

def main():

    pause("\nPress Enter to continue.")

    print("\nexample qunti update:")
    a = datavision.Qunti(
        [['alpha', '10'],
         ['beta',  '20'],
         ['gamma', '30'],
         ['gamma', '15']]
    )
    b = datavision.Qunti(
        [['delta', '40'],
         ['alpha', '50']]
    )
    print("a = {qunti}".format(qunti = a))
    print("b = {qunti}".format(qunti = b))
    print("update of a with b:")
    a.update(b)
    print("a = {qunti}".format(qunti = a))

    pause("\nPress Enter to continue.")

    print("\nexample qunti symmetric difference, intersection and update:")
    a = datavision.Qunti(
        [['alpha', '10'],
         ['beta',  '20'],
         ['gamma', '30'],
         ['gamma', '15']]
    )
    b = datavision.Qunti([['delta', '40'], ['alpha', '50'], ['gamma', '25']])
    print("a = {qunti}".format(qunti = a))
    print("b = {qunti}".format(qunti = b))
    print("symmetric difference of a and b:")
    print(a.symmetric_difference(b))
    print("intersection of a and b:")
    print(a.intersection(b))
    print("update of a with b:")
    a.update(b)
    print("a = {qunti}".format(qunti = a))

    pause("\nPress Enter to continue.\n")

    print("plot 3 x 3 list")
    matrix1 = [[ 1,  2,  3 ],
               [ 4,  5,  6 ],
               [ 7,  8,  9 ]]
    datavision.plot_list(listObject = matrix1)
    
    print("plot 4 x 4 list")
    matrix2 = [[ 1,  2,  3,  4 ],
              [  5,  6,  7,  8 ],
              [  9, 10, 11, 12 ],
              [ 13, 14, 15, 16 ]]
    datavision.plot_list(listObject = matrix2)
    
    print("plot 5 x 5 list")
    matrix3 = [[  1,  2,  3,  4,  5 ],
               [  6,  7,  8,  9, 10 ],
               [ 11, 12, 13, 14, 15 ],
               [ 16, 17, 18, 19, 20 ],
               [ 21, 22, 23, 24, 25 ]]
    datavision.plot_list(listObject = matrix3)

    print("plot 1 x 3 list")
    matrix4 = [[1],
               [2],
               [3]]
    datavision.plot_list(listObject = matrix4)

    print("plot 3-element list as 3 x 1 list")
    matrix5 = [1, 2, 3]
    datavision.plot_list(listObject = matrix5)

    pause("Press Enter to continue.")

    print("print and plot 10 x 10 matrix")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 50,
        numberOfRows    = 50,
        randomise       = True
    )
    print(matrix)
    matrix.plot()

    pause("Press Enter to continue.")

    matrix.close_plot()
    
    print("plot 2 x 2 matrix and display it changing in a loop")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 2,
        numberOfRows    = 2,
        randomise       = True
    )
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print("update matrix")
            matrix[row][column] = 10
            matrix.plot()
            time.sleep(1)

    pause("Press Enter to continue.")

    matrix.close_plot()

    print("plot 10 x 10 matrix and display it changing in a loop")
    matrix = datavision.Matrix(
        title = "matrix",
        numberOfColumns = 10,
        numberOfRows    = 10,
        randomise       = True
    )
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print("update matrix")
            matrix[row][column] = random.uniform(-1, 1)
            matrix.plot()
            #time.sleep(0.01)
    
    matrix.close_plot()

    pause("Press Enter to terminate.")

if __name__ == '__main__':
    main()

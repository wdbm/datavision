#!/usr/bin/env python

import datavision as datavision

def main():

    matrix = [[ 1,  2,  3,  4],
              [ 5,  6,  7,  8],
              [ 9, 10, 11, 12],
              [13, 14, 15, 16]]
    datavision.plotList(matrix)

if __name__ == '__main__':
    main()

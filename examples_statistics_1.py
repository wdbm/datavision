#!/usr/bin/env python

import datavision

def main():

    x = [1, 2, 3, 3, 5, 6, 7]
    y = [1, 2, 3, 4, 5, 6, 7]
    
    r, p_value = datavision.correlation_linear(x, y)
    print(datavision.correlation_linear(x, y, printout = True))

if __name__ == "__main__":
    main()

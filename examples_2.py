#!/usr/bin/env python

import sys
import numpy
import datavision

def pause(
    text = "\nPress Enter to continue."
    ):
    if sys.version_info >= (3, 0):
        input(text)
    else:
        raw_input(text)

def main():

    pause("\nPress Enter to continue.")
    print(chr(27) + "[2J")

    plot = datavision.TTYFigure()
    x = numpy.arange(10)
    y = x ** 2 
    tmp = plot.plot(
        x,
        y,
        marker = "_o",
        plot_slope = False
    )
    print plot.plot(
        x,
        30. - y,
        marker = "_s"
    )

    pause("\nPress Enter to terminate.")
    print(chr(27) + "[2J")

    x = numpy.random.normal(0, 1, 1e6)
    datavision.histogram(x, 50)

    pause("\nPress Enter to terminate.")
    print(chr(27) + "[2J")

    x = numpy.random.normal(0, 1, 1e6)
    datavision.histogram(x, 10)

    pause("\nPress Enter to terminate.")
    print(chr(27) + "[2J")

    x = numpy.random.normal(0, 1, 1e6)
    y = numpy.random.normal(0, 1, 1e6)
    datavision.histogram2D(
        x,
        y,
        bins  = [20, 20],
        width = 30
    )

    pause("\nPress Enter to terminate.")
    print(chr(27) + "[2J")

if __name__ == '__main__':
    main()

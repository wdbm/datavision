#!/usr/bin/env python

import numpy
import matplotlib.pyplot
import datavision
import shijian

def main():

    a = numpy.random.normal(2, 2, size = 120)
    b = numpy.random.normal(2, 2, size = 120)
    
    datavision.save_histogram_comparison_matplotlib(
        values_1      = a,
        values_2      = b,
        label_1       = "a",
        label_2       = "b",
        normalize     = True,
        label_ratio_x = "frequency",
        label_y       = "",
        title         = "comparison of a and b",
        filename      = "histogram_comparison_1.png"
    )

if __name__ == "__main__":
    main()

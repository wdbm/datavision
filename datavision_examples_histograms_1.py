#!/usr/bin/env python

import numpy
import datavision

def main():

    print("\ngenerate two arrays of data")

    a = numpy.random.normal(2, 2, size = 120)
    b = numpy.random.normal(2, 2, size = 120)

    print("\narray 1:\n{array_1}\n\narray 2:\n{array_2}".format(
        array_1 = a,
        array_2 = b
    ))

    filename = "histogram_1.png"
    print("\nsave histogram of array 1 to {filename}".format(
        filename = filename
    ))

    datavision.save_histogram_matplotlib(
        a,
        filename   = filename,
        color_fill = "#000000"
        )

    filename = "histogram_comparison_1.png"
    print("\nsave histogram comparison of array 1 and array 2 to {filename}".format(
        filename = filename
    ))

    datavision.save_histogram_comparison_matplotlib(
        values_1      = a,
        values_2      = b,
        label_1       = "a",
        label_2       = "b",
        normalize     = True,
        label_ratio_x = "frequency",
        label_y       = "",
        title         = "comparison of a and b",
        filename      = filename
    )

if __name__ == "__main__":
    main()

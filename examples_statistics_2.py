#!/usr/bin/env python

import numpy
import datavision

def main():

    variable_1 = [1.2, 2.7, 3.2, 3.3, 5.1, 6.2, 7.3]
    variable_2 = [1.1, 2.1, 3.4, 4.9, 5.5, 6.8, 7.6]
    variable_3 = [1.4, 1.3, 1.8, 4.9, 6.5, 6.6, 8.5]

    #variable_1 = numpy.random.normal(2, 2, size = 120)
    #variable_2 = numpy.random.normal(2, 2, size = 120)
    #variable_3 = numpy.random.normal(2, 2, size = 120)

    datavision.save_graph_all_combinations_matplotlib(
        variables        = [ variable_1,   variable_2,   variable_3 ],
        variables_names  = ["variable_1", "variable_2", "variable_3"],
        title            = "variable correlations",
        filename         = "variable_correlations.png"
    )

if __name__ == "__main__":
    main()

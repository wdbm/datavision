#!/usr/bin/env python
from __future__ import division

import numpy

import datavision
import shijian

def main():

    datavision.save_graph_matplotlib(
        values       = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        title        = "graph",
        title_axis_x = "x",
        title_axis_y = "y",
        filename     = "graph.png",
        directory    = ".",
        overwrite    = True,
        color        = "black",
        LaTeX        = False,
        marker_size  = 5
    )

    datavision.save_multigraph_matplotlib(
        variables        = [[1, 2, 3], [3, 1, 3]],
        variables_names  = ["a", "b"],
        title            = "a versus b",
        label_x          = "x",
        label_y          = "y",
        filename         = "multigraph.png",
        directory        = ".",
        overwrite        = True,
        LaTeX            = False,
        marker_size      = 20,
        palette_name     = "palette1"
    )

if __name__ == "__main__":
    main()

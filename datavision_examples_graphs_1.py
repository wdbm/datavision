#!/usr/bin/env python
from __future__ import division

import datetime

import datavision
import numpy
import shijian

def main():

################################################################################
#                                                                              #
# y, or x, y graph                                                             #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# x, y graph                                                                   #
#                                                                              #
################################################################################

    datavision.save_multigraph_matplotlib(
        variables        = [
                               [1.1, 2.4, 3.9, 4.3, 5.1, 6.3, 7.3],
                               [3  , 1  , 3  , 4  , 3  , 5  , 6  ]
                           ],
        variables_names  = ["a", "b"],
        title            = "a versus b",
        title_axis_x     = "x",
        title_axis_y     = "y",
        filename         = "multigraph.png",
        directory        = ".",
        overwrite        = True,
        LaTeX            = False,
        line             = True,
        marker_size      = 10,
        palette_name     = "palette1",
        font_size        = 10
    )

################################################################################
#                                                                              #
# multiple x, y datasets graph                                                 #
#                                                                              #
################################################################################

    dataset_1_name = "dataset 1"
    dataset_1_x    = [0, 1, 2, 3, 4]
    dataset_1_y    = [0, 1, 2, 3, 4]

    dataset_2_name = "dataset 2"
    dataset_2_x    = [0, 1, 2, 3, 4]
    dataset_2_y    = [2, 2, 2, 2, 2]

    dataset_3_name = "dataset 3"
    dataset_3_x    = [3, 3, 3, 3, 3]
    dataset_3_y    = [0, 1, 2, 3, 4]

    datavision.save_multigraph_2D_matplotlib(
        variables_x      = [dataset_1_x, dataset_2_x, dataset_3_x],
        variables_y      = [dataset_1_y, dataset_2_y, dataset_3_y],
        variables_names  = [dataset_1_name, dataset_2_name, dataset_3_name],
        title            = "2D multigraph",
        title_axis_x     = "x",
        title_axis_y     = "y",
        filename         = "multigraph_2D.png",
        directory        = ".",
        overwrite        = True,
        LaTeX            = False,
        markers          = True,
        marker_size      = 0.8,
        line             = True,
        line_width       = 0.5,
        palette_name     = "palette1",
        font_size        = 10
    )

################################################################################
#                                                                              #
# date graph                                                                   #
#                                                                              #
################################################################################

    x = [
            datetime.datetime.strptime("2017-03-12", "%Y-%m-%d"),
            datetime.datetime.strptime("2017-03-13", "%Y-%m-%d"),
            datetime.datetime.strptime("2017-03-14", "%Y-%m-%d"),
        ]
    y = [
            12,
            13,
            14
        ]

    datavision.save_multigraph_2D_matplotlib(
        variables_x      = [x],
        variables_y      = [y],
        variables_names  = ["time"],
        title            = "2D multigraph date",
        title_axis_x     = "time",
        title_axis_y     = "y",
        filename         = "multigraph_2D_date.png",
        directory        = ".",
        overwrite        = True,
        LaTeX            = False,
        markers          = True,
        marker_size      = 0.8,
        line             = True,
        line_width       = 0.5,
        palette_name     = "palette1",
        time_axis_x      = True,
        font_size        = 10
    )

################################################################################
#                                                                              #
# time graph                                                                   #
#                                                                              #
################################################################################

    x = [
            datetime.datetime.strptime("2017-03-13T0900Z", "%Y-%m-%dT%H%MZ"),
            datetime.datetime.strptime("2017-03-13T1200Z", "%Y-%m-%dT%H%MZ"),
            datetime.datetime.strptime("2017-03-13T1700Z", "%Y-%m-%dT%H%MZ"),
        ]
    y = [
            1,
            2,
            3
        ]

    datavision.save_multigraph_2D_matplotlib(
        variables_x      = [x],
        variables_y      = [y],
        variables_names  = ["time"],
        title            = "2D multigraph time",
        title_axis_x     = "time",
        title_axis_y     = "y",
        filename         = "multigraph_2D_time.png",
        directory        = ".",
        overwrite        = True,
        LaTeX            = False,
        markers          = True,
        marker_size      = 0.8,
        line             = True,
        line_width       = 0.5,
        palette_name     = "palette1",
        time_axis_x      = True,
        time_style       = "%H:%M", #"%Y-%m-%dT%H%MZ",
        font_size        = 10
    )

if __name__ == "__main__":
    main()

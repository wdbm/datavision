#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# datavision_TTY_plot                                                          #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program displays a TTY plot of piped values.                            #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help          display help message
    --version           display version and exit
"""

import docopt
import sys

import datavision

name    = "datavision_TTY_plot"
version = "2017-04-28T1439Z"
logo    = None

def main(options):

    if not sys.stdin.isatty():
        input_stream_list = [line for line in sys.stdin]
        y = [float(element.strip()) for element in input_stream_list[0].split(",")]
        x = range(0, len(y))
        plot = datavision.TTYFigure()
        tmp = plot.plot(x, y, marker = "_o")
        print(tmp)

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

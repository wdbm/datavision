#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# data_example_1                                                               #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an example of data usage.                                    #
#                                                                              #
# copyright (C) 2015 Will Breaden Madden, w.bm@cern.ch                         #
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
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
"""

name    = "data_example_1"
version = "2015-12-11T1731Z"
logo    = None

import docopt
import pyprel
import datavision
from random import randint

def main(options):

    dataset = datavision.Dataset()

    for index in range(0, 10):
        dataset.variable(
            index = index,
            name  = "blue",
            value = randint(0, 9)
        )
        dataset.variable(
            index = index,
            name  = "red",
            value = randint(0, 9)
        )

    print("\nThe indices available in the dataset are as follows:\n\n{indices}".format(
        indices = dataset.indices()
    ))

    print("\nThe variables in the dataset are as follows:\n\n{indices}".format(
        indices = dataset.variables()
    ))

    print("\nA table of the dataset is as follows:\n")

    print(dataset.table())

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

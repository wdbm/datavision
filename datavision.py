################################################################################
#                                                                              #
# datavision                                                                   #
#                                                                              #
################################################################################
#                                                                              #
# version: 2014-11-14T1254Z                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides data visualisation utilities in Python.                #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
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

import matplotlib.pyplot as plt
import numpy as np

def plotList(
    list,
    style = "heatmap"
    ):
    # convert list to NumPy array
    array = np.array(list)
    dimensionality = len(array.shape)
    if dimensionality == 2:
        if style == "heatmap":
            # create axis labels
            labelsColumn = []
            labelsRow = []
            for rowNumber in xrange(0, len(list)):
                labelsRow.append(rowNumber + 1)
                for element in list[rowNumber]:
                    labelsColumn.append(element)
            fig, ax = plt.subplots()
            heatmap = ax.pcolor(array, cmap = plt.cm.Blues)
            # major ticks at middle of each cell
            ax.set_xticks(np.arange(array.shape[0]) + 0.5, minor = False)
            ax.set_yticks(np.arange(array.shape[1]) + 0.5, minor = False)
            # table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.set_xticklabels(labelsRow, minor = False)
            ax.set_yticklabels(labelsColumn, minor = False)
            plt.show()
        else:
            Exception
    else:
        Exception

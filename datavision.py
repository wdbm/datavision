################################################################################
#                                                                              #
# datavision                                                                   #
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

version = "2014-11-17T0015Z"

import random
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import shijian as shijian

class Matrix(list):
    
    def __init__(
        self,
        *args,
        title                    = None,
        numberOfColumns          = 3,
        numberOfRows             = 3,
        element                  = 0.0,
        randomise                = False,
        randomiseLimitLower      = -0.2,
        randomiseLimitUpper      = 0.2
        ):
        # list initialisation
        super().__init__(self, *args)   
        self.title               = title
        self.numberOfColumns     = numberOfColumns
        self.numberOfRows        = numberOfRows
        self.element             = element
        self.randomise           = randomise
        self.randomiseLimitLower = randomiseLimitLower
        self.randomiseLimitUpper = randomiseLimitUpper
        # fill with default element
        for column in range(self.numberOfColumns):
            self.append([element] * self.numberOfRows)
        # fill with pseudorandom elements
        if self.randomise:
            random.seed()
            for row in range(self.numberOfRows):
                for column in range(self.numberOfColumns):
                    self[row][column] = random.uniform(
                        self.randomiseLimitUpper,
                        self.randomiseLimitLower
                    )
        # plot
        self._array = np.array(self)
        self._plotNumber         = shijian.uniqueNumber()
        self._plotFigure, \
        self._plotAxes           = plotList(
                                       list       = self,
                                       title      = self.title,
                                       plotNumber = self._plotNumber,
                                       mode       = "return"
                                   )
        # show or draw plot
        self._plotShown          = False

    def plot(self):
        # display or redraw plot
        if self._plotShown:
            plt.figure(str(self._plotNumber))
            self._array = np.array(self)
            self._plotAxes.pcolor(
                self._array,
                cmap = plt.cm.Blues
            )
            plt.draw()
        else:
            plt.figure(str(self._plotNumber))
            plt.show()
            self._plotShown = True

    #def savePlot(self):
    #    plt.figure(str(self._plotNumber))
    #    # upcoming -- plt.savefig(filename)

    def closePlot(self):
        plt.figure(str(self._plotNumber))
        plt.close()
        self._plotShown = False

def plotList(
    list       = list,
    title      = None,
    plotNumber = None,
    style      = "colormap",
    mode       = "plot" # plot/return/save
    ):
    if not plotNumber:
        plotNumber = shijian.uniqueNumber()
    # convert list to NumPy array
    array = np.array(list)
    dimensionality = len(array.shape)
    if dimensionality == 2:
        if style == "colormap":
            # create axis labels
            labelsColumn = []
            labelsRow = []
            for rowNumber in range(0, len(list)):
                labelsRow.append(rowNumber + 1)
                for columnNumber in range(0, len(list[rowNumber])):
                    labelsColumn.append(columnNumber)
            figure = plt.figure(str(plotNumber))
            axes = figure.add_subplot(111)
            colormap = axes.pcolor(array, cmap = plt.cm.Blues)
            # major ticks at middle of each cell
            axes.set_xticks(np.arange(array.shape[0]) + 0.5, minor = False)
            axes.set_yticks(np.arange(array.shape[1]) + 0.5, minor = False)
            # table-like display
            axes.invert_yaxis()
            axes.xaxis.tick_top()
            axes.set_xticklabels(labelsRow, minor = False)
            axes.set_yticklabels(labelsColumn, minor = False)
            # LaTeX text
            plt.rc('text', usetex = True)
            plt.rc('font', family = 'serif')
            # title
            if title:
                plt.title(title, y = 1.05)
            # plot/return/save
            if mode == "plot":
                plt.show()
            elif mode == "return":
                return(figure, axes)
            elif mode == "save":
                raise Exception # upcoming -- plt.savefig(filename)
            else:
                raise Exception
        else:
            raise Exception
    else:
        raise Exception

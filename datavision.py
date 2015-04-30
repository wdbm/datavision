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

version = "2015-04-30T0232Z"

import sys
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
            self._plotFigure, \
            self._plotAxes       = plot_list(
                                       listObject = self,
                                       title      = self.title,
                                       plotNumber = self._plotNumber,
                                       plot       = False,
                                       returnPlot = True
                                )
            plt.figure(str(self._plotNumber))
            plt.show()
            self._plotShown = True

    def save_plot(
        self,
        fileName  = None,
        overwrite = False
        ):
        plt.figure(str(self._plotNumber))
        fileNameProposed = shijian.proposeFileName(
            fileName  = fileName,
            overwrite = overwrite
        )
        plt.savefig(fileNameProposed)

    def close_plot(self):
        plt.figure(str(self._plotNumber))
        plt.close()
        self._plotShown = False

def plot_list(
    listObject = None,
    title      = None,
    plotNumber = None,
    style      = "colormap",
    fileName   = None,
    overwrite  = False,
    plot       = True,
    returnPlot = False,
    save       = False
    ):
    if not plotNumber:
        plotNumber = shijian.uniqueNumber()
    if style == "colormap":
        # convert list to NumPy array
        array = np.array(listObject)
        dimensionality = len(array.shape)
        if dimensionality == 1:
            array = np.array([listObject])
        # create axis labels
        labelsColumn = list(range(0, array.shape[1]))
        labelsRow = list(range(0, array.shape[0]))
        # create figure and axes
        figure = plt.figure(str(plotNumber))
        axes = figure.add_subplot(111)
        colormap = axes.pcolor(array, cmap = plt.cm.Blues)
        # major ticks at middle of each cell
        axes.set_xticks(np.arange(array.shape[1]) + 0.5, minor = False)
        axes.set_yticks(np.arange(array.shape[0]) + 0.5, minor = False)
        # table-like display
        axes.invert_yaxis()
        axes.xaxis.tick_top()
        axes.set_xticklabels(labelsColumn, minor = False)
        axes.set_yticklabels(labelsRow, minor = False)
        # LaTeX text
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'serif')
        # title
        if title:
            plt.title(title, y = 1.05)
        # plot/return/save
        if plot:
            plt.show()
        if returnPlot:
            return(figure, axes)
        if save:
            fileNameProposed = shijian.proposeFileName(
                fileName  = fileName,
                overwrite = overwrite
            )
            plt.savefig(fileNameProposed)

def list_quotient(
    list_dividend = None,
    list_divisor  = None
    ):
    [dividend / divisor for dividend, divisor in zip(
        list_dividend,
        list_divisor
    )]

def list_mean(
    lists = None
    ):
    return([sum(element)/len(element) for element in zip(*lists)])


class Qunti(list):

    def __init__(
        self,
        *args
        ):
        # list initialisation
        if sys.version_info >= (3, 0):
            super().__init__(*args)
        else:
            super(qunti, self).__init__(*args)
    
    def symmetric_difference(
        self,
        updateZus
        ):
        symmetricDifferenceSet = \
            set(zu[0] for zu in self) ^ set(zu[0] for zu in updateZus)
        return(
            [zu for zu in self if zu[0] in symmetricDifferenceSet] +
            [zu for zu in updateZus if zu[0] in symmetricDifferenceSet]
        )

    def intersection(
        self,
        updateZus
        ):
        intersectionSet = \
            set(zu[0] for zu in self) & set(zu[0] for zu in updateZus)
        return(
            [zu for zu in self if zu[0] in intersectionSet] +
            [zu for zu in updateZus if zu[0] in intersectionSet]
        )

    def update(
        self,
        updateZus
        ):
        selfUpdated = []
        # Get the symmetric difference zus of the current zus and the update
        # zus. Include the symmetric difference zus in the updated self zus.
        symmetricDifference = self.symmetric_difference(updateZus)
        symmetricDifferenceSet = set(zu[0] for zu in symmetricDifference)
        selfUpdated.extend(symmetricDifference)
        # Include all entries of the update zus not in the symmetric difference
        # zus in the updated self zus.        
        selfUpdated.extend(
            [zu for zu in updateZus \
            if zu[0] not in symmetricDifferenceSet]
        )
        # Update the self zus.
        self.__init__(selfUpdated)

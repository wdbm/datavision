# -*- coding: utf-8 -*-
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
# copyright (C) 2014 2015 William Breaden Madden                               #
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

version = "2015-09-28T1325Z"

import sys
import math
import random
import matplotlib.pyplot
matplotlib.pyplot.ion()
import numpy
import shijian

class Matrix(list):
    
    def __init__(
        self,
        title                    = None,
        numberOfColumns          = 3,
        numberOfRows             = 3,
        element                  = 0.0,
        randomise                = False,
        randomiseLimitLower      = -0.2,
        randomiseLimitUpper      = 0.2,
        *args
        ):
        # list initialisation
        if sys.version_info >= (3, 0):
            super().__init__(self, *args)
        else:
            super(Matrix, self).__init__(*args)        
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
        self._array = numpy.array(self)
        self._plotNumber         = shijian.uniqueNumber()
        # show or draw plot
        self._plotShown          = False

    def plot(self):
        # display or redraw plot
        if self._plotShown:
            matplotlib.pyplot.figure(str(self._plotNumber))
            self._array = numpy.array(self)
            self._plotAxes.pcolor(
                self._array,
                cmap = matplotlib.pyplot.cm.Blues
            )
            matplotlib.pyplot.draw()
        else:
            self._plotFigure, \
            self._plotAxes       = plot_list(
                                       listObject = self,
                                       title      = self.title,
                                       plotNumber = self._plotNumber,
                                       plot       = False,
                                       returnPlot = True
                                )
            matplotlib.pyplot.figure(str(self._plotNumber))
            matplotlib.pyplot.show()
            self._plotShown = True

    def save_plot(
        self,
        fileName  = None,
        overwrite = False
        ):
        matplotlib.pyplot.figure(str(self._plotNumber))
        fileNameProposed = shijian.proposeFileName(
            fileName  = fileName,
            overwrite = overwrite
        )
        matplotlib.pyplot.savefig(fileNameProposed)

    def close_plot(self):
        matplotlib.pyplot.figure(str(self._plotNumber))
        matplotlib.pyplot.close()
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
        array = numpy.array(listObject)
        dimensionality = len(array.shape)
        if dimensionality == 1:
            array = numpy.array([listObject])
        # create axis labels
        labelsColumn = list(range(0, array.shape[1]))
        labelsRow = list(range(0, array.shape[0]))
        # create figure and axes
        figure = matplotlib.pyplot.figure(str(plotNumber))
        axes = figure.add_subplot(111)
        colormap = axes.pcolor(array, cmap = matplotlib.pyplot.cm.Blues)
        # major ticks at middle of each cell
        axes.set_xticks(numpy.arange(array.shape[1]) + 0.5, minor = False)
        axes.set_yticks(numpy.arange(array.shape[0]) + 0.5, minor = False)
        # table-like display
        axes.invert_yaxis()
        axes.xaxis.tick_top()
        axes.set_xticklabels(labelsColumn, minor = False)
        axes.set_yticklabels(labelsRow, minor = False)
        # LaTeX text
        matplotlib.pyplot.rc('text', usetex = True)
        matplotlib.pyplot.rc('font', family = 'serif')
        # title
        if title:
            matplotlib.pyplot.title(title, y = 1.05)
        # plot/return/save
        if plot:
            matplotlib.pyplot.show()
        if returnPlot:
            return(figure, axes)
        if save:
            fileNameProposed = shijian.proposeFileName(
                fileName  = fileName,
                overwrite = overwrite
            )
            matplotlib.pyplot.savefig(fileNameProposed)

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
            super(Qunti, self).__init__(*args)
    
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

class TTYFigureData(object):
    """
    data container of TTYFigure
    """
    def __init__(
        self,
        x,                      # x values
        y,                      # y values
        marker          = "_.", # datum marker
        plot_slope      = True
        ):
        self.x          = x
        self.y          = y
        self.plot_slope = plot_slope
        self.markers    = {
            "-" : u"None" ,  # solid line style
            "," : u"\u2219", # point marker
            "." : u"\u2218", # pixel marker
            ".f": u"\u2218", # pixel marker
            "o" : u"\u25CB", # circle marker
            "of": u"\u25CF", # circle marker
            "v" : u"\u25BD", # triangle_down marker
            "vf": u"\u25BC", # filler triangle_down marker
            "^" : u"\u25B3", # triangle_up marker
            "^f": u"\u25B2", # filled triangle_up marker
            "<" : u"\u25C1", # triangle_left marker
            "<f": u"\u25C0", # filled triangle_left marker
            ">" : u"\u25B7", # triangle_right marker
            ">f": u"\u25B6", # filled triangle_right marker
            "s" : u"\u25FD", # square marker
            "sf": u"\u25FC", # square marker
            "*" : u"\u2606", # star marker
            "*f": u"\u2605", # star marker
            "+" : u"\u271A", # plus marker
            "x" : u"\u274C", # x marker
            "d" : u"\u25C7", # diamond marker
            "df": u"\u25C6"  # filled diamond marker
        }
        self.set_marker(marker)

    def set_marker(
        self,
        marker
        ):
        if marker in [None, "None", u"None", ""]:
            self.plot_slope = True
            self.marker = ""
        elif marker[0] == "_":
            self.marker = self.markers[marker[1:]]
        else:
            self.marker = marker

    def extent(self):
        """
        return range of 2D data
        """
        return [min(self.x), max(self.x), min(self.y), max(self.y)]

    def __repr__(self):
        return "TTYFigureData: {representation}\n".format(
            representation = str(object.__repr__(self))
        )

class TTYFigure(object):

    def __init__(
        self,
        shape       = (80, 20),
        margins     = (0.05, 0.1),
        draw_axes   = True,
        newline     = "\n",
        plot_labels = True,
        limit_x     = None,
        limit_y     = None,
        **kwargs
        ):
        self.canvas = TTYCanvas(
            shape,
            margins = margins,
            limit_x = limit_x,
            limit_y = limit_y
        )
        self.draw_axes     = draw_axes
        self.new_line      = newline
        self.plot_labels   = plot_labels
        self.outBuffer     = None
        self.tickSymbols   = u"\u253C"  # "+"
        self.x_axis_symbol = u"\u2500"  # u"\u23bc" # "-"
        self.y_axis_symbol = u"\u2502"  # "|"
        self.data          = []

    def limit_x(
        self,
        limit_lower = None,
        limit_upper = None
        ):
        return self.canvas.limit_x(limit_lower, limit_upper)

    def limit_y(
        self,
        limit_lower = None,
        limit_upper = None
        ):
        return self.canvas.limit_y(limit_lower, limit_upper)

    def get_coordinates(
        self,
        value,
        minimum,
        step,
        limits = None
        ):
        result = int((value - minimum) / step)
        if limits is not None:
            if result <= limits[0]:
                result = limits[0]
            elif result >= limits[1]:
                result = limits[1] - 1
        return result

    def _draw_axes(self):
        zero_x = self.get_coordinates(
            0,
            self.canvas.min_x,
            self.canvas.step_x,
            limits = [1, self.canvas.x_size]
        )
        if zero_x >= self.canvas.x_size:
            zero_x = self.canvas.x_size - 1
        for y in xrange(self.canvas.y_size):
            self.outBuffer[zero_x][y] = self.y_axis_symbol

        zero_y = self.get_coordinates(
            0,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size])
        if zero_y >= self.canvas.y_size:
            zero_y = self.canvas.y_size - 1
        for x in xrange(self.canvas.x_size):
            self.outBuffer[x][zero_y] = self.x_axis_symbol # u"\u23bc"

        self.outBuffer[zero_x][zero_y] = self.tickSymbols # "+"

    def _get_symbol_by_slope(
        self,
        slope,
        default_symbol
        ):
        """
        return line oriented approximatively along the slope value
        """
        if slope > math.tan(3 * math.pi / 8):
            draw_symbol = "|"
        elif math.tan(math.pi / 8) < slope < math.tan(3 * math.pi / 8):
            draw_symbol = u"\u27cb" # "/"
        elif abs(slope) < math.tan(math.pi / 8):
            draw_symbol = "-"
        elif slope < math.tan(-math.pi / 8) and\
            slope > math.tan(-3 * math.pi / 8):
            draw_symbol = u"\u27CD" # "\\"
        elif slope < math.tan(-3 * math.pi / 8):
            draw_symbol = "|"
        else:
            draw_symbol = default_symbol
        return draw_symbol

    def _plot_labels(self):

        if self.canvas.y_size < 2:
            return

        act_min_x, act_max_x, act_min_y, act_max_y = self.canvas.extent()

        min_x_coordinates = self.get_coordinates(
            act_min_x,
            self.canvas.min_x,
            self.canvas.step_x,
            limits = [0, self.canvas.x_size]
        )
        max_x_coordinates = self.get_coordinates(
            act_max_x,
            self.canvas.min_x,
            self.canvas.step_x,
            limits = [0, self.canvas.x_size]
        )
        min_y_coordinates = self.get_coordinates(
            act_min_y,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size]
        )
        max_y_coordinates = self.get_coordinates(
            act_max_y,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size]
        )

        x_zero_coordinates = self.get_coordinates(
            0,
            self.canvas.min_x,
            self.canvas.step_x,
            limits = [0, self.canvas.x_size]
        )
        y_zero_coordinates = self.get_coordinates(
            0,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size]
        )

        self.outBuffer[x_zero_coordinates][min_y_coordinates] = self.tickSymbols
        self.outBuffer[x_zero_coordinates][max_y_coordinates] = self.tickSymbols
        self.outBuffer[min_x_coordinates][y_zero_coordinates] = self.tickSymbols
        self.outBuffer[max_x_coordinates][y_zero_coordinates] = self.tickSymbols

        min_x_string, max_x_string, min_y_string, max_y_string =\
            self.canvas.extent_string()
        if self.canvas.x_string() is not None:
            for i, c in enumerate(min_x_string):
                self.outBuffer[
                    min_x_coordinates + i + 1
                ][
                    y_zero_coordinates - 1
                ] = c
            for i, c in enumerate(max_x_string):
                self.outBuffer[
                    max_x_coordinates + i - len(max_x_string)
                ][
                    y_zero_coordinates - 1
                ] = c

        if self.canvas.y_string() is not None:
            for i, c in enumerate(max_y_string):
                self.outBuffer[
                    x_zero_coordinates + i + 1
                ][
                    max_y_coordinates
                ] = c
            for i, c in enumerate(min_y_string):
                self.outBuffer[
                    x_zero_coordinates + i + 1
                ][
                    min_y_coordinates
                ] = c

    def _plot_line(
        self,
        start,
        end,
        data
        ):
        """
        plot line from start = (x0, y0) to end = (x1, y1)
        """

        clipped_line = self.canvas._clip_line(start, end)

        if clipped_line is None:
            return False

        start, end = clipped_line

        x0 = self.get_coordinates(
            start[0],
            self.canvas.min_x,
            self.canvas.step_x
        )
        y0 = self.get_coordinates(
            start[1],
            self.canvas.min_y,
            self.canvas.step_y
        )
        x1 = self.get_coordinates(
            end[0],
            self.canvas.min_x,
            self.canvas.step_x
        )
        y1 = self.get_coordinates(
            end[1],
            self.canvas.min_y,
            self.canvas.step_y
        )

        if (x0, y0) == (x1, y1):
            return True

        #x_zero_coordinates = self.get_coordinates(
        #    0,
        #    self.canvas.min_x,
        #    self.canvas.step_x
        #)
        y_zero_coordinates = self.get_coordinates(
            0,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size]
        )

        if start[0] - end[0] == 0:
            draw_symbol = u"|"
        elif start[1] - end[1] == 0:
            draw_symbol = "-"
        else:
            slope =\
                (1.0 / self.canvas.ratio) * (end[1] - start[1])\
                / (end[0] - start[0])
            draw_symbol = self._get_symbol_by_slope(slope, data.marker)

        dx = x1 - x0
        dy = y1 - y0
        if abs(dx) > abs(dy):
            s = sign(dx)
            slope = float(dy) / dx
            for i in range(0, abs(int(dx))):
                current_draw_symbol = draw_symbol
                x = i * s
                current_y = int(y0 + slope * x)
                if\
                    (self.draw_axes) and\
                    (current_y == y_zero_coordinates) and\
                    (draw_symbol == self.x_axis_symbol):
                    current_draw_symbol = "-"
                self.outBuffer[x0 + x][current_y] = current_draw_symbol
        else:
            s = sign(dy)
            slope = float(dx) / dy
            for i in range(0, abs(int(dy))):
                y = i * s
                current_draw_symbol = draw_symbol
                current_y = y0 + y
                if\
                    (self.draw_axes) and\
                    (current_y == y_zero_coordinates) and\
                    (draw_symbol == self.x_axis_symbol):
                    current_draw_symbol = "-"
                self.outBuffer[
                    int(x0 + slope * y)
                ][
                    current_y
                ] = current_draw_symbol

        return False

    def _plot_data_with_slope(
        self,
        data
        ):
        xy = list(zip(data.x, data.y))

        # Sort by the x coördinate.
        xy.sort(key = lambda c: c[0])
        previous_p = xy[0]
        e_xy = enumerate(xy)
        e_xy.next()
        for i, (xi, yi) in e_xy:
            line = self._plot_line(previous_p, (xi, yi), data)
            previous_p = (xi, yi)

            # If a line is not used, use markers.
            if not line & self.canvas.coordinates_inside_data(xi, yi):
                draw_symbol = data.marker

                px, py = xy[i - 1]
                nx, ny = xy[i]

                if abs(nx - px) > 0.000001:
                    slope = (1.0 / self.canvas.ratio) * (ny - py) / (nx - px)
                    draw_symbol = self._get_symbol_by_slope(
                        slope,
                        draw_symbol
                    )

                x_coordinates = self.get_coordinates(
                    xi,
                    self.canvas.min_x,
                    self.canvas.step_x
                )
                y_coordinates = self.get_coordinates(
                    yi,
                    self.canvas.min_y,
                    self.canvas.step_y
                )

                if self.canvas.coordinates_inside_buffer(
                    x_coordinates,
                    y_coordinates
                    ):
                    y0_coordinates = self.get_coordinates(
                        0,
                        self.canvas.min_y,
                        self.canvas.step_y
                    )
                    if self.draw_axes:
                        if\
                            (y_coordinates == y0_coordinates) and\
                            (draw_symbol == u"\u23bc"):
                            draw_symbol = "="
                    self.outBuffer[x_coordinates][y_coordinates] = draw_symbol

    def _plot_data(
        self,
        data
        ):
        if data.plot_slope:
            self._plot_data_with_slope(data)
        else:
            for x, y in zip(data.x, data.y):
                if self.canvas.coordinates_inside_data(x, y):
                    x_coordinates = self.get_coordinates(
                        x,
                        self.canvas.min_x,
                        self.canvas.step_x
                    )
                    y_coordinates = self.get_coordinates(
                        y,
                        self.canvas.min_y,
                        self.canvas.step_y
                    )

                    if self.canvas.coordinates_inside_buffer(
                        x_coordinates,
                        y_coordinates
                        ):
                        self.outBuffer[
                            x_coordinates
                        ][
                            y_coordinates
                        ] = data.marker

    def auto_limits(self):
        if self.canvas.auto_adjust is True:
            min_x = 0.
            max_x = 0.
            min_y = 0.
            max_y = 0.
            for dk in self.data:
                ek = dk.extent()
                min_x = min(min_x, min(ek[:2]))
                min_y = min(min_y, min(ek[2:]))
                max_x = max(max_x, max(ek[:2]))
                max_y = max(max_y, max(ek[2:]))
            self.canvas.limit_x(min_x, max_x)
            self.canvas.limit_y(min_y, max_y)

    def append_data(
        self,
        data
        ):
        self.data.append(data)
        self.auto_limits()

    def plot(
        self,
        x_values   = None,
        y_values   = None,
        marker     = None,
        plot_slope = False,
        limit_x    = None,
        limit_y    = None
        ):

        if y_values is None:
            y_values = x_values[:]
            x_values = range(len(y_values))

        figureData = TTYFigureData(
            x_values,
            y_values,
            marker = marker,
            plot_slope = plot_slope
        )
        self.append_data(figureData)

        if limit_x is not None:
            self.canvas.limit_x(limit_x)

        if limit_y is not None:
            self.canvas.limit_y(limit_x)

        return self.draw()

    def draw(self):
        self.outBuffer =\
            [[" "] * self.canvas.y_size for i in range(self.canvas.x_size)]
        if self.draw_axes:
            self._draw_axes()

        for dk in self.data:
            self._plot_data(dk)

        if self.plot_labels:
            self._plot_labels()
        result_transposed = transpose(reverse_y(self.outBuffer))
        result = self.new_line.join(["".join(row) for row in result_transposed])
        return result

class TTYCanvas(object):
    """
    canvas of a TTYFigure instance
    
    The canvas manages all transformations between data space and figure space
    accounting for scaling and pixels.
    """
    def __init__(
        self,
        shape   = None, # canvas height and width (tuple of 2 integers)
        margins = None, # fractional margins
        limit_x = None, # x-axis limits (tuple of two floats)
        limit_y = None  # y axis limits (tuple of two floats)
        ):
        self.shape         = shape or (50, 20)
        self.margins       = margins or (0.05, 0.1)
        self._limit_x      = limit_x or [0, 1]
        self._limit_y      = limit_y or [0, 1]
        self.auto_adjust   = True
        self.margin_factor = 1

    @property
    def x_size(self):
        """
        return the width
        """
        return self.shape[0]

    @property
    def y_size(self):
        """
        return the height
        """
        return self.shape[1]

    @property
    def margin_x(self):
        """
        return x margin
        """
        return self.margins[0]

    @property
    def margin_y(self):
        """
        return y margin
        """
        return self.margins[1]

    def limit_x(
        self,
        limit_lower = None, # float
        limit_upper = None  # float
        ):
        """
        get or set x limits of the current axes

        x_min, x_max = limit_x() # return the current limit_x
        limit_x(x_min, x_max)    # set the limit_x to x_min, x_max
        """
        if limit_lower is None and limit_upper is None:
            return self._limit_x
        elif hasattr(limit_lower, "__iter__"):
            self._limit_x = limit_lower[:2]
        else:
            self._limit_x = [limit_lower, limit_upper]
        if self._limit_x[0] == self._limit_x[1]:
            self._limit_x[1] += 1
        self._limit_x[0] -= self.mod_x
        self._limit_x[1] += self.mod_x

    def limit_y(
        self,
        limit_lower = None,
        limit_upper = None
        ):
        """
        get or set y limits of the current axes

        y_min, y_max = limit_x() # return the current limit_y
        limit_y(y_min, y_max)    # set the limit_y to y_min, y_max
        """
        if limit_lower is None and limit_upper is None:
            return self._limit_y
        elif hasattr(limit_lower, "__iter__"):
            self._limit_y = limit_lower[:2]
        else:
            self._limit_y = [limit_lower, limit_upper]
        if self._limit_y[0] == self._limit_y[1]:
            self._limit_y[1] += 1
        self._limit_y[0] -= self.mod_y
        self._limit_y[1] += self.mod_y

    @property
    def min_x(self):
        """
        return x lower limit
        """
        return self._limit_x[0]

    @property
    def max_x(self):
        """
        return x upper limit
        """
        return self._limit_x[1]

    @property
    def min_y(self):
        """
        return y lower limit
        """
        return self._limit_y[0]

    @property
    def max_y(self):
        """
        return y upper limit
        """
        return self._limit_y[1]

    @property
    def step_x(self):
        return float(self.max_x - self.min_x) / float(self.x_size)

    @property
    def step_y(self):
        return float(self.max_y - self.min_y) / float(self.y_size)

    @property
    def ratio(self):
        return self.step_y / self.step_x

    @property
    def mod_x(self):
        return (self.max_x - self.min_x) * self.margin_x

    @property
    def mod_y(self):
        return (self.max_y - self.min_y) * self.margin_y

    def extent(
        self,
        margin_factor = None
        ):
        margin_factor = margin_factor or self.margin_factor
        min_x = (self.min_x + self.mod_x * margin_factor)
        max_x = (self.max_x - self.mod_x * margin_factor)
        min_y = (self.min_y + self.mod_y * margin_factor)
        max_y = (self.max_y - self.mod_y * margin_factor)
        return (min_x, max_x, min_y, max_y)

    def extent_string(
        self,
        margin = None
        ):
        def transform(value, formatting):
            if abs(value) < 1:
                _string = "%+.2g" % value
            elif formatting is not None:
                _string = formatting % value
            else:
                _string = None
            return _string
        extent  = self.extent(margin)
        xformat = self.x_string()
        yformat = self.y_string()
        return transform(extent[0], xformat),\
               transform(extent[1], xformat),\
               transform(extent[2], yformat),\
               transform(extent[3], yformat)

    def x_string(self):
        if self.x_size < 16:
            x_string = None
        elif self.x_size < 23:
            x_string = "%+.2g"
        else:
            x_string = "%+g"
        return x_string

    def y_string(self):
        if self.x_size < 8:
            y_string = None
        elif self.x_size < 11:
            y_string = "%+.2g"
        else:
            y_string = "%+g"
        return y_string

    def coordinates_inside_buffer(
        self,
        x,
        y
        ):
        return (0 <= x < self.x_size) and (0 < y < self.y_size)

    def coordinates_inside_data(
        self,
        x,
        y
        ):
        """
        return Boolean to check if coördinate (x, y) is in the data box
        """
        return (self.min_x <= x < self.max_x) and (self.min_y <= y < self.max_y)

    def _clip_line(
        self,
        line_pt_1,
        line_pt_2
        ):
        """
        clip line to canvas
        """
        x_min = min(line_pt_1[0], line_pt_2[0])
        x_max = max(line_pt_1[0], line_pt_2[0])
        y_min = min(line_pt_1[1], line_pt_2[1])
        y_max = max(line_pt_1[1], line_pt_2[1])

        extent = self.extent()

        if line_pt_1[0] == line_pt_2[0]:
            return (
                (line_pt_1[0], max(y_min, extent[1])),
                (line_pt_1[0], min(y_max, extent[3]))
            )

        if line_pt_1[1] == line_pt_2[1]:
            return (
                (max(x_min, extent[0]), line_pt_1[1]),
                (min(x_max, extent[2]), line_pt_1[1])
            )

        if ((extent[0] <= line_pt_1[0] < extent[2]) and
            (extent[1] <= line_pt_1[1] < extent[3]) and
            (extent[0] <= line_pt_2[0] < extent[2]) and
            (extent[1] <= line_pt_2[1] < extent[3])):
            return line_pt_1, line_pt_2

        ts = [0.0,
              1.0,
              float(extent[0] - line_pt_1[0]) / (line_pt_2[0] - line_pt_1[0]),
              float(extent[2] - line_pt_1[0]) / (line_pt_2[0] - line_pt_1[0]),
              float(extent[1] - line_pt_1[1]) / (line_pt_2[1] - line_pt_1[1]),
              float(extent[3] - line_pt_1[1]) / (line_pt_2[1] - line_pt_1[1])
              ]
        ts.sort()

        if (ts[2] < 0) or (ts[2] >= 1) or (ts[3] < 0) or (ts[2] >= 1):
            return None

        result =\
            [(pt_1 + t * (pt_2 - pt_1))\
                for t in (ts[2], ts[3])\
                    for (pt_1, pt_2) in zip(line_pt_1, line_pt_2)]

        return (result[:2], result[2:])

def plot(
    x,
    y           = None,
    marker      = None,
    shape       = (50, 20),
    draw_axes   = True,
    newline     = "\n",
    plot_slope  = False,
    margin_x    = 0.05,
    margin_y    = 0.1,
    plot_labels = True,
    limit_x     = None,
    limit_y     = None
    ):

    flags = {
        "shape"       : shape,
        "draw_axes"   : draw_axes,
        "newline"     : newline,
        "marker"      : marker,
        "plot_slope"  : plot_slope,
        "margins"     : (margin_x, margin_y),
        "plot_labels" : plot_labels
    }

    _figure = TTYFigure(**flags)

    print(_figure.plot(
        x,
        y,
        marker = marker,
        plot_slope = plot_slope,
        limit_x    = limit_x,
        limit_y    = limit_y
    ))

def steppify(x, y):
    """
    Steppify a curve (x, y). This is useful for filling histograms manually.
    """
    dx = 0.5 * (x[1:] + x[:-1])
    xx = numpy.zeros(2 * len(dx), dtype=float)
    yy = numpy.zeros(2 * len(y), dtype=float)
    xx[0::2], xx[1::2] = dx, dx
    yy[0::2], yy[1::2] = y, y
    xx = numpy.concatenate((
        [x[0] - (dx[0] - x[0])],
        xx,
        [x[-1] + (x[-1] - dx[-1])]
    ))
    return xx, yy

def stemify(x, y):
    """
    Stemify a curve (x, y). This is useful for filling histograms manually.
    """
    xx = numpy.zeros(3 * len(x), dtype=float)
    yy = numpy.zeros(3 * len(y), dtype=float)
    xx[0::3], xx[1::3], xx[2::3] = x, x, x
    yy[1::3] = y
    return xx, yy

def histogram(
    x,
    bins           = 10,
    normalized     = False,
    weights        = None,
    density        = None,
    histogram_type = "stem",
    shape          = (50, 20),
    draw_axes      = True,
    newline        = "\n",
    marker         = "_.",
    plot_slope     = False,
    margin_x       = 0.05,
    margin_y       = 0.1,
    plot_labels    = True,
    limit_x        = None,
    limit_y        = None
    ):

    from numpy import histogram

    if histogram_type not in ["None", "stem", "step"]:
        raise ValueError("histogram_type must be in [None, stem, step]")

    n, b = histogram(
        x,
        bins    = bins,
        range   = limit_x,
        normed  = normalized,
        weights = weights,
        density = density
    )

    _x = 0.5 * (b[:-1] + b[1:])
    if histogram_type == "step":
        step(_x, n.astype(float))
    elif histogram_type == "stem":
        stem(_x, n.astype(float))
    else:
        _y = n.astype(float)
        plot(
            _x,
            _y,
            shape       = shape,
            draw_axes   = draw_axes,
            newline     = newline,
            marker      = marker,
            plot_slope  = plot_slope,
            margin_x    = margin_x,
            margin_y    = margin_y,
            plot_labels = plot_labels,
            limit_x     = limit_x,
            limit_y     = limit_y
        )

def step(
    x,
    y,
    shape       = (50, 20),
    draw_axes   = True,
    newline     = "\n",
    marker      = "_.",
    plot_slope  = True,
    margin_x    = 0.05,
    margin_y    = 0.1,
    plot_labels = True,
    limit_x     = None,
    limit_y     = None
    ):
    _x, _y = steppify(x, y)
    plot(
        _x,
        _y,
        shape       = shape,
        draw_axes   = draw_axes,
        newline     = newline,
        marker      = marker,
        plot_slope  = plot_slope,
        margin_x    = margin_x,
        margin_y    = margin_y,
        plot_labels = plot_labels,
        limit_x     = limit_x,
        limit_y     = limit_y
    )


def stem(
    x,
    y,
    shape       = (50, 20),
    draw_axes   = True,
    newline     = "\n",
    marker      = "_.",
    plot_slope  = True,
    margin_x    = 0.05,
    margin_y    = 0.1,
    plot_labels = True,
    limit_x     = None,
    limit_y     = None
    ):

    _x, _y = stemify(x, y)
    plot(
        _x,
        _y,
        shape       = shape,
        draw_axes   = draw_axes,
        newline     = newline,
        marker      = marker,
        plot_slope  = plot_slope,
        margin_x    = margin_x,
        margin_y    = margin_y,
        plot_labels = plot_labels,
        limit_x     = limit_x,
        limit_y     = limit_y
    )

def histogram2D(
    x,
    y,
    bins             = [50, 20],
    histogramRange   = None,
    normalized       = False,
    weights          = None,
    number_of_colors = 16,
    width            = 50,
    percentiles      = None
    ):

    image, ex, ey = numpy.histogram2d(
        x,
        y,
        bins,
        range   = histogramRange,
        normed  = normalized,
        weights = weights
    )

    if percentiles is None:
        show_image(
            image,
            extent           = [min(ex), max(ex), min(ey), max(ey)],
            number_of_colors = number_of_colors,
            width            = width
        )
    else:
        percentile_show_image(
            image,
            levels           = percentiles,
            extent           = None,
            width            = width,
            number_of_colors = None
        )

def percentile_show_image(
    image,
    levels           = [68, 95, 99],
    extent           = None,
    width            = 50,
    number_of_colors = 16
    ):
    _image  = image.astype(float)
    _image -= image.min()
    _image /= _image.max()

    n = len(levels)
    for e, lk in enumerate(sorted(levels)):
        _image[_image <= 0.01 * float(lk)] = n - e

    show_image(
        1. - _image,
        extent           = extent,
        width            = width,
        number_of_colors = number_of_colors
    )

def show_image(
    image,
    extent           = None,
    width            = 50,
    number_of_colors = 16
    ):

    from scipy import ndimage

    width0 = image.shape[0]
    _image = ndimage.zoom(
        image.astype(float),
        float(width) / float(width0)
    )

    _image -= image.min()
    _image /= _image.max()

    width, height = _image.shape[:2]

    if len(image.shape) > 2:
        _color = True
    else:
        _color = False

    if number_of_colors == 16:
        color = "MNHQ$OC?7>!:-;. "[::-1]
    else:
        color = """
        $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. 
        """[::-1]
    number_of_colors = len(color)

    string = ""
    if not _color:
        for h in xrange(height):
            for w in xrange(width):
                string += color[int(_image[w, h] * (number_of_colors - 1))]
            string += "\n"
    else:
        for h in xrange(height):
            for w in xrange(width):
                string += color[int(sum(_image[w, h]) * (number_of_colors - 1))]
            string += "\n"
    print(string)

def sign(x):
    """
    sign of number
    - -1 : negative sign
    - 0:   null
    - 1:   positive
    """
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

def transpose(matrix):
    """
    transpose 2D matrix (list)
    """
    return [[x[i] for x in matrix] for i in range(len(matrix[0]))]

def reverse_y(matrix):
    """
    reverse y-axis of 2D matrix
    """
    return [list(reversed(matrix_i)) for matrix_i in matrix]

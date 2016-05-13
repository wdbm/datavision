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
from __future__ import division

name    = "datavision"
version = "2016-05-13T0409Z"

import itertools
import math
import matplotlib.pyplot
import numpy
import operator
import os
import PIL.Image
import random
import scipy.stats
import sys

import pyprel
import shijian

class Dataset(object):

    def __init__(
        self
        ):
        self._index = 0
        self._data  = {}

    def index(
        number = None
    ):
        if number is not None:
            self._index = number
        return self._index

    def indices(
        self
    ):
        return [index for index in self._data]

    def variable(
        self,
        index = None,
        name  = None,
        value = None
    ):
        if index is not None:
            self._index = index
        if name is not None:
            if value is not None:
                try:
                    self._data[self._index][name] = value
                except:
                    self._data[self._index] = {}
                    self._data[self._index][name] = value
        return self._data[self._index][name]

    def variables(
        self,
        index = 0
    ):
        return sorted([
            variable for variable, value in self._data[self._index].iteritems()
        ])

    def values(
        self,
        name = None
    ):
        return [self._data[index][name] for index in self.indices()]

    def table(
        self
    ):
        table_contents = ["index"]
        table_contents.extend(self.variables())
        table_contents = [table_contents]
        for index in self.indices():
            values = [
                str(self.variable(
                    name = name,
                    index = index
                )) for name in self.variables()]
            row = [str(index)]
            row.extend(values)
            table_contents.append(row)
        return pyprel.Table(
            contents = table_contents
        )

    def normalize(
        self,
        name      = None,
        summation = None
    ):
        values_raw = self.values(name = name)
        values_normalized = normalize(
            values_raw,
            summation = summation
        )
        for index_normalized, index in enumerate(self.indices()):
            self.variable(
                index = index,
                name  = name,
                value = values_normalized[index_normalized]
            )

    def normalize_all(
        self
    ):
        for name in self.variables():
            self.normalize(name = name)

    def preprocess(
        self,
        name = None
    ):
        from sklearn import preprocessing
        values_raw = self.values(name = name)
        values_preprocessed = list(preprocessing.scale(values_raw))
        for index_preprocessed, index in enumerate(self.indices()):
            self.variable(
                index = index,
                name  = name,
                value = values_preprocessed[index_preprocessed]
            )

    def preprocess_all(
        self,
        skip_variables = ["class"]
    ):
        for name in self.variables():
            if name not in skip_variables:
                self.preprocess(name = name)

    def shuffle(
        self,
        name = None,
        seed = 100
    ):
        random.seed(seed)
        values = self.values(name = name)
        random.shuffle(values)
        for index_shuffled, index in enumerate(self.indices()):
            self.variable(
                index = index,
                name  = name,
                value = values[index_shuffled]
            )

    def shuffle_all(
        self,
        seed = 100
    ):
        for name in self.variables():
            self.shuffle(
                name = name,
                seed = seed
            )

    def add(
        self,
        dataset = None
    ):
        index_current_maximum = max(self.indices())
        for index_offset, index in enumerate(dataset.indices()):
            for name in dataset.variables():
                self.variable(
                    index = index_current_maximum + 1 + index_offset,
                    name  = name,
                    value = dataset.variable(
                                index = index,
                                name  = name
                            )
                )

class Matrix(list):
    
    def __init__(
        self,
        title                    = None,
        number_of_columns        = 3,
        number_of_rows           = 3,
        element                  = 0.0,
        randomise                = False,
        randomise_limit_lower    = -0.2,
        randomise_limit_upper    = 0.2,
        *args
        ):
        matplotlib.pyplot.ion()
        # list initialisation
        if sys.version_info >= (3, 0):
            super().__init__(self, *args)
        else:
            super(Matrix, self).__init__(*args)        
        self.title               = title
        self.number_of_columns   = number_of_columns
        self.number_of_rows      = number_of_rows
        self.element             = element
        self.randomise           = randomise
        self.randomise_limit_lower = randomise_limit_lower
        self.randomise_limit_upper = randomise_limit_upper
        # fill with default element
        for column in range(self.number_of_columns):
            self.append([element] * self.number_of_rows)
        # fill with pseudorandom elements
        if self.randomise:
            random.seed()
            for row in range(self.number_of_rows):
                for column in range(self.number_of_columns):
                    self[row][column] = random.uniform(
                        self.randomise_limit_upper,
                        self.randomise_limit_lower
                    )
        # plot
        self._array = numpy.array(self)
        self._plot_number        = shijian.unique_number()
        # show or draw plot
        self._plot_shown         = False

    def plot(self):
        # display or redraw plot
        if self._plot_shown:
            matplotlib.pyplot.figure(str(self._plot_number))
            self._array = numpy.array(self)
            self._plot_axes.pcolor(
                self._array,
                cmap = matplotlib.pyplot.cm.Blues
            )
            matplotlib.pyplot.draw()
        else:
            self._plot_figure, \
            self._plot_axes = plot_list(
                list_object = self,
                title       = self.title,
                plot_number = self._plot_number,
                plot        = False,
                return_plot = True
            )
            matplotlib.pyplot.figure(str(self._plot_number))
            matplotlib.pyplot.show()
            self._plot_shown = True

    def save_plot(
        self,
        filename  = None,
        overwrite = False
        ):
        matplotlib.pyplot.figure(str(self._plot_number))
        filename_proposed = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )
        matplotlib.pyplot.savefig(
            filename_proposed,
            dpi = 700
        )

    def close_plot(self):
        matplotlib.pyplot.figure(str(self._plot_number))
        matplotlib.pyplot.close()
        self._plot_shown = False

def plot_list(
    list_object = None,
    title       = None,
    plot_number = None,
    style       = "colormap",
    filename    = None,
    overwrite   = False,
    plot        = True,
    return_plot = False,
    save        = False
    ):
    if not plot_number:
        plot_number = shijian.unique_number()
    if style == "colormap":
        # convert list to NumPy array
        array = numpy.array(list_object)
        dimensionality = len(array.shape)
        if dimensionality == 1:
            array = numpy.array([list_object])
        # create axis labels
        labels_column = list(range(0, array.shape[1]))
        labels_row = list(range(0, array.shape[0]))
        # create figure and axes
        figure = matplotlib.pyplot.figure(str(plot_number))
        axes = figure.add_subplot(111)
        colormap = axes.pcolor(array, cmap = matplotlib.pyplot.cm.Blues)
        # major ticks at middle of each cell
        axes.set_xticks(numpy.arange(array.shape[1]) + 0.5, minor = False)
        axes.set_yticks(numpy.arange(array.shape[0]) + 0.5, minor = False)
        # table-like display
        axes.invert_yaxis()
        axes.xaxis.tick_top()
        axes.set_xticklabels(labels_column, minor = False)
        axes.set_yticklabels(labels_row, minor = False)
        # LaTeX text
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
        # title
        if title:
            matplotlib.pyplot.title(title, y = 1.05)
        # plot/return/save
        if plot:
            matplotlib.pyplot.show()
        if return_plot:
            return(figure, axes)
        if save:
            filename_proposed = shijian.propose_filename(
                filename  = filename,
                overwrite = overwrite
            )
            matplotlib.pyplot.savefig(
                filename_proposed,
                dpi = 700
            )

def save_graph_matplotlib(
    values       = None,
    title        = None,
    title_axis_x = None,
    title_axis_y = None,
    filename     = None,
    directory    = ".",
    overwrite    = True,
    color        = "black",
    LaTeX        = False,
    markers      = True,
    marker_size  = 1,
    aspect       = None,
    line         = False,
    line_style   = "-",
    line_width   = 0.2,
    font_size    = 20
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if filename is None:
        if title is None:
            filename = "graph.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    # Turn off scientific notation.
    matplotlib.pyplot.gca().get_xaxis().get_major_formatter().set_scientific(False)
    matplotlib.pyplot.gca().get_yaxis().get_major_formatter().set_scientific(False)

    y = values
    x = range(0, len(y))

    figure = matplotlib.pyplot.figure()

    if title is not None:
        figure.suptitle(
            title,
            fontsize = font_size
        )

    if markers is True:
        matplotlib.pyplot.scatter(
            x,
            y,
            s          = marker_size,
            c          = color,
            edgecolors = "none",
        )
    if line is True:
        matplotlib.pyplot.plot(
            x,
            y,
            line_style,
            c         = color,
            linewidth = line_width
        )

    matplotlib.pyplot.xlabel(title_axis_x, fontsize = font_size)
    matplotlib.pyplot.ylabel(title_axis_y, fontsize = font_size)
    matplotlib.pyplot.xticks(fontsize = font_size)
    matplotlib.pyplot.yticks(fontsize = font_size)

    if not os.path.exists(directory):
        os.makedirs(directory)
    if aspect is None:
        matplotlib.pyplot.axes().set_aspect(
            1 / matplotlib.pyplot.axes().get_data_ratio()
        )
    else:
        matplotlib.pyplot.axes().set_aspect(aspect)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        dpi = 700
    )
    matplotlib.pyplot.close()

def save_multigraph_matplotlib(
    variables       = None,
    variables_names = None,
    title           = None,
    label_x         = "",
    label_y         = "",
    filename        = None,
    directory       = ".",
    overwrite       = True,
    LaTeX           = False,
    markers         = True,
    marker_size     = 1,
    line            = False,
    line_style      = "-",
    line_width      = 0.2,
    font_size       = 20,
    aspect          = None,
    palette_name    = "palette21"
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if filename is None:
        if title is None:
            filename = "multigraph.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    # Turn off scientific notation.
    matplotlib.pyplot.gca().get_xaxis().get_major_formatter().set_scientific(False)
    matplotlib.pyplot.gca().get_yaxis().get_major_formatter().set_scientific(False)

    figure = matplotlib.pyplot.figure()

    palette = pyprel.access_palette(
        name = palette_name,
        minimum_number_of_colors_needed = len(variables)
    )
    for values, name, color in zip(
        variables,
        variables_names,
        palette
        ):
        y = values
        x = range(0, len(y))
        if markers is True:
            matplotlib.pyplot.scatter(
                x,
                y,
                s          = marker_size,
                c          = color,
                edgecolors = "none",
                label      = name,
            )
        if line is True:
            matplotlib.pyplot.plot(
                x,
                y,
                line_style,
                c         = color,
                linewidth = line_width,
                #label     = name,
            )

    if title is not None:
        figure.suptitle(
            title,
            fontsize = 20
        )
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    legend = matplotlib.pyplot.legend(
        #loc            = "best",
        loc            = "center left",
        bbox_to_anchor = (1, 0.5),
        fontsize       = 10
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    if aspect is None:
        matplotlib.pyplot.axes().set_aspect(
            1 / matplotlib.pyplot.axes().get_data_ratio()
        )
    else:
        matplotlib.pyplot.axes().set_aspect(aspect)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        bbox_extra_artists = (legend,),
        bbox_inches        = "tight",
        dpi                = 700
    )
    matplotlib.pyplot.close()

def save_multigraph_2D_matplotlib(
    variables_x      = None,
    variables_y      = None,
    variables_names  = None,
    title            = None,
    label_x          = "",
    label_y          = "",
    filename         = None,
    directory        = ".",
    overwrite        = True,
    LaTeX            = False,
    markers         = True,
    marker_size     = 1,
    line            = False,
    line_style      = "-",
    line_width      = 0.2,
    font_size       = 20,
    aspect           = None,
    palette_name     = "palette21"
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if filename is None:
        if title is None:
            filename = "multigraph.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    # Turn off scientific notation.
    matplotlib.pyplot.gca().get_xaxis().get_major_formatter().set_scientific(False)
    matplotlib.pyplot.gca().get_yaxis().get_major_formatter().set_scientific(False)

    figure = matplotlib.pyplot.figure()

    palette = pyprel.access_palette(
        name = palette_name,
        minimum_number_of_colors_needed = len(variables_x)
    )
    for values_x, values_y, name, color in zip(
        variables_x,
        variables_y,
        variables_names,
        palette
        ):
        y = values_y
        x = values_x
        if markers is True:
            matplotlib.pyplot.scatter(
                x,
                y,
                s          = marker_size,
                c          = color,
                edgecolors = "none",
                label      = name,
            )
        if line is True:
            matplotlib.pyplot.plot(
                x,
                y,
                line_style,
                c         = color,
                linewidth = line_width,
                label     = name,
            )
    if title is not None:
        figure.suptitle(
            title,
            fontsize = 20
        )
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    legend = matplotlib.pyplot.legend(
        #loc            = "best",
        loc            = "center left",
        bbox_to_anchor = (1, 0.5),
        fontsize       = 10
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    if aspect is None:
        matplotlib.pyplot.axes().set_aspect(
            1 / matplotlib.pyplot.axes().get_data_ratio()
        )
    else:
        matplotlib.pyplot.axes().set_aspect(aspect)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        bbox_extra_artists = (legend,),
        bbox_inches        = "tight",
        dpi                = 700
    )
    matplotlib.pyplot.close()

def generate_sine_values(
    frequency   = 5,
    sample_rate = 16000,
    time        = 10
    ):
    sampling_interval = time / sample_rate
    values_time       = numpy.arange(0, time, sampling_interval)
    values_amplitude  = numpy.sin(2 * numpy.pi * frequency * values_time)
    return values_amplitude, values_time

def generate_composite_sine_values(
    frequencies = [5, 10, 15],
    sample_rate = 16000,
    time        = 10
    ):
    values_amplitude_list = []
    for frequency in frequencies:
        values_amplitude, values_time = generate_sine_values(
            frequency   = frequency,
            time        = time,
            sample_rate = sample_rate
        )
        values_amplitude_list.append(values_amplitude)
    values_amplitude_sum = sum(values_amplitude_list)
    return values_amplitude_sum, values_time

def greatest_frequency_contributions_FFT(
    values_amplitude        = None,
    values_time             = None,
    time                    = None,
    sample_rate             = 16000,
    number_of_contributions = 10
    ):

    if values_time is None:
        sampling_interval = time / sample_rate
        values_time       = numpy.arange(0, time, sampling_interval)
    signal_length     = len(values_amplitude)
    values_indices    = numpy.arange(signal_length)
    if time is None:
        time = signal_length / sample_rate
    values_time = numpy.linspace(0, time, num = signal_length)
    # two sides frequency range
    frequencies       = values_indices / time
    # one side frequency range
    frequencies       = frequencies[range(int(signal_length / 2))] 
    # FFT
    weightings        = numpy.fft.fft(values_amplitude) / signal_length
    # normalization
    weightings        = weightings[range(int(signal_length / 2))]

    weightings_absolute = [abs(weighting) for weighting in list(weightings)]

    indices = shijian.indices_of_greatest_values(
        weightings_absolute,
        number = number_of_contributions
    )
    frequencies = [frequencies[index] for index in indices]

    return frequencies

def save_FFT_plot_matplotlib(
    values_amplitude       = None,
    values_time            = None,
    time                   = None,
    sample_rate            = 16000,
    filename               = "FFT.png",
    title_axis_x_amplitude = "time",
    title_axis_y_amplitude = "amplitude",
    title_axis_x_FFT       = "frequency",
    title_axis_y_FFT       = "|weighting|"
    ):

    if values_time is None:
        sampling_interval = time / sample_rate
        values_time       = numpy.arange(0, time, sampling_interval)
    signal_length     = len(values_amplitude)
    values_indices    = numpy.arange(signal_length)
    if time is None:
        time = signal_length / sample_rate
    values_time = numpy.linspace(0, time, num = signal_length)
    # two sides frequency range
    frequencies       = values_indices / time
    # one side frequency range
    frequencies       = frequencies[range(int(signal_length / 2))] 
    # FFT
    weightings        = numpy.fft.fft(values_amplitude) / signal_length
    # normalization
    weightings        = weightings[range(int(signal_length / 2))]

    figure, axes      = matplotlib.pyplot.subplots(2, 1)
    # plot amplitude versus time
    axes[0].plot(values_time, values_amplitude, "b", linewidth = 0.5)
    axes[0].set_xlabel(title_axis_x_amplitude)
    axes[0].set_ylabel(title_axis_y_amplitude)
    # plot FFT
    axes[1].plot(frequencies, abs(weightings), "r", linewidth = 0.5)
    axes[1].set_xlabel(title_axis_x_FFT)
    axes[1].set_ylabel(title_axis_y_FFT)

    figure.savefig(
        filename,
        dpi = 700
    )

def dot_product(v1, v2):
    return(sum((a * b) for a, b in zip(v1, v2)))

def magnitude(v):
    return(numpy.linalg.norm(v))
    #return(math.sqrt(dot_product(v, v)))

def angle(v1, v2):
    cosine = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    cosine = 1 if cosine > 1 else cosine
    return(math.acos(cosine))

def composite_variable(x):
    k = len(x) + 1
    variable = 0
    for index, element in enumerate(x):
        variable += k**(index - 1) * element
    return variable

def normalize(
    x,
    summation = None
    ):
    if summation is None:
        summation = sum(x) # normalize to unity
    return [element/summation for element in x]

def normalize_to_range(
    values,
    minimum = 0.0,
    maximum = 1.0
    ):
    """
    This function normalizes values of a list to a specified range and returns
    the original object if the values are not of the types integer or float.
    """
    normalized_values = []
    minimum_value = min(values)
    maximum_value = max(values)
    for value in values:
        numerator = value - minimum_value
        denominator = maximum_value - minimum_value
        value_normalized = (maximum - minimum) * numerator/denominator + minimum
        normalized_values.append(value_normalized)
    return normalized_values

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

def mean(
    values,
    ):
    array_of_values = numpy.array(values)
    mean = array_of_values.mean()
    return mean

def standard_deviation(
    values,
    ):
    array_of_values = numpy.array(values)
    standard_deviation = array_of_values.std()
    return standard_deviation

def interquartile_range(
    values,
    ):
    array_of_values = numpy.array(values)
    interquartile_range = numpy.percentile(values, 75) -\
                          numpy.percentile(values, 25)
    return interquartile_range

def list_element_combinations_variadic(
    elements_specification
    ):
    """
    This function accepts a specification of lists of elements for each place in
    lists in the form of a list, the elements of which are lists of possible
    elements and returns a list of lists corresponding to the combinations of
    elements of the specification with varying numbers of elements.

    For example, the list elements specification [[10, 20], [30, 40], [50, 60]]
    yields the following lists:

    [10]
    [20]
    [10, 30]
    [10, 40]
    [20, 30]
    [20, 40]
    [10, 30, 50]
    [10, 30, 60]
    [10, 40, 50]
    [10, 40, 60]
    [20, 30, 50]
    [20, 30, 60]
    [20, 40, 50]
    [20, 40, 60]
    """
    lists = [list(list_generated) for index, element_specification in enumerate(elements_specification) for list_generated in itertools.product(*elements_specification[:index + 1])]
    return lists

def correlation_linear(
    values_1,
    values_2,
    printout = None
    ):
    """
    This function calculates the Pearson product-moment correlation coefficient.
    This is a measure of the linear collelation of two variables. The value can
    be between +1 and -1 inclusive, where 1 is total positive correlation, 0 is
    no correlation and -1 is total negative correlation. It is a measure of the
    linear dependence between two variables.

    This function also calculates the significance (2-tailed p-value) of the
    correlation coefficient given the sample size.
    """
    r, p_value = scipy.stats.pearsonr(values_1, values_2)
    if printout is not True:
        return r, p_value
    else:
        text = (
            "Pearson linear correlation coefficient: {r}\n"
            "2-tailed p-value: {p_value}"
        ).format(
            r       = r,
            p_value = p_value
        )
        return text

def analyze_correlations(
    variables            = None,
    variables_names      = None,
    table_order_variable = "r",
    combined_graph       = True,
    individual_graphs    = True,
    generate_plots       = True,
    directory            = "analysis_correlations"
    ):

    # Create a list of variable values combined with their names.
    variable_collection = []
    for variable, variable_name in zip(variables, variables_names):
        variable_collection.append([variable, variable_name])

    # Loop over all pair combinations of variable values with their respective
    # names and calculate their correlations. Generate and print a table.
    table_title = [[
        "variable combination",
        "linear correlation",
        "correlation p-value"
    ]]
    table_contents = []
    variable_collections_combinations = list(itertools.combinations(variable_collection, 2))
    for variable_combination in variable_collections_combinations:
        variable_1_values = variable_combination[0][0]
        variable_1_name = variable_combination[0][1]
        variable_2_values = variable_combination[1][0]
        variable_2_name = variable_combination[1][1]
        label = variable_1_name + " versus " + variable_2_name
        r, p_value = correlation_linear(variable_1_values, variable_2_values)
        table_contents.append([label, str(r), str(p_value)])

    # Order the table contents by correlation or p-value.
    if table_order_variable == "r":
        table_order_variable_index = 1
    if table_order_variable == "p_value":
        table_order_variable_index = 2
    table_contents_sorted = sorted(
        table_contents,
        key     = operator.itemgetter(table_order_variable_index),
        reverse = True
    )
    table_contents = table_title
    table_contents.extend(table_contents_sorted)

    print(pyprel.Table(
        contents = table_contents
    ))
    if generate_plots is True:
        if combined_graph is True:
            save_graph_all_combinations_matplotlib(
                variables        = variables,
                variables_names  = variables_names,
                title            = "variable correlations",
                filename         = "variable_correlations.png",
                directory        = "analysis_correlations"
            )
        if individual_graphs is True:
            save_graphs_all_combinations_matplotlib(
                variables        = variables,
                variables_names  = variables_names,
                directory        = "analysis_correlations"
            )

def frange(x, y, step):
    while x < y:
        yield x
        x += step

def scale_list(
    values = None,
    factor = None,
    ):
    return [factor * value for value in values]

def propose_number_of_bins(
    values,
    binning_logic_system = None,
    ):
    """
    This function returns a proposal for binning for a histogram of a specified
    list using an optional specified binning logic system.

    Freedman-Diaconis: bin width is proportional to the interquartile range of
                       the data divided by the cube root of the size of the data

    Scott:             bin width is proportional to the standard deviation of
                       the values divided by the cube root of the size of the
                       data
    """
    # Set the default binning logic system.
    if binning_logic_system is None:
        binning_logic_system = "Scott"
    # Engage the requested logic system.
    if binning_logic_system == "Freedman-Diaconis":
        #log.debug("engage Freedman-Diaconis binning logic")
        bin_size =\
            2 * interquartile_range(values) * \
            len(values) ** (-1/3)
    elif binning_logic_system == "Scott":
        #log.debug("engage Scott binning logic")
        bin_size =\
            3.5 * standard_deviation(values) * \
            len(values) ** (-1/3)
    else:
        log.error("undefined binning logic system requested")
        raise(ValueError)
    number_of_bins = (max(values) - min(values)) / bin_size
    if numpy.isinf(number_of_bins) or numpy.isnan(number_of_bins):
        number_of_bins = len(set(values)) # number of unique values
        #log.debug(
        #    "binning algorithms ineffective -- " +
        #    "propose binning by unique values"
        #)
    return int(round(number_of_bins))

def save_graph_all_combinations_matplotlib(
    variables        = None,
    variables_names  = None,
    title            = None,
    label_x          = "",
    label_y          = "",
    filename         = None,
    directory        = ".",
    overwrite        = True,
    LaTeX            = False,
    marker_size      = 1
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if filename is None:
        if title is None:
            filename = "graph_all_combinations.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    # Turn off scientific notation.
    matplotlib.pyplot.gca().get_xaxis().get_major_formatter().set_scientific(False)
    matplotlib.pyplot.gca().get_yaxis().get_major_formatter().set_scientific(False)
    
    figure = matplotlib.pyplot.figure()

    # Create a list of variable values combined with their names.
    variable_collection = []
    for variable, variable_name in zip(variables, variables_names):
        variable_collection.append([variable, variable_name])

    # Loop over all pair combinations of variable values with their respective
    # names and add them to the plot.
    variable_collections_combinations = list(itertools.combinations(variable_collection, 2))
    number_of_combinations = len(variable_collections_combinations)
    palette = pyprel.access_palette(name = "palette21")
    palette.extend_palette(
        minimum_number_of_colors_needed = number_of_combinations
    )
    for variable_combination, color in zip(
        variable_collections_combinations,
        palette
        ):
        variable_1_values = variable_combination[0][0]
        variable_1_name   = variable_combination[0][1]
        variable_2_values = variable_combination[1][0]
        variable_2_name   = variable_combination[1][1]
        label             = variable_1_name + " versus " + variable_2_name
        matplotlib.pyplot.scatter(
            variable_1_values,
            variable_2_values,
            s          = marker_size,
            c          = color,
            edgecolors = "none",
            label      = label,
        )

    if title is not None:
        figure.suptitle(title, fontsize = 20)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    legend = matplotlib.pyplot.legend(
        #loc            = "best",
        loc            = "center left",
        bbox_to_anchor = (1, 0.5),
        fontsize       = 10
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        bbox_extra_artists = (legend,),
        bbox_inches        = "tight",
        dpi                = 700
    )
    matplotlib.pyplot.close()

def save_graphs_all_combinations_matplotlib(
    variables        = None,
    variables_names  = None,
    directory        = ".",
    overwrite        = True,
    LaTeX            = False
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")

    marker_size = 1

    # Turn off scientific notation.
    matplotlib.pyplot.gca().get_xaxis().get_major_formatter().set_scientific(False)
    matplotlib.pyplot.gca().get_yaxis().get_major_formatter().set_scientific(False)

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a list of variable values combined with their names.
    variable_collection = []
    for variable, variable_name in zip(variables, variables_names):
        variable_collection.append([variable, variable_name])

    # Loop over all pair combinations of variable values with their respective
    # names and plot them.
    variable_collections_combinations = list(itertools.combinations(variable_collection, 2))
    number_of_combinations = len(variable_collections_combinations)
    for variable_combination in variable_collections_combinations:
        variable_1_values = variable_combination[0][0]
        variable_1_name   = variable_combination[0][1]
        variable_2_values = variable_combination[1][0]
        variable_2_name   = variable_combination[1][1]
        label             = variable_1_name + " versus " + variable_2_name
        label_x           = variable_1_name
        label_y           = variable_2_name
        filename = shijian.propose_filename(
            filename  = directory + "/" + label.replace(" ", "_") + ".png",
            overwrite = overwrite
        )
        figure = matplotlib.pyplot.figure()
        figure.suptitle(label, fontsize = 20)
        #figure.set_size_inches(7.87, 7.87)
        #figure.tight_layout()
        matplotlib.pyplot.scatter(
            variable_1_values,
            variable_2_values,
            s          = marker_size,
            c          = "#000000",
            edgecolors = "none",
            #label      = label,
        )
        matplotlib.pyplot.xlabel(label_x)
        matplotlib.pyplot.ylabel(label_y)
        #legend = matplotlib.pyplot.legend(
        #    #loc            = "best",
        #    loc            = "center left",
        #    bbox_to_anchor = (1, 0.5),
        #    fontsize       = 10
        #)
        #print("save {filename}".format(filename = filename))
        matplotlib.pyplot.savefig(
            filename,
            #bbox_extra_artists = (legend,),
            bbox_inches = "tight",
            dpi         = 700
        )
        matplotlib.pyplot.close()

def save_parallel_coordinates_matplotlib(
    datasets,
    styles              = None,
    title               = None,
    label_x             = "",
    label_y             = "",
    labels_ticks_x_axis = None, # under consideration
    filename            = None,
    directory           = ".",
    overwrite           = True,
    LaTeX               = False
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if filename is None:
        if title is None:
            filename = "parallel_coordinates.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    dimensions = len(datasets[0])
    if labels_ticks_x_axis is None:
        labels_ticks_x_axis = range(dimensions)
    figure, axes        = matplotlib.pyplot.subplots(
        1,
        dimensions - 1,
        sharey  = False,
        figsize = (14, 14)
    )

    # If no list of line styles is set, create a list of colors for lines.
    if styles is None:
        colors = pyprel.access_palette(
            name = "palette21",
            minimum_number_of_colors_needed = len(datasets)
        )
        styles = colors

    # Calculate limits of data for each feature.
    range_minimum_maximum = list()
    for dataset in zip(*datasets):
        minimum_value = min(dataset)
        maximum_value = max(dataset)
        if minimum_value == maximum_value:
            minimum_value -= 0.5
            maximum_value = minimum_value + 1.
        range_of_values = float(maximum_value - minimum_value)
        range_minimum_maximum.append((
            minimum_value,
            maximum_value,
            range_of_values
        ))

    # Normalize datasets.
    datasets_normalized = list()
    for dataset in datasets:
        dataset_normalized = [
            (value - range_minimum_maximum[dimension][0]) /
            range_minimum_maximum[dimension][2]
            for dimension, value in enumerate(dataset)
        ]
        datasets_normalized.append(dataset_normalized)
    datasets = datasets_normalized

    # Plot datasets on all subplots.
    for index_axis, axis in enumerate(axes):
        for index_dataset, dataset in enumerate(datasets):
            axis.plot(labels_ticks_x_axis, dataset, styles[index_dataset])
        axis.set_xlim([
            labels_ticks_x_axis[index_axis],
            labels_ticks_x_axis[index_axis + 1]
        ])

    # Set all y-axis ticks except last.
    for dimension, (axes_most, label_tick_x_axis) in enumerate(zip(axes, labels_ticks_x_axis[:-1])):
        axes_most.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([label_tick_x_axis]))
        number_of_ticks    = len(axes_most.get_yticklabels())
        labels_ticks       = list()
        step_ticks         = range_minimum_maximum[dimension][2] / (number_of_ticks - 1)
        value_minimum_tick = range_minimum_maximum[dimension][0]
        labels_ticks = [
            "{value:4.2f}".format(
                value = (value_minimum_tick + index_tick * step_ticks)
            ) for index_tick in xrange(number_of_ticks)
        ]
        axes_most.set_yticklabels(labels_ticks)

    # Set all last y-axis ticks to the right of the plot.
    axes_last = matplotlib.pyplot.twinx(axes[-1])
    dimension += 1
    axes_last.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([
        labels_ticks_x_axis[-2], labels_ticks_x_axis[-1]
    ]))
    number_of_ticks    = len(axes_last.get_yticklabels())
    step_ticks         = range_minimum_maximum[dimension][2] / (number_of_ticks - 1)
    value_minimum_tick = range_minimum_maximum[dimension][0]
    labels_ticks = [
        "{value:4.2f}".format(
            value = (value_minimum_tick + index_tick * step_ticks)
        ) for index_tick in xrange(number_of_ticks)
    ]
    axes_last.set_yticklabels(labels_ticks)

    # Stack subplots.
    matplotlib.pyplot.subplots_adjust(wspace = 0)

    if title is not None:
        figure.suptitle(title, fontsize = 20)
    matplotlib.pyplot.xlabel(label_x)
    matplotlib.pyplot.ylabel(label_y)
    #legend = matplotlib.pyplot.legend(
    #    #loc            = "best",
    #    loc            = "center left",
    #    bbox_to_anchor = (1, 0.5),
    #    fontsize       = 10
    #)
    if not os.path.exists(directory):
        os.makedirs(directory)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        #bbox_extra_artists = (legend,),
        bbox_inches        = "tight",
        dpi                = 700
    )
    matplotlib.pyplot.close()

def save_histogram_matplotlib(
    values,
    filename       = None,
    directory      = ".",
    number_of_bins = None,
    color_fill     = "#3861AA",
    color_edge     = "none",
    normalize      = False,
    label_x        = "frequency",
    label_y        = None,
    title          = None,
    overwrite      = True,
    LaTeX          = False,
    aspect         = None,
    font_size      = 20
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if number_of_bins is None:
        number_of_bins = propose_number_of_bins(values)
    if filename is None:
        if title is None:
            filename = "histogram.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )
    n, bins, patches = matplotlib.pyplot.hist(
        values,
        number_of_bins,
        normed    = int(normalize),
        facecolor = color_fill,
        edgecolor = color_edge,
        alpha     = 1
    )
    if label_x is not None:
        matplotlib.pyplot.xlabel(label_x, fontsize = font_size)
    if label_y is not None:
        matplotlib.pyplot.ylabel(label_y, fontsize = font_size)
    matplotlib.pyplot.xticks(fontsize = font_size)
    matplotlib.pyplot.yticks(fontsize = font_size)
    if title is not None:
        matplotlib.pyplot.title(title, fontsize = font_size)
    #matplotlib.pyplot.subplots_adjust(left = 0.15)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if aspect is None:
        matplotlib.pyplot.axes().set_aspect(
            1 / matplotlib.pyplot.axes().get_data_ratio()
        )
    else:
        matplotlib.pyplot.axes().set_aspect(aspect)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        dpi = 700
    )
    matplotlib.pyplot.close()

def save_histogram_comparison_matplotlib(
    values_1       = None,
    values_2       = None,
    filename       = None,
    directory      = ".",
    number_of_bins = None,
    normalize      = True,
    label_x        = "",
    label_y        = None,
    label_ratio_x  = "frequency",
    label_ratio_y  = "ratio",
    title          = None,
    label_1        = "1",
    label_2        = "2",
    overwrite      = True,
    LaTeX          = False,
    #aspect         = None,
    font_size      = 20
    ):

    matplotlib.pyplot.ioff()
    if LaTeX is True:
        matplotlib.pyplot.rc("text", usetex = True)
        matplotlib.pyplot.rc("font", family = "serif")
    if number_of_bins is None:
        number_of_bins_1 = propose_number_of_bins(values_1)
        number_of_bins_2 = propose_number_of_bins(values_2)
        number_of_bins   = int((number_of_bins_1 + number_of_bins_2) / 2)
    if filename is None:
        if title is None:
            filename = "histogram_comparison.png"
        else:
            filename = shijian.propose_filename(
                filename  = title.replace(" ", "_") + ".png",
                overwrite = overwrite
            )
    else:
        filename = shijian.propose_filename(
            filename  = filename,
            overwrite = overwrite
        )

    values = []
    values.append(values_1)
    values.append(values_2)
    bar_width = 0.8
    figure, (axis_1, axis_2) = matplotlib.pyplot.subplots(
        nrows       = 2,
        gridspec_kw = {"height_ratios": (2, 1)}
    )
    ns, bins, patches = axis_1.hist(
        values,
        color     = [
                        (  0 / 255,  85 / 255, 160 / 255), # #3861AA
                        (  0 / 255, 255 / 255,   0 / 255)  # #00FF00
                    ],
        normed    = normalize,
        histtype  = "stepfilled",
        bins      = number_of_bins,
        alpha     = 0.5,
        label     = [label_1, label_2],
        rwidth    = bar_width,
        linewidth = 0
    )
    axis_1.legend(
        loc = "best"
    )
    bars = axis_2.bar(
        bins[:-1],
        ns[0] / ns[1],
        alpha     = 0.5,
        linewidth = 0,
        width     = bins[1] - bins[0]
    )
    for bar in bars:
        bar.set_color("#00B9BC")
    axis_1.set_xlabel(label_x, fontsize = font_size)
    axis_1.set_ylabel(label_y, fontsize = font_size)
    axis_2.set_xlabel(label_ratio_x, fontsize = font_size)
    axis_2.set_ylabel(label_ratio_y, fontsize = font_size)
    #axis_1.xticks(fontsize = font_size)
    #axis_1.yticks(fontsize = font_size)
    #axis_2.xticks(fontsize = font_size)
    #axis_2.yticks(fontsize = font_size)
    matplotlib.pyplot.suptitle(title, fontsize = font_size)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #if aspect is None:
    #    matplotlib.pyplot.axes().set_aspect(
    #        1 / matplotlib.pyplot.axes().get_data_ratio()
    #    )
    #else:
    #    matplotlib.pyplot.axes().set_aspect(aspect)
    matplotlib.pyplot.savefig(
        directory + "/" + filename,
        dpi = 700
    )
    matplotlib.pyplot.close()

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
        update_zus
        ):
        symmetric_difference_set = \
            set(zu[0] for zu in self) ^ set(zu[0] for zu in update_zus)
        return(
            [zu for zu in self if zu[0] in symmetric_difference_set] +
            [zu for zu in update_zus if zu[0] in symmetric_difference_set]
        )

    def intersection(
        self,
        update_zus
        ):
        intersection_set = \
            set(zu[0] for zu in self) & set(zu[0] for zu in update_zus)
        return(
            [zu for zu in self if zu[0] in intersection_set] +
            [zu for zu in update_zus if zu[0] in intersection_set]
        )

    def update(
        self,
        update_zus
        ):
        self_updated = []
        # Get the symmetric difference zus of the current zus and the update
        # zus. Include the symmetric difference zus in the updated self zus.
        symmetric_difference = self.symmetric_difference(update_zus)
        symmetric_difference_set = set(zu[0] for zu in symmetric_difference)
        self_updated.extend(symmetric_difference)
        # Include all entries of the update zus not in the symmetric difference
        # zus in the updated self zus.        
        self_updated.extend(
            [zu for zu in update_zus \
            if zu[0] not in symmetric_difference_set]
        )
        # Update the self zus.
        self.__init__(self_updated)

class TTYFigureData(object):
    """
    data container of TTYFigure
    """

    markers = {
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
        self.out_buffer    = None
        self.tick_symbols  = u"\u253C"  # "+"
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
            self.out_buffer[zero_x][y] = self.y_axis_symbol

        zero_y = self.get_coordinates(
            0,
            self.canvas.min_y,
            self.canvas.step_y,
            limits = [1, self.canvas.y_size])
        if zero_y >= self.canvas.y_size:
            zero_y = self.canvas.y_size - 1
        for x in xrange(self.canvas.x_size):
            self.out_buffer[x][zero_y] = self.x_axis_symbol # u"\u23bc"

        self.out_buffer[zero_x][zero_y] = self.tick_symbols # "+"

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

        self.out_buffer[x_zero_coordinates][min_y_coordinates] = self.tick_symbols
        self.out_buffer[x_zero_coordinates][max_y_coordinates] = self.tick_symbols
        self.out_buffer[min_x_coordinates][y_zero_coordinates] = self.tick_symbols
        self.out_buffer[max_x_coordinates][y_zero_coordinates] = self.tick_symbols

        min_x_string, max_x_string, min_y_string, max_y_string =\
            self.canvas.extent_string()
        if self.canvas.x_string() is not None:
            for i, c in enumerate(min_x_string):
                self.out_buffer[
                    min_x_coordinates + i + 1
                ][
                    y_zero_coordinates - 1
                ] = c
            for i, c in enumerate(max_x_string):
                self.out_buffer[
                    max_x_coordinates + i - len(max_x_string)
                ][
                    y_zero_coordinates - 1
                ] = c

        if self.canvas.y_string() is not None:
            for i, c in enumerate(max_y_string):
                self.out_buffer[
                    x_zero_coordinates + i + 1
                ][
                    max_y_coordinates
                ] = c
            for i, c in enumerate(min_y_string):
                self.out_buffer[
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
                self.out_buffer[x0 + x][current_y] = current_draw_symbol
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
                self.out_buffer[
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
                    self.out_buffer[x_coordinates][y_coordinates] = draw_symbol

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
                        self.out_buffer[
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

        figure_data = TTYFigureData(
            x_values,
            y_values,
            marker = marker,
            plot_slope = plot_slope
        )
        self.append_data(figure_data)

        if limit_x is not None:
            self.canvas.limit_x(limit_x)

        if limit_y is not None:
            self.canvas.limit_y(limit_x)

        return self.draw()

    def draw(self):
        self.out_buffer =\
            [[" "] * self.canvas.y_size for i in range(self.canvas.x_size)]
        if self.draw_axes:
            self._draw_axes()

        for dk in self.data:
            self._plot_data(dk)

        if self.plot_labels:
            self._plot_labels()
        result_transposed = transpose(reverse_y(self.out_buffer))
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
    histogram_range  = None,
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
        range   = histogram_range,
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

def difference_RMS_images(
    filename_1 = None,
    filename_2 = None
    ):
    histogram_1 = PIL.Image.open(filename_1).histogram()
    histogram_2 = PIL.Image.open(filename_2).histogram()
    try:
        RMS = math.sqrt(reduce(operator.add, map(
            lambda a, b: (a - b)**2, histogram_1, histogram_2)) / len(histogram_1)
        )
    except:
        RMS = None
    return RMS

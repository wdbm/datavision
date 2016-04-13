#!/usr/bin/env python
from __future__ import division

import numpy

import datavision
import shijian

def main():

    time        = 1
    sample_rate = 500

    values_amplitude_1, values_time_1 = datavision.generate_sine_values(
        frequency   = 5,
        time        = time,
        sample_rate = sample_rate
    )
    values_amplitude_2, values_time_2 = datavision.generate_sine_values(
        frequency   = 10,
        time        = time,
        sample_rate = sample_rate
    )
    values_amplitude_3, values_time_3 = datavision.generate_sine_values(
        frequency   = 15,
        time        = time,
        sample_rate = sample_rate
    )
    values_amplitude_4, values_time_3 = datavision.generate_sine_values(
        frequency   = 20,
        time        = time,
        sample_rate = sample_rate
    )
    values_amplitude_5, values_time_3 = datavision.generate_sine_values(
        frequency   = 25,
        time        = time,
        sample_rate = sample_rate
    )

    values_amplitude =\
        values_amplitude_1 +\
        values_amplitude_2 +\
        values_amplitude_3 +\
        values_amplitude_4 +\
        values_amplitude_5

    datavision.save_FFT_plot_matplotlib(
        values_amplitude = values_amplitude,
        time             = time,
        sample_rate      = sample_rate,
        filename         = "FFT.png"
    )

    number_of_contributions = 5

    print("{number} greatest frequency contributions: {frequencies}".format(
        number      = number_of_contributions,
        frequencies = datavision.greatest_frequency_contributions_FFT(
            values_amplitude        = values_amplitude,
            time                    = time,
            sample_rate             = sample_rate,
            number_of_contributions = number_of_contributions
        )
    ))

if __name__ == "__main__":
    main()

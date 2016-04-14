#!/usr/bin/env python
from __future__ import division

import numpy

import datavision
import shijian

def generate_composite_sine_values(
    frequencies = [5, 10, 15],
    sample_rate = 16000,
    time        = 10
    ):
    values_amplitude_list = []
    for frequency in frequencies:
        values_amplitude, values_time = datavision.generate_sine_values(
            frequency   = frequency,
            time        = time,
            sample_rate = sample_rate
        )
        values_amplitude_list.append(values_amplitude)
    values_amplitude_sum = sum(values_amplitude_list)
    return values_amplitude_sum, values_time

def main():

    time        = 1
    sample_rate = 300

    values_amplitude, values_time = generate_composite_sine_values(
        time        = time,
        sample_rate = sample_rate
    )

    datavision.save_FFT_plot_matplotlib(
        values_amplitude = values_amplitude,
        values_time      = values_time,
        time             = time,
        sample_rate      = sample_rate,
        filename         = "FFT.png"
    )

    number_of_contributions = 3

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

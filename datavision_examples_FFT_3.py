#!/usr/bin/env python
from __future__ import division

import numpy

import datavision

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
        frequency   = 100,
        time        = time,
        sample_rate = sample_rate
    )

    values_amplitude =\
        values_amplitude_1 +\
        values_amplitude_2 +\
        values_amplitude_3

    datavision.save_FFT_plot_matplotlib(
        values_amplitude = values_amplitude,
        time             = time,
        sample_rate      = sample_rate,
        filename         = "FFT.png"
    )

if __name__ == "__main__":
    main()

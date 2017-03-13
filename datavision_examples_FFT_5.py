#!/usr/bin/env python
from __future__ import division

import numpy

import datavision
import shijian

def main():

    time        = 1
    sample_rate = 300

    values_amplitude, values_time = datavision.generate_composite_sine_values(
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

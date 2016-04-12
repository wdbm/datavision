#!/usr/bin/env python
from __future__ import division

import numpy

import datavision

def main():

    signal_frequency  = 5
    sample_rate       = 150
    sampling_interval = 1 / sample_rate
    values_time       = numpy.arange(0, 1, sampling_interval)
    values_amplitude  = numpy.sin(2 * numpy.pi * signal_frequency * values_time)

    datavision.save_FFT_plot_matplotlib(
        values      = values_amplitude,
        sample_rate = sample_rate,
        filename    = "FFT.png"
    )

if __name__ == "__main__":
    main()

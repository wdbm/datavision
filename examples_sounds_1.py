#!/usr/bin/env python
from __future__ import division

import time

import datavision
import numpy

def main():

    message = "hello world i hope you are happy"

    print("message: {message}".format(
        message = message
    ))

    datavision.play_message_sounds(
        message   = message,
        save_plot = True
    )

    time.sleep(5)

    message = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    print("message: {message}".format(
        message = message
    ))

    datavision.play_message_sounds(
        message   = message
    )

    message = numpy.random.random((1, 15, 3)) * 255

    print("message:\{message}".format(
        message = message
    ))
    message = str(message).replace("\n", "")
    print "".join(str(element) for element in set(message))

    datavision.play_message_sounds(
        message = message,
        symbols = "".join(str(element) for element in set(message)),
        gaussian_filter = False
    )

if __name__ == "__main__":
    main()

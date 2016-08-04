#!/usr/bin/env python
from __future__ import division

import time

import datavision

def main():

    message = "hello world i hope you are happy"

    print("message: {message}".format(
        message = message
    ))

    datavision.play_message_sounds(
        message   = message,
        save_plot = True,
        directory = "plots"
    )

    time.sleep(5)

    message = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    print("message: {message}".format(
        message = message
    ))

    datavision.play_message_sounds(
        message   = message,
        directory = "plots"
    )

if __name__ == "__main__":
    main()

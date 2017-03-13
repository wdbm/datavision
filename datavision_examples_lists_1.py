#!/usr/bin/env python

import datavision

def main():

    for list_configuration in datavision.list_element_combinations_variadic(
        [[10, 20], [30, 40], [50, 60]]
    ):
        print(list_configuration)

if __name__ == "__main__":
    main()

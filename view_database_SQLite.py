#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# view_database_SQLite.py                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a database inspection program.                               #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
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

Usage:
    program [options]

Options:
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
    --database=FILE          database [default: database.db]
    --rows=NUMBER            limit on number of table rows displayed
"""

from __future__ import division

name    = "view_database_SQLite.py"
version = "2017-02-03T1617Z"
logo    = None

import datetime
import docopt
import inspect
import logging
import os
import subprocess
import sys
import time

import dataset
import propyte
import pyprel

def main(options):

    global program
    program = propyte.Program(
        options = options,
        name    = name,
        version = version,
        logo    = logo
        )
    global log
    from propyte import log

    filename_database   = options["--database"]
    rows_limit          = options["--rows"]
    if rows_limit is not None:
        rows_limit = int(rows_limit)

    log.info("\naccess database {filename}".format(
        filename = filename_database
    ))
    database = dataset.connect(
        "sqlite:///{filename_database}".format(
            filename_database = filename_database
        )
    )

    for name_table in database.tables:

        log.info("access table \"{name_table}\"".format(
            name_table = name_table
        ))
        table = database[name_table]
        log.info(
            "number of rows in table \"{name_table}\": {number_of_rows}".format(
                name_table     = name_table,
                number_of_rows = str(len(table))
            )
        )
        log.info("\ntable {name_table} printout:\n".format(
            name_table = name_table
        ))

        print(
            pyprel.Table(
                contents = pyprel.table_dataset_database_table(
                    table      = database[name_table],
                    rows_limit = rows_limit
                )
            )
        )

    program.terminate()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

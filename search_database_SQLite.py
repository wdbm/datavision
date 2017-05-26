#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# search_database_SQLite                                                       #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program searches a database's tables' entries for specified text.       #
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

usage:
    program [options]

options:
    -h, --help         display help message
    --version          display version and exit

    --databasein=FILE  database [default: database.db]
    --searchtext=TEXT  database [default: Bitcoin]
"""

from __future__ import division
import docopt

import dataset
import propyte
import pyprel
import shijian

name    = "search_database_SQLite"
version = "2017-05-26T1714Z"
logo    = None

def access_database(
    filename = "database.db"
    ):
    print("access database {filename}".format(
        filename = filename
    ))
    database = dataset.connect("sqlite:///" + str(filename))
    return database

def main(options):

    filename_database_in  = options["--databasein"]
    search_text           = options["--searchtext"]

    database_in = access_database(filename = filename_database_in)

    for name_table in database_in.tables:
        print("\naccess table {table}".format(
            table = name_table
        ))
        table = database_in[name_table]

        entries_in = [entry for entry in table.all()]

        print("\nsearch entries")

        for entry in entries_in:
            for key in entry:
                if search_text in str(key) or search_text in str(entry[key]):
                    print("\nmatch found -- table {table} entry {ID}".format(
                        table = name_table,
                        ID    = entry["id"]
                    ))
                    pyprel.print_dictionary(dictionary = entry)

    print("search complete")

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

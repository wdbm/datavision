#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# change_field_name_database_SQLite                                            #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program changes the field name of all tables of a database and saves a  #
# a new database with the changes.                                             #
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
    -h, --help          display help message
    --version           display version and exit

    --databasein=FILE   database           [default: database.db]
    --databaseout=FILE  database           [default: database_1.db]
    --fieldin=TEXT      field to change
    --fieldout=TEXT     field to change to
"""

from __future__ import division

import docopt
import collections

import dataset
import propyte
import shijian

name    = "change_field_name_database_SQLite"
version = "2017-04-19T1319Z"
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
    filename_database_out = options["--databaseout"]
    field_in              = options["--fieldin"]
    field_out             = options["--fieldout"]

    print("\nchange field \"{field_in}\" to field \"{field_out}\"\n".format(
        field_in  = field_in,
        field_out = field_out
    ))

    database_in = access_database(filename = filename_database_in)

    print("tables in database: {tables}".format(
        tables = ", ".join(database_in.tables)
    ))

    for name_table in database_in.tables:
        print("\naccess table {table}".format(
            table = name_table
        ))
        table = database_in[name_table]
        print("table {table} fields: {fields}".format(
            table  = name_table,
            fields = ", ".join(table.columns)
        ))
        print("table {table} number of rows: {number_rows}".format(
            table       = name_table,
            number_rows = str(len(table))
        ))

        print("load input entries")
        entries_in = [entry for entry in table.all()]

        for entry in entries_in:
            del(entry["id"])

        entries_out = []
        for index, entry_in in enumerate(entries_in):
            entries_out.append(collections.OrderedDict(
                (field_out if key == field_in else key, value) for key, value in entry_in.viewitems()
            ))

        print("save entries with field changed to database {filename}".format(
            filename = filename_database_out
        ))
        database_out = access_database(filename = filename_database_out)
        
        table = database_out[name_table]
        
        progress_extent = len(entries_out)
        progress = shijian.Progress()
        progress.engage_quick_calculation_mode()
        
        for index, entry in enumerate(entries_out):
            table.insert(entry)
            print(progress.add_datum(fraction = (index + 1) / progress_extent))

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

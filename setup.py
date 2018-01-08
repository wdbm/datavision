#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "datavision",
        version          = "2018.01.08.2333",
        description      = "Python data visualisation",
        long_description = long_description(),
        url              = "https://github.com/wdbm/datavision",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "datavision"
                           ],
        install_requires = [
                           "pandas",
                           "python-dateutil",
                           "dataset",
                           "matplotlib",
                           "numpy",
                           "Pillow",
                           "pygame",
                           "pyprel",
                           "scipy",
                           "shijian"
                           ],
        scripts          = [
                           "change_field_name_database_SQLite.py",
                           "datavision_TTY_plot.py",
                           "duplicates_database_SQLite.py",
                           "search_database_SQLite.py",
                           "view_database_SQLite.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           datavision = datavision:datavision
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()

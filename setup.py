#!/usr/bin/env python
##
## Name:     setup.py
## Purpose:  Install KMeans library.
## Author:   M. J. Fromberger (@creachadair)
##
## Standard usage:  python setup.py install
##
from distutils.core import setup

setup(name='KMeans',
      version="1.0",
      description='K-Means Clustering Algorithm Implementation',
      author='M. J. Fromberger',
      py_modules=["KMeans"])

# Here there be dragons

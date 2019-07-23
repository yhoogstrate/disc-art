#!/usr/bin/env python
# *- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 textwidth=79:

import discart
from setuptools import setup

def get_requirements():
    with open('requirements.txt', 'r') as fh:
        content = fh.read().strip().split()
    return content


setup(name="disc-art",
      scripts=['bin/disc-art'],
      packages=["discart"],
      test_suite="tests",
      tests_require=['nose2', 'pytest', 'pytest-cov'],
      setup_requires=[],# scipy, numpy
      install_requires=[get_requirements()],
      version=discart.__version__,
      description="-",
      author=discart.__author__,
      url=discart.__homepage__,
      keywords=["rna-seq", "ribo-minus", "random-hexamer"],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ])

#!/usr/bin/env python

from distutils.core import setup

setup(name='erwin',
      version='0.0',
      description='Erwin Antichess Engine',
      author='Damodar Dahal',
      author_email='damodar.dahal@amazon.com',
      package_dir={'': 'packages'},
      entry_points={
          "console_scripts": [
              "erwin = solver.cli:cli"
          ]
      }
      )

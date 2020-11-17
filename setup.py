#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 17-11-2020 11:16:50

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

from setuptools import setup, find_packages

setup(name='connect4',
      version='0.0.1',
      description='',
      url='https://github.com/BenedictWilkinsAI/connect4',
      author='Benedict Wilkins',
      author_email='brjw@hotmail.co.uk',
      license='GNU3',
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
      ],
      install_requires=['gym', 'numpy'],
      include_package_data=True,
      packages=find_packages())

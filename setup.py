#!/usr/bin/python
""" setup for mdtf_test_data """
from setuptools import setup, find_packages
import os


is_travis = "TRAVIS" in os.environ

setup(
    name="mdtf_test_data",
    version="1.0.0",
    author="John Krasting",
    author_email="John.Krasting@noaa.gov",
    description=("Tools for working with MDTF Diagnostics test data sets"),
    license="LGPLv3",
    keywords="",
    url="https://github.com/jkrasting/mdtf_test_data",
    packages=find_packages()
)

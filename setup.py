""" setup for mdtf_test_data """
from setuptools import setup, find_packages
import os


is_travis = "TRAVIS" in os.environ

setup(
    name="mdtf_test_data",
    version="0.0.1",
    author="John Krasting",
    author_email="John.Krasting@noaa.gov",
    description=("Tools for working with MDTF Diagnostics test data sets"),
    license="LGPLv3",
    keywords="",
    url="https://github.com/jkrasting/mdtf_test_data",
    packages=find_packages(),
    scripts=["scripts/mdtf-coarsen.py", "scripts/ncar_synthetic.py"],
)

""" setup for mdtf_data_decimator """
from setuptools import setup, find_packages
import os


is_travis = "TRAVIS" in os.environ

setup(
    name="mdtf_data_decimator",
    version="0.0.1",
    author="John Krasting",
    author_email="John.Krasting@noaa.gov",
    description=("A tool to coarsen inout data for MDTF Diagnostics"),
    license="LGPLv3",
    keywords="",
    url="https://github.com/jkrasting/mdtf_data_decimator",
    packages=find_packages(),
    scripts=["scripts/mdtf-coarsen.py","scripts/ncar_synthetic.py"],
)

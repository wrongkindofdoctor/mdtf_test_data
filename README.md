[![Total alerts](https://img.shields.io/lgtm/alerts/g/jkrasting/mdtf_data_decimator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_data_decimator/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jkrasting/mdtf_data_decimator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_data_decimator/context:python)

# MDTF Diagnostics Coarse Resolution Test Data
Package to coarsen input data for MDTF Diagnostics

## Overview
This package is designed to coarsen NetCDF files for generating test datasets that can be used with the MDTF Diagnostics package.  

## Requirements
* xarray
* xESMF
* numpy
* cftime

## Getting the code
```
git clone https://github.com/jkrasting/mdtf_data_decimator.git
```

## Installation
```
cd mdtf_data_decimator
pip install .
```

## Usage
```
mdtf-coarsen.py 
usage: mdtf-coarsen.py [-h] [-r REGRID_METHOD] [-o OUTFILE] [-O] infile

Coarsen a NetCDF file.

positional arguments:
  infile                Path to input NetCDF file

optional arguments:
  -h, --help            show this help message and exit
  -r REGRID_METHOD      xESMF regridding method
  -o OUTFILE, --outfile OUTFILE
                        Filename of output NetCDF file
  -O                    Overwrite existing file
```
Notes: 
* The tool only supports standard grids with dimensions name `lat` and `lon` for now
* Any xESMF regrid method may be passed with the `-r` option

## Getting Help
Submit a [GitHub Issue](https://github.com/jkrasting/mdtf_data_decimator/issues)

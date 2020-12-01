[![Total alerts](https://img.shields.io/lgtm/alerts/g/jkrasting/mdtf_test_data.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_test_data/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jkrasting/mdtf_test_data.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jkrasting/mdtf_test_data/context:python)

# MDTF Diagnostics Test Data Tools
Package to work with test input datasets for MDTF Diagnostics

## Overview
This package is designed to coarsen NetCDF files for generating test datasets and produce synthetic datasets on-the-fly that can be used for testing the MDTF Diagnostics package.  

## Requirements
* xarray
* xESMF
* numpy
* cftime

## Getting the code
```
git clone https://github.com/jkrasting/mdtf_test_data.git
```

## Installation
```
cd mdtf_test_data
pip install .
```

## Usage
This package can be used to generate fully-synthetic datasets based on NCAR's 
CESM2 and GFDL's CM4 model output that can be used to test the MDTF Diagnostics package.

To generate NCAR CESM output in a directory called `NCAR.Synthetic`:
```
./ncar_synthetic.py
```

To generate GFDL CM4 output in a directory called `GFDL.Synthetic`:
```
./gfdl_synthetic.py
```

To coarsen an existing NetCDF file:
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
* The coarsening tool only supports standard grids with dimensions name `lat` and `lon` for now
* Any xESMF regrid method may be passed with the `-r` option

## Getting Help
Submit a [GitHub Issue](https://github.com/jkrasting/mdtf_test_data/issues)

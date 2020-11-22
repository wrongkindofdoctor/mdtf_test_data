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
```
Notes: 
* The tool only supports standard grids with dimensions name `lat` and `lon` for now
* Any xESMF regrid method may be passed with the `-r` option

## Getting Help
Submit a [GitHub Issue](https://github.com/jkrasting/mdtf_data_decimator/issues)

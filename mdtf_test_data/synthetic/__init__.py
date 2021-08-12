""" Init file for generating synthetic datasets """

from .synthetic_data import (
    dataset_stats,
    generate_synthetic_dataset,
    gfdl_vertical_coord,
    gfdl_plev19_vertical_coord,
    ncar_hybrid_coord,
    write_to_netcdf,
)

from . import time

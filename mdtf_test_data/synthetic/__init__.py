""" Module for generating synthetic datasets """

from .synthetic import (
    dataset_stats,
    generate_daily_time_axis,
    generate_hourly_time_axis,
    generate_monthly_time_axis,
    generate_ncar_dataset,
    generate_random_array,
    ncar_hybrid_coord,
    write_to_netcdf,
)

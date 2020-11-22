""" Collection of tools to coarsen model data """

__all__ = ["regrid_lat_lon_dataset"]

import numpy as np
import xarray as xr
import xesmf as xe


def regrid_lat_lon_dataset(dset, method="bilinear"):
    """Regrids xarray dataset to a standard 15x15 degree grid

    Parameters
    ----------
    dset : xarray.Dataset
        Input dataset.  Must have horizonatal dimensions of "lat" and "lon"
    method : str, optional
        xESMF regridding option, by default "bilinear"

    Returns
    -------
    xarray.Dataset
        Regridded data set
    """

    # Define output grid. Currently fixed at 15x15 but could be generalized
    dset_out = xr.Dataset(
        {
            "lat": (["lat"], np.arange(-82.5, 95.0, 15.0)),
            "lon": (["lon"], np.arange(7.5, 365.0, 15.0)),
        }
    )

    # Create xESMF regridder object
    regridder = xe.Regridder(dset, dset_out, method)

    # Loop over variables
    for var in list(dset.variables):
        _dim = list(dset[var].dims)
        if "lat" in _dim and "lon" in _dim:
            _regridded = regridder(dset[var])
            dset_out[var] = _regridded.astype(dset[var].dtype)
            dset_out[var].attrs = dset[var].attrs
        elif var not in ["lat", "lon"]:
            dset_out[var] = dset[var]

    # Copy coordinate metadata
    dset_out["lat"].attrs = dset["lat"].attrs
    dset_out["lon"].attrs = dset["lon"].attrs

    # Copy dataset metadata
    dset_out.attrs = dset.attrs
    dset_out.attrs["coarsen_method"] = f"xESMF {method}"

    return dset_out

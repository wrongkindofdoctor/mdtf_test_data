""" Collection of tools to coarsen model data """

__all__ = ["construct_tripolar_grid"]

import warnings

import numpy as np
import xarray as xr
import pkg_resources as pkgr

try:
    import xesmf as xe
except:
    warnings.warn("Unable to load `xesmf`. Regridding functionality will not work.")


def construct_tripolar_grid(
    point_type="t", add_attrs=False, attr_fmt="gfdl", retain_coords=False
):
    """Generate a tripolar grid based on a real 5-degree MOM6 configuration

    Parameters
    ----------
    point_type : str, optional
        Grid type. Options are t, u, v, c. By default "t" (tracer)
    add_attrs : bool, optional
        Include lat and lon variable attributes, by default False
    attr_fmt : str, optional
        Modeling center attribute format, by default "gfdl"
    retain_coords : bool, optional
        Keep geolon, geolat, and wet in the dataset, by default False

    Returns
    -------
    xarray.Dataset
        Shell dataset with masked variable and ocean depth field
    """

    ds_in = pkgr.resource_filename("mdtf_test_data", "resources/ocean_static_5deg.nc")
    ds_in = xr.open_dataset(ds_in)

    if point_type == "t":
        lat = ds_in["geolat"]
        lon = ds_in["geolon"]
        wet = ds_in["wet"]
    elif point_type == "u":
        lat = ds_in["geolat_u"]
        lon = ds_in["geolon_u"]
        wet = ds_in["wet_u"]
    elif point_type == "v":
        lat = ds_in["geolat_v"]
        lon = ds_in["geolon_v"]
        wet = ds_in["wet_v"]
    elif point_type == "c":
        lat = ds_in["geolat_c"]
        lon = ds_in["geolon_c"]
        wet = ds_in["wet_c"]

    dset = xr.Dataset()
    dset["mask"] = xr.where(wet == 0.0, np.nan, 1.0)

    if point_type == "t":
        dset["depth"] = xr.DataArray(ds_in["depth_ocean"])

    if retain_coords is True:
        dset[lat.name] = lat
        dset[lon.name] = lat
        dset[wet.name] = wet

        if add_attrs is True:
            if attr_fmt == "gfdl":
                dset[lat.name].attrs = {}
                dset[lon.name].attrs = {}
                dset[wet.name].attrs = {}
            elif attr_fmt == "ncar":
                dset[lat.name].attrs = {}
                dset[lon.name].attrs = {}
                dset[wet.name].attrs = {}
            else:
                raise ValueError("Unknown attribute format")

        else:
            dset[lat.name].attrs = {}
            dset[lon.name].attrs = {}
            dset[wet.name].attrs = {}

    return dset

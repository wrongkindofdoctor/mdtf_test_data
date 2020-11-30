""" Module for generating synthetic datasets """

___all__ = [
    "dataset_stats",
    "generate_daily_time_axis",
    "generate_hourly_time_axis",
    "generate_monthly_time_axis",
    "generate_ncar_dataset",
    "generate_random_array",
    "ncar_hybrid_coord",
    "write_to_netcdf",
    "generate_monthly_time_axis",
]

import cftime
import xarray as xr
import numpy as np

from mdtf_test_data.coarsen import construct_rect_grid


def dataset_stats(filename, var=None):
    """Prints statistics and attributes for a NetCDF file

    Parameters
    ----------
    filename : str, path-like
        Path to NetCDF file to analyze
    var : str, optional
        Variable to analyze (None prints a list of variables), by default None
    """
    dset = xr.open_dataset(filename)
    if var is None:
        print(list(dset.variables))
    else:
        means = dset[var].mean(axis=(0, -2, -1)).values
        stds = dset[var].std(axis=(0, -2, -1)).values
        print(dset[var].attrs)
        print(means, stds)
    dset.close()


def generate_daily_time_axis(startyear, nyears, timefmt="ncar"):
    """Construct a daily noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    timefmt : str, optional
        Time axis format, either "gfdl" or "ncar", "ncar" by default

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """

    daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = list(np.arange(1, 13))
    days = [np.arange(1, daysinmonth[n] + 1) for n, x in enumerate(months)]
    days = [item for sublist in days for item in sublist]
    days = days * nyears
    months = [[months[n]] * daysinmonth[n] for n, x in enumerate(months)]
    months = [item for sublist in months for item in sublist]
    months = months * nyears
    years = list(np.arange(startyear, startyear + nyears))
    years = [[years[x]] * 365 for x in range(0, len(years))]
    years = [item for sublist in years for item in sublist]

    if timefmt == "gfdl":
        hours = [12] * len(days)
        time_attrs = {
            "long_name": "time",
            "cartesian_axis": "T",
            "calendar_type": "noleap",
            "bounds": "time_bnds",
        }
    else:
        hours = [0] * len(days)
        time_attrs = {"long_name": "time", "bounds": "time_bnds"}

    timetuple = list(zip(years, months, days, hours))
    times = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    time = xr.DataArray(
        times,
        dims={"time": times},
        coords={"time": (times)},
        attrs=time_attrs,
    )

    nbnds = np.array([0, 1])
    if timefmt == "gfdl":
        coords = (time, ("bnds", nbnds))
        bnds_attrs = {"long_name": "time axis boundaries"}
    else:
        coords = (time, ("nbnds", nbnds))
        bnds_attrs = {"long_name": "time interval endpoints"}

    timetuple = list(zip(years, months, days)) + [(startyear + nyears, 1, 1)]
    bounds = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    bounds = list(zip(bounds[0:-1], bounds[1::]))

    time_bnds = xr.DataArray(
        bounds,
        coords=coords,
        attrs=bnds_attrs,
    )

    return time, time_bnds


def generate_hourly_time_axis(startyear, nyears, dhour):
    """Construct an hourly noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    dhour : int
        Delta skip for hours (e.g. 1 hour, 3 hours, 6 hours)

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """

    nhours = int(24 / dhour)
    hours = list(np.arange(0, 24, dhour))
    hours = hours * 365 * nyears
    daysinmonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = list(np.arange(1, 13))
    days = [np.arange(1, daysinmonth[n] + 1) for n in range(0, len(months))]
    days = [item for sublist in days for item in sublist]
    days = [item for item in days for i in range(nhours)]
    days = days * nyears
    months = [[months[n]] * daysinmonth[n] for n, x in enumerate(months)]
    months = [item for sublist in months for item in sublist]
    months = [item for item in months for i in range(nhours)]
    months = months * nyears
    years = list(np.arange(startyear, startyear + nyears))
    years = [[years[x]] * 365 for x in range(0, len(years))]
    years = [item for sublist in years for item in sublist]
    years = [item for item in years for i in range(nhours)]
    timetuple = list(zip(years, months, days, hours))
    times = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    time = xr.DataArray(
        times,
        dims={"time": times},
        coords={"time": (times)},
        attrs={"long_name": "time", "bounds": "time_bnds"},
    )

    timetuple = (
        [(startyear, 1, 1, 0)]
        + list(zip(years, months, days, hours))
        + [(startyear + nyears, 1, 1, dhour)]
    )
    bounds = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    bounds = list(zip(bounds[0:-1], bounds[1::]))[0:-1]
    nbnds = np.array([0, 1])
    time_bnds = xr.DataArray(
        bounds,
        coords=(time, ("nbnds", nbnds)),
        attrs={"long_name": "time interval endpoints"},
    )

    return time, time_bnds


def generate_monthly_time_axis(startyear, nyears, dataformat="ncar"):
    """Construct a monthly noleap time dimension with associated bounds

    Parameters
    ----------
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis

    Returns
    -------
    xarray.DataArray
        time and time_bnds xarray DataArray types
    """

    nyears = (nyears + 1) if dataformat == "ncar" else nyears

    years = np.arange(startyear, startyear + nyears)
    years = [year for year in years for x in range(12)]
    months = list(np.arange(1, 13)) * nyears
    days = 1 if dataformat == "ncar" else 15
    days = [days] * len(months)
    timetuple = list(zip(years, months, days))
    times = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    times = times[1:-11] if dataformat == "ncar" else times
    time = xr.DataArray(
        times,
        dims={"time": times},
        coords={"time": (times)},
        attrs={"long_name": "time", "bounds": "time_bnds"},
    )

    days = [1] * len(months)
    timetuple = list(zip(years, months, days))
    bounds = [cftime.DatetimeNoLeap(*x, calendar="noleap") for x in timetuple]
    bounds = bounds + [cftime.DatetimeNoLeap(startyear + nyears, 1, 1)]
    bounds = list(zip(bounds[0:-1], bounds[1::]))
    bounds = bounds[0:-12] if dataformat == "ncar" else bounds
    nbnds = np.array([0, 1])
    time_bnds = xr.DataArray(
        bounds,
        coords=(time, ("nbnds", nbnds)),
        attrs={"long_name": "time interval endpoints"},
    )

    return time, time_bnds


def generate_ncar_dataset(
    stats, dlon, dlat, startyear, nyears, varname, timeres="mon", attrs=None
):
    """Generates xarray dataset of syntheic data in NCAR format

    Parameters
    ----------
    stats : tuple or list of tuples
        Array statistics in the format of [(mean,stddev)]
    dlon : float, optional
        Grid spacing in the x-dimension (longitude)
    dlat : float, optional
        Grid spacing in the y-dimension (latitude)
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    varname : str
        Variable name in output dataset
    attrs : dict, optional
        Variable attributes, by default None

    Returns
    -------
    xarray.Dataset
        Dataset of synthetic data
    """

    attrs = {} if attrs is None else attrs

    dset = construct_rect_grid(dlon, dlat, add_attrs=True)
    lat = dset.lat
    lon = dset.lon
    xyshape = (len(dset["lat"]), len(dset["lon"]))

    if timeres == "mon":
        time, time_bnds = generate_monthly_time_axis(startyear, nyears)
    elif timeres == "day":
        time, time_bnds = generate_daily_time_axis(startyear, nyears)
    elif timeres == "3hr":
        time, time_bnds = generate_hourly_time_axis(startyear, nyears, 3)
    elif timeres == "1hr":
        time, time_bnds = generate_hourly_time_axis(startyear, nyears, 1)
    else:
        print(timeres)
        raise ValueError("Unknown time resolution requested")

    dset["time"] = time
    dset["time_bnds"] = time_bnds

    dates = np.array([int(x.strftime("%Y%m%d")) for x in time.values])
    dset["date"] = xr.DataArray(
        dates, dims={"time": (time)}, attrs={"long_name": "current date (YYYYMMDD)"}
    )

    stats = [stats] if not isinstance(stats, list) else stats
    if len(stats) > 1:
        lev, hyam, hybm = ncar_hybrid_coord()
        dset["lev"] = lev
        dset["hyam"] = hyam
        dset["hybm"] = hybm

    data = generate_random_array(xyshape, len(time), stats)
    data = data.squeeze()

    if len(data.shape) == 4:
        assert data.shape[1] == len(
            dset["lev"]
        ), "Length of stats must match number of levels"
        dset[varname] = xr.DataArray(data, coords=(time, lev, lat, lon), attrs=attrs)
    else:
        dset[varname] = xr.DataArray(data, coords=(time, lat, lon), attrs=attrs)

    dset = dset.drop("nbnds")

    return dset


def generate_random_array(xyshape, ntimes, stats, dtype="float32"):
    """Generates an array of sample data chosen from a normal distribution

    Parameters
    ----------
    stats : tuple or list of tuples
        Array statistics in the format of [(mean,stddev)]
    xyshape : tuple
        Tuple of desired array shape

    Returns
    -------
    np.ndarray
        Array of random data
    """
    stats = [stats] if not isinstance(stats, list) else stats

    data = []
    for time in range(ntimes):
        np.random.seed(time)
        data.append(np.array([np.random.normal(x[0], x[1], xyshape) for x in stats]))

    return np.array(data).astype(dtype)


def ncar_hybrid_coord():
    """Generates NCAR CAM2 hybrid vertical coordinate

    Returns
    -------
    xarray.DataArray
        NCAR vertical hybrid coordinate, a, and b coefficients
    """

    lev = np.array(
        [
            2.501651,
            4.187496,
            6.66766,
            10.099201,
            14.551163,
            19.943806,
            26.002806,
            32.250471,
            38.050216,
            42.70557,
            46.240154,
            49.511782,
            53.014888,
            56.765857,
            60.782212,
            65.082732,
            69.687527,
            74.618127,
            79.897583,
            85.550576,
            91.603545,
            98.084766,
            105.024556,
            112.455371,
            120.411924,
            128.931421,
            138.053706,
            147.821421,
            158.280234,
            169.479033,
            181.470176,
            194.309746,
            208.057754,
            222.778457,
            238.540693,
            255.418164,
            273.489746,
            292.839941,
            313.559268,
            335.744541,
            359.499453,
            384.935117,
            412.17043,
            441.332715,
            472.55834,
            505.993262,
            541.793789,
            580.127324,
            621.173066,
            665.12291,
            712.182383,
            762.571445,
            816.525625,
            858.699883,
            886.368125,
            912.162773,
            935.873203,
            957.301758,
            976.266953,
            992.556094,
        ]
    )

    hyam = np.array(
        [
            2.501651e-03,
            4.187496e-03,
            6.667660e-03,
            1.009920e-02,
            1.455116e-02,
            1.994381e-02,
            2.600281e-02,
            3.225047e-02,
            3.805022e-02,
            4.270557e-02,
            4.624015e-02,
            4.951178e-02,
            5.301489e-02,
            5.676586e-02,
            6.078221e-02,
            6.508273e-02,
            6.968753e-02,
            7.461813e-02,
            7.989758e-02,
            8.555058e-02,
            9.160354e-02,
            9.808477e-02,
            1.050246e-01,
            1.124554e-01,
            1.204119e-01,
            1.289314e-01,
            1.380537e-01,
            1.478214e-01,
            1.582802e-01,
            1.694790e-01,
            1.746796e-01,
            1.726401e-01,
            1.696388e-01,
            1.664251e-01,
            1.629841e-01,
            1.592996e-01,
            1.553543e-01,
            1.511300e-01,
            1.466068e-01,
            1.417635e-01,
            1.365776e-01,
            1.310247e-01,
            1.250790e-01,
            1.187125e-01,
            1.118957e-01,
            1.045965e-01,
            9.678086e-02,
            8.841227e-02,
            7.945159e-02,
            6.985690e-02,
            5.958334e-02,
            4.858288e-02,
            3.680412e-02,
            2.759706e-02,
            2.155681e-02,
            1.592557e-02,
            1.074934e-02,
            6.071232e-03,
            1.930966e-03,
            -1.648308e-09,
        ]
    )

    hybm = np.array(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.006791,
            0.02167,
            0.038419,
            0.056353,
            0.075557,
            0.096119,
            0.118135,
            0.14171,
            0.166953,
            0.193981,
            0.222922,
            0.25391,
            0.287091,
            0.32262,
            0.360663,
            0.401397,
            0.445013,
            0.491715,
            0.541721,
            0.595266,
            0.652599,
            0.713989,
            0.779722,
            0.831103,
            0.864811,
            0.896237,
            0.925124,
            0.951231,
            0.974336,
            0.992556,
        ]
    )

    lev_attrs = {
        "long_name": "hybrid level at midpoints (1000*(A+B))",
        "units": "level",
        "positive": "down",
        "standard_name": "atmosphere_hybrid_sigma_pressure_coordinate",
        "formula_terms": "a: hyam b: hybm p0: P0 ps: PS",
    }

    lev = xr.DataArray(lev, dims={"lev": lev}, coords={"lev": (lev)}, attrs=lev_attrs)
    hyam = xr.DataArray(
        hyam,
        dims={"lev": lev},
        coords={"lev": (lev)},
        attrs={"long_name": "hybrid A coefficient at layer midpoints"},
    )
    hybm = xr.DataArray(
        hybm,
        dims={"lev": lev},
        coords={"lev": (lev)},
        attrs={"long_name": "hybrid B coefficient at layer midpoints"},
    )

    return lev, hyam, hybm


def write_to_netcdf(dset_out, outfile, time_dtype="float"):
    """Writes xarray dataset to NetCDF with proper encodings

    Parameters
    ----------
    dset_out : xarray.Dataset
        xarray dataset to write to NetCDF
    outfile : str, path-like
        Path to output file
    """
    encoding = {}
    for var in list(dset_out.variables):
        if var == "time":
            dset_out[var].encoding["units"] = "days since 1975-01-01"
            if time_dtype == "float":
                dset_out[var].encoding["dtype"] = "float64"
                dset_out[var].encoding["_FillValue"] = 1.0e20
            elif time_dtype == "int":
                dset_out[var].encoding["dtype"] = "i4"
        elif var == "time_bnds":
            dset_out[var].encoding["units"] = "days since 1975-01-01"
            if time_dtype == "float":
                dset_out[var].encoding["dtype"] = "float64"
                dset_out[var].encoding["_FillValue"] = 1.0e20
            elif time_dtype == "int":
                dset_out[var].encoding["dtype"] = "i4"
        elif var == "date":
            dset_out[var].encoding["dtype"] = "i4"
        elif "float" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = 1.0e20
        elif "int" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = -999
        else:
            dset_out[var].encoding["_FillValue"] = None
    dset_out.to_netcdf(outfile, encoding=encoding)

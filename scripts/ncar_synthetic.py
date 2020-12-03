#!/usr/bin/env python

""" Script to generate synthetic NCAR CESM2 output """

import os

import mdtf_test_data as td

DLON = 20
DLAT = 20
STARTYEAR = 1975
NYEARS = 7

CASENAME = "NCAR.Synthetic"

os.makedirs(f"{CASENAME}/mon")
os.makedirs(f"{CASENAME}/day")
os.makedirs(f"{CASENAME}/3hr")
os.makedirs(f"{CASENAME}/1hr")

# -- Create Monthly Data
print("Generating monthly data ...")

OUTFILE = "Z3"
attrs = {
    "mdims": 1,
    "units": "m",
    "long_name": "Geopotential Height (above sea level)",
    "cell_methods": "time: mean",
}
stats = [
    (39911.184, 1503.5703),
    (36339.867, 1318.1272),
    (33167.73, 1159.6759),
    (30402.71, 1024.01),
    (28014.025, 907.52545),
    (25977.67, 812.5992),
    (24280.934, 738.819),
    (22914.363, 684.1405),
    (21870.918, 646.11),
    (21145.533, 622.05505),
    (20650.492, 606.9762),
    (20228.424, 595.159),
    (19807.398, 584.4423),
    (19387.41, 574.9577),
    (18968.504, 566.8599),
    (18550.766, 560.364),
    (18134.246, 555.6607),
    (17718.803, 552.8208),
    (17304.172, 551.8367),
    (16890.176, 552.6706),
    (16476.494, 555.1753),
    (16062.766, 559.1083),
    (15648.681, 564.17194),
    (15233.889, 570.0084),
    (14818.047, 576.20264),
    (14400.834, 582.3102),
    (13981.972, 587.88904),
    (13561.267, 592.5198),
    (13138.605, 595.81165),
    (12713.972, 597.3992),
    (12294.373, 588.3031),
    (11880.293, 569.56024),
    (11464.33, 550.8575),
    (11045.44, 532.8474),
    (10623.187, 515.4224),
    (10196.957, 498.81952),
    (9766.008, 483.6007),
    (9329.627, 470.50427),
    (8887.224, 460.28516),
    (8438.355, 453.60825),
    (7982.7095, 450.97073),
    (7520.093, 452.66232),
    (7050.4, 458.75568),
    (6573.596, 469.11874),
    (6089.6963, 483.45206),
    (5598.735, 501.3424),
    (5100.8115, 522.31775),
    (4596.0874, 545.8952),
    (4084.7944, 571.5943),
    (3567.0034, 598.9684),
    (3042.794, 627.6345),
    (2512.47, 657.2358),
    (1976.4714, 687.46045),
    (1575.0771, 710.3252),
    (1322.4452, 724.7243),
    (1092.8248, 737.91113),
    (886.49493, 749.894),
    (703.75806, 760.6792),
    (544.9365, 770.3126),
    (410.32043, 777.56665),
]
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, NYEARS, OUTFILE, timeres="mon", attrs=attrs
)
td.synthetic.write_to_netcdf(
    ds_out, f"{CASENAME}/mon/{CASENAME}.{OUTFILE}.mon.nc", time_dtype="int"
)

OUTFILE = "PS"
attrs = {"units": "Pa", "long_name": "Surface pressure", "cell_methods": "time: mean"}
stats = [(96888.24, 8931.88)]
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, NYEARS, OUTFILE, timeres="mon", attrs=attrs
)
td.synthetic.write_to_netcdf(
    ds_out, f"{CASENAME}/mon/{CASENAME}.{OUTFILE}.mon.nc", time_dtype="int"
)


# -- Create Daily Data
print("Generating daily data ...")

DLON = 5
DLAT = 5

OUTFILE = "FLUT"
attrs = {
    "cell_methods": "time: mean",
    "long_name": "Upwelling longwave flux at top of model",
    "units": "W/m2",
    "Sampling_Sequence": "rad_lwsw",
}
stats = (224.86646, 48.011627)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "OMEGA500"
attrs = {
    "Sampling_Sequence": "rad_lwsw",
    "units": "Pa/s",
    "long_name": "Vertical velocity at 500 mbar pressure surface",
    "cell_methods": "time: mean",
}
stats = (-0.00053095096, 0.09604603)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "PRECT"
attrs = {
    "Sampling_Sequence": "rad_lwsw",
    "units": "m/s",
    "long_name": "Total (convective and large-scale) precipitation rate (liq + ice)",
    "cell_methods": "time: mean",
}
stats = (2.929617e-08, 5.7031237e-08)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "T250"
attrs = {
    "p": 250.0,
    "cell_methods": "time: mean",
    "long_name": "Temperature",
    "units": "K",
    "mdims": 1,
    "time": 0.0,
}
stats = (219.75917, 8.456115)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "U200"
attrs = {
    "Sampling_Sequence": "rad_lwsw",
    "units": "m/s",
    "long_name": "Zonal wind at 200 mbar pressure surface",
    "cell_methods": "time: mean",
}
stats = (13.888344, 17.738035)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "U250"
attrs = {
    "time": 0.0,
    "mdims": 1,
    "units": "m/s",
    "long_name": "Zonal wind",
    "cell_methods": "time: mean",
    "p": 250.0,
}
stats = (12.897135, 17.588223)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "U850"
attrs = {
    "Sampling_Sequence": "rad_lwsw",
    "units": "m/s",
    "long_name": "Zonal wind at 850 mbar pressure surface",
    "cell_methods": "time: mean",
}
stats = (1.4072706, 8.031601)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "V200"
attrs = {
    "units": "m/s",
    "long_name": "Meridional wind at 200 mbar pressure surface",
    "cell_methods": "time: mean",
}
stats = (-0.10729608, 11.274971)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "V850"
attrs = {
    "lon": 0.0,
    "lat": -90.0,
    "lev": 2.501650543212891,
    "time": 0.0,
    "mdims": 1,
    "units": "m/s",
    "long_name": "meridional wind at 850 hPa",
    "cell_methods": "time: mean",
}
stats = (0.06057823, 5.5419374)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

OUTFILE = "Z250"
attrs = {
    "p": 250.0,
    "cell_methods": "time: mean",
    "long_name": "Geopotential Height (above sea level)",
    "units": "m",
    "mdims": 1,
    "time": 0.0,
}
stats = (10259.143, 568.0995)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="day", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/day/{CASENAME}.{OUTFILE}.day.nc")

# -- Create 3-hourly Data
print("Generating 3-hourly data ...")

DLON = 20
DLAT = 20

OUTFILE = "PRECT"
attrs = {
    "units": "m/s",
    "long_name": "Total (convective and large-scale) precipitation rate (liq + ice)",
    "cell_methods": "time: mean",
}
stats = (2.6630838e-08, 6.908e-08)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="3hr", attrs=attrs
)
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/3hr/{CASENAME}.{OUTFILE}.3hr.nc")

# -- Create 1-hourly Data
print("Generating 1-hourly data ...")

NYEARS = 1
DLON = 20
DLAT = 20

OUTFILE = "PRECT"
attrs = {
    "units": "m/s",
    "long_name": "Total (convective and large-scale) precipitation rate (liq + ice)",
}
stats = (2.6785912e-08, 7.193412e-08)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="1hr", attrs=attrs
)
ds_out = ds_out.isel(time=slice(0, 2130))
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/1hr/{CASENAME}.{OUTFILE}.1hr.nc")

OUTFILE = "prw"
attrs = {
    "units": "kg/m2",
    "long_name": "Vertically integrated specific humidity (surface to 200 mb)",
}
stats = (18.124813, 15.1677885)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="1hr", attrs=attrs
)
ds_out = ds_out.isel(time=slice(0, 2130))
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/1hr/{CASENAME}.{OUTFILE}.1hr.nc")

OUTFILE = "qsat_int"
attrs = {
    "units": "kg/m2",
    "long_name": "Vertically integrated saturated specific humidity (surface to 200 mb)",
}
stats = (30.223436, 24.573318)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="1hr", attrs=attrs
)
ds_out = ds_out.isel(time=slice(0, 2130))
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/1hr/{CASENAME}.{OUTFILE}.1hr.nc")

OUTFILE = "tave"
attrs = {
    "units": "K",
    "long_name": "Vertically integrated temperature (surface to 200 mb)",
}
stats = (254.17484, 14.091375)
ds_out = td.synthetic.generate_synthetic_dataset(
    stats, DLON, DLAT, STARTYEAR, 7, OUTFILE, timeres="1hr", attrs=attrs
)
ds_out = ds_out.isel(time=slice(0, 2130))
td.synthetic.write_to_netcdf(ds_out, f"{CASENAME}/1hr/{CASENAME}.{OUTFILE}.1hr.nc")

import os
import pytest
import numpy as np
import pickle
import xarray as xr

from .synthetic_data import (
    xr_times_from_tuples,
    write_to_netcdf,
    ncar_hybrid_coord,
    generate_daily_time_axis,
    generate_hourly_time_axis,
    generate_monthly_time_axis,
    generate_random_array,
    generate_synthetic_dataset,
    gfdl_plev19_vertical_coord,
    gfdl_vertical_coord,
)


def pytest_namespace():
    return {
        "ds_gfdl": None,
        "ds_ncar": None,
        "ncar_hybrid": None,
        "gfdl_plev19": None,
        "gfdl_vert": None,
    }


@pytest.mark.parametrize("timefmt", ["gfdl", "ncar"])
def test_xr_times_from_tuples_ncar(timefmt):
    bounds = [(1, 1, 1), (2, 1, 1), (3, 1, 1)]
    times = [(1, 7, 15), (2, 7, 15)]
    result = xr_times_from_tuples(times, bounds, timefmt=timefmt)
    assert isinstance(result, xr.Dataset)
    assert "base_time_unit" in result.attrs.keys()
    if timefmt == "gfdl":
        assert sorted(list(result.variables)) == [
            "average_DT",
            "average_T1",
            "average_T2",
            "time",
            "time_bnds",
        ]
        assert sorted(list(result.dims)) == ["bnds", "time"]
        pytest.ds_gfdl = result
    elif timefmt == "ncar":
        assert sorted(list(result.variables)) == ["date", "time", "time_bnds"]
        assert sorted(list(result.dims)) == ["nbnds", "time"]
        pytest.ds_ncar = result
    else:
        assert False, f"Unknown format: {timefmt}"


def test_write_to_netcdf():
    outfile = ".pytest.dummy.out.nc"
    if os.path.exists(outfile):
        os.remove(outfile)
    write_to_netcdf(pytest.ds_gfdl, outfile)
    assert os.path.exists(outfile)
    if os.path.exists(outfile):
        os.remove(outfile)


def test_ncar_hybrid_coord():
    result = ncar_hybrid_coord()
    assert isinstance(result, xr.Dataset)
    assert np.allclose(float(result.lev.sum()), 18419.680589)
    assert np.allclose(float(result.hyam.sum()), 4.999968233351692)
    assert np.allclose(float(result.hybm.sum()), 13.419714)
    pytest.ncar_hybrid = result


def test_gfdl_plev19_vertical_coord():
    result = gfdl_plev19_vertical_coord()
    assert isinstance(result, xr.Dataset)
    assert np.allclose(float(result.plev19.sum()), 616100.0)
    pytest.gfdl_plev19 = result


def test_gfdl_vertical_coord():
    result = gfdl_vertical_coord()
    assert isinstance(result, xr.Dataset)
    assert np.allclose(float(result.pfull.sum()), 14932.053848)
    assert np.allclose(float(result.phalf.sum()), 15444.908725)
    pytest.gfdl_vert = result


def test_generate_random_array():
    result = generate_random_array((20, 20), 5, [(5.0, 10.0), (50.0, 100.0)])
    assert result.shape == (5, 2, 20, 20)
    assert np.allclose(result.sum(), 104847.61)
    assert np.allclose(
        (result[:, 0, :, :].mean(), result[:, 0, :, :].std()), (5.2270184, 10.07385)
    )
    assert np.allclose(
        (result[:, 1, :, :].mean(), result[:, 1, :, :].std()), (47.196785, 98.86136)
    )


def test_generate_daily_time_axis():
    result = generate_daily_time_axis(1850, 2)
    assert isinstance(result, xr.Dataset)
    assert len(result.time) == 730
    assert int(result.time[1] - result.time[0]) == 86400000000000


@pytest.mark.parametrize(
    "dhour,length,dt", [(3, 2920, 10800000000000), (4, 2190, 14400000000000)]
)
def test_generate_hourly_time_axis(dhour, length, dt):
    result = generate_hourly_time_axis(1971, 1, dhour)
    assert isinstance(result, xr.Dataset)
    assert len(result.time) == length
    assert int(result.time[1] - result.time[0]) == dt


def test_generate_monthly_time_axis():
    result = generate_monthly_time_axis(1931, 5)
    assert isinstance(result, xr.Dataset)
    assert len(result.time) == 60
    assert int(result.time[1] - result.time[0]) == 2419200000000000


def test_generate_synthetic_dataset():
    # not sure this is fully portable below
    stats = [(10.0, 1.0) for x in range(0, 19)]
    result = generate_synthetic_dataset(
        stats,
        180,
        90,
        1860,
        2,
        "dummy",
        attrs={"test_attribute": "some_value"},
        fmt="gfdl",
    )
    print(result)
    if not os.path.exists("ref_synth_dset.pkl"):
        pickle.dump(result, open("ref_synth_dset.pkl", "wb"))
    else:
        reference = pickle.load(open("ref_synth_dset.pkl", "rb"))
        assert result.equals(reference)

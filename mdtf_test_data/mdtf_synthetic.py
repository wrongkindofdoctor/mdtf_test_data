#!/usr/bin/env python
""" mdtf_test_data driver program """
import argparse
from util.cli import cli_holder
from synthetic.synthetic_setup import synthetic_main
import sys
import os
from envyaml import EnvYAML

def read_yaml(file_name):
    """ A function to read YAML files """
    config = EnvYAML(file_name)
    return config

def main():
    """The the central nervous system of the mdtf_test_data package"""
    print("Starting mdtf_test_data")
    # default behavior is to run script from mdtf_test_data directory
    cur_dir = os.getcwd()
    assert(os.path.basename(cur_dir) == "mdtf_test_data"), "Error: Current directory is not mdtf_test_data"
    # Define the the CLI arguments and call the parser.
    parser = argparse.ArgumentParser(description="parse mdtf_test_data command-line arguments")
    # @TODO add support for CMIP convention
    parser.add_argument("--convention","-c", type=str, help="Model convention", choices=['GFDL', 'CESM', 'NCAR'],
                    required=True, default="")
    parser.add_argument("--startyear", type=int, help="Start year of time period",
                    required=False, default=1)
    parser.add_argument("--nyears", type=int, help="Total length of time period in years",
                    required=False, default=10)
    parser.add_argument("--dlat", type=float, help="Latitude resolution in degrees",
                    required=False, default=20.0)
    parser.add_argument("--dlon", type=float, help="Longitude resolution in degrees",
                    required=False, default=20.0)
    args = parser.parse_args()
    cli_info = cli_holder(args.convention, args.startyear,
                          args.nyears, args.dlat, args.dlon)

    assert cli_info.dlat <= 30.0 and cli_info.dlat >= 0.5, "Error: dlat value is invalid; valid range is [0.5 30.0]"
    assert cli_info.dlon <= 60.0 and cli_info.dlon >= 0.5, "Error: dlon value is invalid; valid range is [0.5 60.0]"
    if cli_info.convention == 'GFDL':
        print("Importing GFDL variable information")
        input_data = read_yaml("config/gfdl_day.yml")

        print("Calling Synthetic Data Generator for GFDL data")
        synthetic_main(input_data, DLAT=cli_info.dlat, DLON=cli_info.dlon,
                         STARTYEAR=cli_info.startyear, NYEARS=cli_info.nyears,
                         CASENAME="GFDL.Synthetic", TIME_RES="day", DATA_FORMAT="gfdl")
    elif cli_info.convention == 'CESM' or cli_info.convention == 'NCAR':
        print("Importing NCAR variable information")
        time_res = ["mon","day","3hr","1hr"]
        for t in time_res:
            input_data = read_yaml("config/ncar_" + t + ".yml")
            dlat = 20.0
            dlon = 20.0
            if t == "day":
                dlat=5.0
                dlon=5.0
            print("Calling Synthetic Data Generator for NCAR data")
            synthetic_main(input_data, DLAT=dlat, DLON=dlon,
                        STARTYEAR=cli_info.startyear, NYEARS=cli_info.nyears,
                        CASENAME="NCAR.Synthetic", TIME_RES=t, DATA_FORMAT="ncar")

if __name__ == '__main__':
    main()
    sys.exit()
""" Script to generate synthetic GFDL CM4 output """

import os

import mdtf_test_data as td

DLON = 20
DLAT = 20
STARTYEAR = 1
NYEARS = 10

CASENAME = "GFDL.Synthetic"

# os.makedirs(f"{CASENAME}/mon")
os.makedirs(f"{CASENAME}/day")
# os.makedirs(f"{CASENAME}/3hr")
# os.makedirs(f"{CASENAME}/1hr")

# -- Create Daily Data
print("Generating daily data ...")

outfile = "precip"
stats = (2.9479988e-05, 6.57948e-05)
attrs = {
    "long_name": "Total precipitation rate",
    "units": "kg/m2/s",
    "cell_methods": "time: mean",
    "time_avg_info": "average_T1,average_T2,average_DT",
    "interp_method": "conserve_order1",
}
dset_out = td.synthetic.generate_synthetic_dataset(
    stats, 20, 20, 1, 10, outfile, timeres="day", attrs=attrs, fmt="gfdl"
)
td.synthetic.write_to_netcdf(dset_out, f"{CASENAME}/day/{CASENAME}.{outfile}.day.nc")

outfile = "sphum"
attrs = {
    "long_name": "specific humidity",
    "units": "kg/kg",
    "cell_methods": "time: mean",
    "time_avg_info": "average_T1,average_T2,average_DT",
    "interp_method": "conserve_order2",
}
stats = [
    (2.207744273619028e-06, 3.1171239811556006e-08),
    (2.2120004814496497e-06, 4.2038056591309214e-08),
    (2.2173462639329955e-06, 6.085841164349404e-08),
    (2.195089336964884e-06, 1.2779378266714048e-07),
    (2.153154582629213e-06, 2.374897718482316e-07),
    (2.094266392305144e-06, 2.854812350960856e-07),
    (2.0205031887599034e-06, 2.8833915166615043e-07),
    (1.9574151792767225e-06, 3.129641470422939e-07),
    (1.9869351035595173e-06, 4.490039202664775e-07),
    (2.3005297862255247e-06, 7.08150935224694e-07),
    (3.968285909650149e-06, 2.2641079340246506e-06),
    (1.0366683454776648e-05, 9.786092959984671e-06),
    (3.099906462011859e-05, 3.574563379515894e-05),
    (8.375193283427507e-05, 0.00010662762360880151),
    (0.00018633835134096444, 0.0002450024476274848),
    (0.00037473972770385444, 0.0004942434024997056),
    (0.000682022946421057, 0.0008718980243429542),
    (0.0011107738828286529, 0.0013433881103992462),
    (0.0016250668559223413, 0.0018277750350534916),
    (0.0021864811424165964, 0.002303780522197485),
    (0.002785360673442483, 0.002752475207671523),
    (0.0034250598400831223, 0.003191043622791767),
    (0.004096926189959049, 0.003610411658883095),
    (0.0047650025226175785, 0.004022716544568539),
    (0.005404375027865171, 0.004434366710484028),
    (0.005979245062917471, 0.004850724712014198),
    (0.006488976068794727, 0.0052804104052484035),
    (0.0068984683603048325, 0.0056708799675107),
    (0.007145351730287075, 0.005889154504984617),
    (0.0072888461872935295, 0.005995234474539757),
    (0.007391186896711588, 0.006065600086003542),
    (0.007494122255593538, 0.006137644872069359),
]
dset_out = td.synthetic.generate_synthetic_dataset(
    stats, 20, 20, 1, 10, outfile, timeres="day", attrs=attrs, fmt="gfdl"
)
td.synthetic.write_to_netcdf(dset_out, f"{CASENAME}/day/{CASENAME}.{outfile}.day.nc")

outfile = "WVP"
attrs = {
    "long_name": "Column integrated water vapor",
    "units": "kg/m2",
    "cell_methods": "time: mean",
    "time_avg_info": "average_T1,average_T2,average_DT",
    "interp_method": "conserve_order1",
}
stats = (19.95419692993164, 17.587417602539062)
dset_out = td.synthetic.generate_synthetic_dataset(
    stats, 20, 20, 1, 10, outfile, timeres="day", attrs=attrs, fmt="gfdl"
)
td.synthetic.write_to_netcdf(dset_out, f"{CASENAME}/day/{CASENAME}.{outfile}.day.nc")

#!/usr/bin/env python3

import sys
import re
import glob

import pandas as pd

import hypsometry_utils as hu

topdir = '/projects/CHARIS/derived_hypsometries/MODSCAG_GF_v09_fromFile_rainv01_less_ET/IN_Hunza_at_DainyorBridge/'

source_types = ['exposed_glacier_ice', 'snow_on_ice', 'snow_on_land']
srctype_re = '|'.join(source_types)

egi_by_year = {}
sol_by_year = {}
soi_by_year = {}
#for year in range(2001, 2014 + 1):
for year in range(2001, 2001 + 1):
    name_patt = "*.{year}.*_melt_by_elev.best_Hunza_model.txt".format(year=year)
    filelist = glob.glob(topdir + name_patt)

    print("Processing year {year} ...".format(year=year))
    for fn in filelist:
        type_ = re.search(srctype_re, fn).group(0)
        hyps = hu.Hypsometry(filename=fn)
        #hyps.print()
        elev_sum = hyps.sum_by_elevband()
        sums_by_year[year] = elev_sum
        print("    **** {} ****".format(type_), fn)
        print("    ", elev_sum)

# Example set of files:
# 
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.exposed_glacier_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.snow_on_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.snow_on_land_melt_by_elev.best_Hunza_model.txt

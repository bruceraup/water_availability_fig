#!/usr/bin/env python3

import sys
import re
import glob

import pandas as pd

import hypsometry_utils as hu


def melt_by_elev(year, typ):
    """
    Calculate a table of melt contribution by elevation band, given a year and
    a source type.
    """
    name_patt = "*.{year}.*{typ}_melt_by_elev.best_Hunza_model.txt".format(year=year, typ=typ)
    filelist = glob.glob(topdir + name_patt)
    if len(filelist) > 1:
        print("WARNING: more than one file matching: ", name_patt)
        print("Using first one")
    fn = filelist[0]
    hyps = hu.Hypsometry(filename=fn)
    elev_sum = hyps.sum_by_elevband()
    return elev_sum


topdir = '/projects/CHARIS/derived_hypsometries/MODSCAG_GF_v09_fromFile_rainv01_less_ET/IN_Hunza_at_DainyorBridge/'

source_types = ['exposed_glacier_ice', 'snow_on_ice', 'snow_on_land']

for typ in source_types:
    year_range = range(2001, 2014 + 1)
    year_range = range(2001, 2001 + 1)
    for year in year_range:
        melt = melt_by_elev(year, typ)
        print("{}, {}".format(typ, year))
        print(melt)


# Example set of files:
# 
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.exposed_glacier_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.snow_on_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.snow_on_land_melt_by_elev.best_Hunza_model.txt

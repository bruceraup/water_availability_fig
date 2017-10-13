#!/usr/bin/env python3

import sys
import re
import glob
import os

import pandas as pd

import hypsometry_utils as hu


def melt_by_elev(topdir, year, typ):
    """
    Calculate a table of melt contribution by elevation band, given a year and
    a source type.
    """
    name_patt = "*.{year}.*{typ}_melt_by_elev.best_Hunza_model.txt".format(year=year, typ=typ)
    filelist = glob.glob(os.path.join(topdir, name_patt))
    if len(filelist) > 1:
        print("WARNING: more than one file matching: ", name_patt)
        print("Using first one")
    fn = filelist[0]
    hyps = hu.Hypsometry(filename=fn)
    elev_sum = hyps.sum_by_elevband()
    return elev_sum


def do_one_basin(topdir):
    source_types = ['exposed_glacier_ice', 'snow_on_ice', 'snow_on_land']

    contribs_all = None
    startyear = 2001
    endyear = 2014

    for typ in source_types:
        year_range = range(startyear, endyear + 1)
        mean_contrib = pd.concat([melt_by_elev(topdir, yr, typ) for yr in year_range], axis=1).mean(axis=1)
        if contribs_all is None:
            contribs_all = mean_contrib
        else:
            contribs_all = pd.concat((contribs_all, mean_contrib), axis=1)

    contribs_all.columns = source_types
    contribs_all = contribs_all.fillna(value=0)
    return contribs_all


def main():

    topdir = '/projects/CHARIS/derived_hypsometries/MODSCAG_GF_v09_fromFile_rainv01_less_ET/'
    subdir_patt = 'IN_v01_OBJECTID*'
    subdirs = glob.glob(os.path.join(topdir, subdir_patt))

    print("Subdirs:  ", subdirs)

    contribs_fullbasin = None

    for subdir in subdirs:
        contribs_onebasin = do_one_basin(subdir)
        print("======== SUBDIR: ", subdir)
        #print(contribs_onebasin)
        if contribs_fullbasin is None:
            contribs_fullbasin = contribs_onebasin
        else:
            contribs_fullbasin = contribs_fullbasin.add(contribs_onebasin, fill_value=0.0)

    with pd.option_context('display.max_rows', None):
        print(contribs_fullbasin)
    #contribs_all.to_csv('mean_contribs_by_type.csv')


if __name__ == '__main__':
    main()

# Example set of files:
# 
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.exposed_glacier_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.GRSIZE_SCAG.fromFile.snow_on_ice_melt_by_elev.best_Hunza_model.txt
# IN_Hunza_at_DainyorBridge.2001.0100m.modicev04_3strike.snow_on_land_melt_by_elev.best_Hunza_model.txt

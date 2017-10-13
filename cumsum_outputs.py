#!/usr/bin/env python3

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


melt_file = 'IN_fullbasin_meltcontributionstytype_500m.txt'
precip_file = 'IN_v01_fullbasinmasks.MERRA_rainfall_km3.annual_mean.by_elev.txt'

melt_df = pd.read_csv(melt_file, sep='\s+')
print(melt_df)

prec_df = pd.read_csv(precip_file, sep='\s+')
print(prec_df)

melt_cum = melt_df.sort_index(ascending=False).cumsum()
prec_cum = prec_df.sort_index(ascending=False).cumsum()

print(melt_cum)
print(prec_cum)

all_contribs = pd.concat((melt_cum, prec_cum), axis=1)

print(all_contribs)

# Calculate contributions as fraction of total.  Drop all rows with all zeros first.

all_contribs = all_contribs[(all_contribs.T != 0).any()]        # drop zero rows

sums = all_contribs.sum(axis=1)
print("SUMS\n", sums)
all_contribs_fraction = all_contribs.divide(sums.values, axis='index')

print("FRACTIONS")
print(all_contribs_fraction)

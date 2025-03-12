import pandas as pd
import geopandas as gpd
from decouple import config

from difflib import get_close_matches


def apply_manual_replace(target, replaces):
    for s_from, s_to in replaces:
        target = target.replace(s_from, s_to)
    return target


def print_precinct_debug_info(df_geo, df_data, manual_replace=None, manual_fixes=None):
    geo_p_names = [p for p in list(df_geo['NAME20'])]
    geopname2vtd = dict()
    for _, row in df_geo.iterrows():
        geopname2vtd[row['NAME20']] = [row['VTDST20'], row['geometry']]

    print("These are the possible names in the GEO data (the VTDST20s and Geo's)")
    for p in sorted(geo_p_names):
        print(p)

    data_p_names = [p.upper() for p in list(df_data['precinct'].unique())]
    print("best guesses for closest GEO from DATA, with manual corrections if provided.")
    print(f"VTDST20 |    OG P Name     |      Fixed P Name      |   Resolved Geo P Name")
    print("-"*80)
    for p_data_og in data_p_names:
        p_data = p_data_og

        if manual_replace:
            p_data = apply_manual_replace(p_data, manual_replace)

        if manual_fixes and (p_data in manual_fixes):
            p_geo = manual_fixes[p_data]
        else:
            closest = get_close_matches(p_data, geo_p_names, n=1)
            if len(closest) > 0:
                p_geo = get_close_matches(p_data, geo_p_names, n=1)[0]
            else:
                p_geo = " "

        if p_geo in geopname2vtd:
            vtd = geopname2vtd[p_geo][0]
        else:
            vtd = "MISSING"

        print(f"{vtd:7} | {p_data_og:16} | {p_data:22} | {p_geo}")


def process_precincts_with_manual_fixes(df_geo, df_data, manual_replace=None, manual_fixes=None):
    geo_p_names = [p for p in list(df_geo['NAME20'])]
    geopname2vtd = dict()
    vtd2geo = dict()
    for _, row in df_geo.iterrows():
        geopname2vtd[row['NAME20']] = [row['VTDST20'], row['geometry']]
        vtd2geo[row['VTDST20']] = row['geometry']

    vtds = list()
    for _, row in df_data.iterrows():
        p_name = row['precinct'].upper()
        p_data_fixed = apply_manual_replace(p_name, manual_replace)

        if p_data_fixed in manual_fixes:
            p_geo = manual_fixes[p_data_fixed]
        else:
            closest = get_close_matches(p_data_fixed, geo_p_names, n=1)
            if len(closest) > 0:
                p_geo = get_close_matches(p_data_fixed, geo_p_names, n=1)[0]
            else:
                p_geo = " "

        if p_geo in geopname2vtd:
            vtd = geopname2vtd[p_geo][0]
        else:
            vtd = "MISSING"

        vtds.append(vtd)

    df_data['VTDST20'] = vtds
    return df_data, vtd2geo

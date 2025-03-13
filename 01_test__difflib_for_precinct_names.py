import pandas as pd
import geopandas as gpd

from difflib import get_close_matches

DIR_DATA = "./data/parsed/42-PA/2024"
DIR_SAVE = ""
FN_DATA  = "001_adams_county_2024.csv"
COUNTY_CODE = "001"

DIR_GEO = "./data/raw/42-PA/voting_districts"
FN_GEO = "cb_2020_42_vtd_500k.shp"

gdf = gpd.read_file(f"{DIR_GEO}/{FN_GEO}")
gdf = gdf[gdf['COUNTYFP20'] == COUNTY_CODE]

MANUAL_REPLACES = [
    ["MT", "MOUNT"]
]

MANUAL_FIXES = {
    "CONEWAGO 3": "CONEWAGO DISTRICT 03",
    "GETTYSBURG 1": "GETTYSBURG WARD 01 PRECINCT 01",
    "GETTYSBURG 3": "GETTYSBURG WARD 03 PRECINCT 01",
    "HUNTINGTON": "HUNTINGTON DISTRICT 01",
    "OXFORD 1": "OXFORD DISTRICT 01",
    "OXFORD 2": "OXFORD DISTRICT 02"
}

geo_p_names = [p for p in list(gdf['NAME20'])]
geopname2vtd = dict()
vtd2geo = dict()
for _, row in gdf.iterrows():
    geopname2vtd[row['NAME20']] = [row['VTDST20'], row['geometry']]
    vtd2geo[row['VTDST20']] = row['geometry']

print(sorted(geo_p_names))

df = pd.read_csv(f"{DIR_DATA}/{FN_DATA}")

def apply_manual_replace(target, replaces):
    for s_from, s_to in replaces:
        target = target.replace(s_from, s_to)
    return target


data_p_names = [p.upper() for p in list(df['precinct'].unique())]

print("looking for closest GEO from DATA")
for p in data_p_names:
    p_data_fixed = apply_manual_replace(p, MANUAL_REPLACES)

    if p_data_fixed in MANUAL_FIXES:
        p_geo = MANUAL_FIXES[p_data_fixed]
    else:
        p_geo = get_close_matches(p_data_fixed, geo_p_names, n=1)[0]

    if p_geo in geopname2vtd:
        vtd = geopname2vtd[p_geo][0]
    else:
        vtd = "MISSING"
    print(f"{vtd:7} | {p:16} | {p_data_fixed:22} | {p_geo}")

vtds = list()
for _, row in df.iterrows():
    p_name = row['precinct']
    p_data_fixed = apply_manual_replace(p_name, MANUAL_REPLACES)

    if p_data_fixed in MANUAL_FIXES:
        p_geo = MANUAL_FIXES[p_data_fixed]
    else:
        p_geo = get_close_matches(p_data_fixed, geo_p_names, n=1)[0]

    if p_geo in geopname2vtd:
        vtd = geopname2vtd[p_geo][0]
    else:
        vtd = "MISSING"

    vtds.append(vtd)

df['VTDST20'] = vtds

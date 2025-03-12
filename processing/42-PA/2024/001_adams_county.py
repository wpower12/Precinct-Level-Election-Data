import pandas as pd
import geopandas as gpd
import pickle

from helper.processing import print_precinct_debug_info, process_precincts_with_manual_fixes

FN_DATA     = "001_adams_county_2024.csv"
COUNTY_CODE = "001"

DIR_DATA = "../../../data/parsed/42-PA/2024"
DIR_SAVE = "../../../data/processed/42-PA/2024"
DIR_GEO  = "../../../data/raw/42-PA/voting_districts"
FN_GEO   = "cb_2020_42_vtd_500k.shp"

gdf = gpd.read_file(f"{DIR_GEO}/{FN_GEO}")
gdf = gdf[gdf['COUNTYFP20'] == COUNTY_CODE]  # Geo data with shapefile geometries.
df  = pd.read_csv(f"{DIR_DATA}/{FN_DATA}")   # Data from Precinct Parsing.

# GOAL - Fill these two objs in with the minimum needed so that Precinct names correctly map to their VTDST20's.
#      - These will start empty.
MANUAL_REPLACES = [
    [" MT ", "MOUNT"]
]
MANUAL_FIXES = {
    "CONEWAGO 3": "CONEWAGO DISTRICT 03",  # Missing district - Issue related to using 2020 geo for 2024 data.
    "GETTYSBURG 1": "GETTYSBURG WARD 01 PRECINCT 01",
    "GETTYSBURG 3": "GETTYSBURG WARD 03 PRECINCT 01",
    "HUNTINGTON": "HUNTINGTON DISTRICT 01",
    "OXFORD 1": "OXFORD DISTRICT 01",
    "OXFORD 2": "OXFORD DISTRICT 02"
}

# Step 1 - Look at raw data to fill out possible fixes and replaces for precinct names
print_precinct_debug_info(gdf, df, manual_replace=MANUAL_REPLACES, manual_fixes=MANUAL_FIXES)

# Step 2 - Actually fill in the VTDST20's into the CSV, and save out the map of VTDST20 -> Geometry
df, vtd2geo = process_precincts_with_manual_fixes(gdf, df, manual_replace=MANUAL_REPLACES, manual_fixes=MANUAL_FIXES)

# Step 3 - Fix Race Names. - Need to figure that out. Oof. Should open ALL of them at once and do a thing.
...

# Final Step - Save stuff.
df.to_csv(f"{DIR_SAVE}/{FN_DATA}", index=False)
with open(f"{DIR_SAVE}/{COUNTY_CODE}_vtd2geo.p", 'wb') as f:
    pickle.dump(vtd2geo, f)

"""
First 'non PDF' return to process. XML.

These seem to be a common type; 'clarity election' service.
"""
import pandas as pd

from helper.parsing.xml import parse_clarity_xml

DIR_DATA = "../../../data/raw/42-PA/2024"
DIR_SAVE = "../../../data/parsed/42-PA/2024"

FN_DATA  = "051_fayette_county_2024.xml"
FN_SAVE  = "051_fayette_county_2024.csv"

YEAR = 2024

election_results = parse_clarity_xml(f"{DIR_DATA}/{FN_DATA}", YEAR)

df = pd.DataFrame(election_results, columns=['precinct','year','race','party','candidate','votes'])
df.to_csv(f"{DIR_SAVE}/{FN_SAVE}", index=False)

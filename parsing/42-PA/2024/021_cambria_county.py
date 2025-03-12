"""
Same exact XML format as 02_allegheny_county

Add a cleaned up version to the helper module. Call it 'parse_from_clarity_xml' since these are apparently
from the 'clarity election' service.
"""
import pandas as pd
from helper.parsing.xml import parse_clarity_xml

DIR_DATA = "../../../data/raw/42-PA/2024"
DIR_SAVE = "../../../data/parsed/42-PA/2024"

FN_DATA  = "021_cambria_county_2024.xml"
FN_SAVE  = "021_cambria_county_2024.csv"

YEAR = 2024

election_results = parse_clarity_xml(f"{DIR_DATA}/{FN_DATA}", YEAR)

df = pd.DataFrame(election_results, columns=['precinct','year','race','party','candidate','votes'])
df.to_csv(f"{DIR_SAVE}/{FN_SAVE}", index=False)

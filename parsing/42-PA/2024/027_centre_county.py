"""
Uses the "<PRECINCT HEADER> <SOME RACE TABLES>" PDF format, where we know each page has a set of complete tables.

Can use the 'Default' Prompt.
"""
import pandas as pd
from decouple import config
from openai import OpenAI

from helper.parsing.pdf import parse_simple_precinct_per_page_llm

DIR_DATA = "../../../data/raw/42-PA/2024"
DIR_SAVE = "../../../data/parsed/42-PA/2024"

FN_DATA  = "027_centre_county_2024.pdf"
FN_SAVE  = "027_centre_county_2024.csv"

BATCH_SIZE = 6
MODEL_STR = "gpt-4o-2024-08-06"

oai_client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

res_returns = parse_simple_precinct_per_page_llm(f"{DIR_DATA}/{FN_DATA}", oai_client, MODEL_STR, BATCH_SIZE)

df = pd.DataFrame(data=res_returns, columns=['precinct','year','race','party','candidate','votes'])
df.to_csv(f"{DIR_SAVE}/{FN_SAVE}", index=False)

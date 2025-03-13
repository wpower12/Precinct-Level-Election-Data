import pandas as pd
from PyPDF2 import PdfReader
from decouple import config
from openai import OpenAI
from tqdm import tqdm
from pydantic import BaseModel
import json

DIR_DATA = "data/raw/42-PA"
FN_DATA  = "027_centre_county_2024.pdf"
FN_SAVE  = "testing_gpt.txt"
MODEL_STR = "gpt-4o-2024-08-06"
PAGE_NUMS = [0, 1, 2]


PROMPT = """You will be given the text pages of a PDF that contain tabular information about election returns. 
Your task will be to parse the information into a list of returns. Each entry in the list will represent a single candidates
total votes from a specific precinct, in a specific race. 

You will be sent multiple pages. Each page will have a consistent layout.
The page you are shown will contain a section at the top, a header, which contains the election name and date, the county name, and the precinct name.
After the header, there will be multiple tabular sections, each containing a contiguous set of rows of data for a specific race. 
The name of the race (<RACE NAME>) will be written before the block of tabular data.

For each of the rows of data that contain a candidate (not the aggregated data in the last two rows), you will create a new item for the result list you will return to me. 
Each row in the table contains data in the following format: <PARTY> <NAME> <TOTAL VOTES> <ELECTION DAY VOTES> <MAIL IN VOTES> <PROVISIONAL BALLOTS>

For each of the races in the text of the PDF document, you will create a new piece of data. This data will look like this:
{
    'precinct': <PRECINCT NAME>,
    'year': <ELECTION YEAR>,
    'race': <RACE NAME>,
    'party': <PARTY>,
    'candidate': <NAME>,
    'votes': <TOTAL VOTES>
}

Your task is to return the full list of election return data from the set of pages you are sent. 
"""

class PrecinctReturn(BaseModel):
    precinct:  str
    year:      str
    party:     str
    candidate: str
    votes: int

class Returns(BaseModel):
    returns: list[PrecinctReturn]


oai_client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)

messages = [
    {'role': 'system', 'content': PROMPT},
    {'role': 'user', 'content': "Each subsequent message will be the text of a page from an election results PDF. Please parse them into the list of return data."},
]

with open(f"{DIR_DATA}/{FN_DATA}", 'rb') as f:
    pdf = PdfReader(f)
    for n in PAGE_NUMS:
        page_text = pdf.pages[n].extract_text()
        messages.append({'role': 'user', 'content': page_text})

res = oai_client.beta.chat.completions.parse(
    model=MODEL_STR,
    messages=messages,
    response_format=Returns
).choices[0].message.content

with open(f"{DIR_DATA}/{FN_SAVE}", 'w') as f:
    f.write(res)

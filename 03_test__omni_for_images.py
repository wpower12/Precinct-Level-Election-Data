"""
Another folder of PDFs. Fun. These are all images. What the fuck.

Folder of IMAGES of pdfs.
"""
import os
import pandas as pd
from pydantic import BaseModel
from decouple import config
from openai import OpenAI
from PyPDF2 import PdfReader
from PIL import Image
import io
import base64

PATH_DATA = "./data/raw/42-PA/2024"
PATH_SAVE = "./data/parsed/42-PA/2024"

DIR_DATA = "023_cameron_county_2024"

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


def show_pfd_img_obj(img_obj):
    img_buff = io.BytesIO()
    Image.open(io.BytesIO(img_obj.data)).save(img_buff, format="png")
    img_to_show = Image.open(img_buff)
    img_to_show.show()


def b64encode_pdf_img_obj(img_obj):
    img_buff = io.BytesIO()
    Image.open(io.BytesIO(img_obj.data)).save(img_buff, format="png")
    return base64.b64encode(img_buff.getvalue()).decode("utf-8")


for fn in os.listdir(f"{PATH_DATA}/{DIR_DATA}"):
    with open(f"{PATH_DATA}/{DIR_DATA}/{fn}", 'rb') as f:
        pdf = PdfReader(f)
        # Looks like they always start at 1.
        for page in pdf.pages[1:]:
            # Looks like (for now), only one image per page. This assumption will surely give at some point.
            img = page.images[0]
            show_pfd_img_obj(img)
            b64_str = b64encode_pdf_img_obj(img)
            print(b64_str)

            break
    break

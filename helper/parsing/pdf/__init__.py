from PyPDF2 import PdfReader
from pydantic import BaseModel
from tqdm import tqdm


class PrecinctReturn(BaseModel):
    precinct:  str
    year:      str
    race:      str
    party:     str
    candidate: str
    votes: int

    # To make it easier to create DFs/csvs.
    def to_dict(self):
        return {
            'precinct':  self.precinct,
            'year':      self.year,
            'race':      self.race,
            'party':     self.party,
            'candidate': self.candidate,
            'votes':     self.votes,
        }

class Returns(BaseModel):
    returns: list[PrecinctReturn]


DEFAULT_SPPP_PROMPT = """You will be given the text pages of a PDF that contain tabular information about election returns. 
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


def make_batches(n, b):
    a = range(n)
    return [a[i:i + b] for i in range(0, n, b)]


def parse_simple_precinct_per_page_llm(path_pdf, oai_client, model_str, batch_size, prompt=DEFAULT_SPPP_PROMPT, debug=False):
    # I'm worried about keeping a fp open the entire time we're waiting for the model to return a result, so
    # I'm gonna be cautious, and open the file, get what I need, and close it. So things will be redundant occasionally
    with open(path_pdf, 'rb') as f:
        num_pages = len(PdfReader(f).pages)

    all_returns = list()
    batches = make_batches(num_pages, batch_size)
    for batch in tqdm(batches, total=len(batches)):
        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user',
             'content': "Each subsequent message will be the text of a page from an election results PDF. Please parse them into the list of return data."},
        ]
        with open(path_pdf, 'rb') as f:
            pdf = PdfReader(f)
            for n in batch:
                page_text = pdf.pages[n].extract_text()
                messages.append({'role': 'user', 'content': page_text})

        result = oai_client.beta.chat.completions.parse(
            model=model_str,
            messages=messages,
            response_format=Returns
        ).choices[0].message.parsed

        res_returns = [r.to_dict() for r in result.returns]
        all_returns.extend(res_returns)

        if debug:
            break

    return all_returns

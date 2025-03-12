from PyPDF2 import PdfReader
from pydantic import BaseModel
from tqdm import tqdm
import json
import pandas as pd
from lxml import etree



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
            'votes':  self.votes,
        }

class Returns(BaseModel):
    returns: list[PrecinctReturn]


def make_batches(n, b):
    a = range(n)
    return [a[i:i + b] for i in range(0, n, b)]


def parse_w_llm(path_pdf, prompt, oai_client, model_str, batch_size, debug=False):
    # I'm worried about keeping a fp open the entire time we're waiting for the model to return a result, so
    # i'm gonna be cautious, and open the file, get what I need, and close it. So things will be redundant occasionally
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


def parse_clarity_xml(path_xml, year):
    tree = etree.parse(path_xml)
    root = tree.getroot()
    raw_rows = list()
    for contest in root.findall("Contest"):
        race = contest.get('text')
        for candidate in contest.findall("Choice"):
            c_name = candidate.get('text')
            c_party = candidate.get('party')
            t_votes = candidate.get('totalVotes')
            if c_name == 'Write-in':
                continue

            total_votes = dict()
            for vote_type in candidate.findall("VoteType"):
                for precinct in vote_type.findall("Precinct"):
                    p_name = precinct.get("name")
                    p_votes = int(precinct.get("votes"))
                    if p_name not in total_votes:
                        total_votes[p_name] = p_votes
                    else:
                        total_votes[p_name] += p_votes

            for p_name in total_votes:
                # precinct, year, race, party, candidate, votes
                raw_rows.append([p_name, year, race, c_party, c_name, total_votes[p_name]])
    return raw_rows

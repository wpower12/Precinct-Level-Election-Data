from lxml import etree


def parse_clarity_xml(path_xml, year):
    tree = etree.parse(path_xml)
    root = tree.getroot()
    raw_rows = list()
    for contest in root.findall("Contest"):
        race = contest.get('text')
        for candidate in contest.findall("Choice"):
            c_name  = candidate.get('text')
            c_party = candidate.get('party')
            t_votes = candidate.get('totalVotes')

            if not c_party:
                continue
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

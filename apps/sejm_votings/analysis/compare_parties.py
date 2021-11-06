import itertools
from apps.sejm_votings.models import Voting


def get_voting_ratio(voting: Voting, party):
    results = voting.results[party]
    all_voting = results["for"] + results["against"]
    if all_voting == 0:
        return 0

    return (results["for"] - results["against"]) / all_voting


def get_data(data: list[Voting], parties=None):
    all_parties = data[0].results.keys()
    pairs = list(itertools.combinations(all_parties, 2))

    if parties:
        parties = list(filter(lambda x: x, parties))
        if len(parties) == 1:
            pairs = list(filter(lambda x: x[0] == parties[0] or x[1] == parties[0], pairs))
        elif len(parties) == 2:
            pairs = list(itertools.combinations(parties, 2))

    values = []
    form = "całości"
    votings_ids = []
    results = []
    for parties_pair in pairs:
        for voting in data:
            no_parties = any(party not in voting.results for party in parties_pair)
            incorrect_form = form not in voting.form

            if no_parties or incorrect_form:
                continue

            votings_ids.append(voting.topic + voting.form)

            voting_values = list(map(lambda party: get_voting_ratio(voting, party), parties_pair))
            votings_similar = len(set(map(lambda value: value > 0, voting_values))) == 1
            values.append(1 if votings_similar else 0)
        value = sum(values) / len(values)
        result = {
            "party_1": parties_pair[0],
            "party_2": parties_pair[1],
            "value": value
        }
        results.append(result)
    return results

import itertools
import json


def get_data():
    with open('db.txt', "r", encoding="utf8") as file:
        lines = file.read().split("\n")
        array = []

        for line in lines:
            if len(line) == 0 or line[0] != "{":
                continue

            data = json.loads(line)
            array.append(data)

        return array


def get_voting_ratio(voting, party):
    results = voting["results"][party]
    all_voting = results["for"] + results["against"]
    if all_voting == 0:
        return 0

    return (results["for"] - results["against"]) / all_voting


data = get_data()
parties = ["Lewica", "Konfederacja", "PiS", "KO"]
values = []
topics = [""]
form = "całości"
pairs = list(itertools.combinations(parties, 2))
votings_ids = []

for parties_pair in pairs:
    for voting in data:
        no_topics = not any(topic in voting["topic"].lower() for topic in topics)
        no_parties = any(party not in voting["results"] for party in parties_pair)
        incorrect_form = form not in voting["form"]

        if no_topics or no_parties or incorrect_form:
            continue

        votings_ids.append(voting["topic"] + voting["form"])

        voting_values = list(map(lambda party: get_voting_ratio(voting, party), parties_pair))
        votings_similar = len(set(map(lambda value: value > 0, voting_values))) == 1
        values.append(1 if votings_similar else 0)

        # if votings_similar:
        #     print(voting["topic"], voting["form"], f"https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9&NrPosiedzenia={voting['sitting']}&NrGlosowania={voting['voting']}")

    value = sum(values) / len(values)
    topics_joined = ", ".join(topics)
    row = [*parties_pair, str(value), topics_joined]
    print('\t'.join(row))

print(len(set(votings_ids)))
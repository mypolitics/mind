import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9'


def get_page(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'
    page = BeautifulSoup(response.text, 'html.parser')

    notFound = page.find(text="Brak danych")

    return None if notFound is not None else page


def get_nr_kadnencji():
    return BASE_URL.split('=')[-1]


def get_all_sitting_and_voting_count():
    page = get_page(BASE_URL)

    table_rows = page.select('tbody > tr')

    sitting_and_voting = {}
    sitting = None
    count = 0
    for row in table_rows:
        columns = row.select('td')

        if nrSitting := columns[0].text.strip():
            if sitting:
                sitting_and_voting[sitting] = count
                count = 0
            sitting = nrSitting
        count += int(columns[-1].text.strip())
    sitting_and_voting[sitting] = count

    return sitting_and_voting


class SejmVoting:
    baseUrl = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9'
    sittingIndex = ""
    votingCount = ""

    def __init__(self, sittingIndex, votingCount):  # 37, 108
        self.sittingIndex = sittingIndex
        self.votingCount = votingCount

    def getQueryUrl(self, sittingIndex, votingIndex):
        return f"{self.baseUrl}&NrPosiedzenia={sittingIndex}&NrGlosowania={votingIndex}"

    def getVoting(self, url: str):
        page = get_page(url)

        if page is None:
            print(page)
            return page

        rows = page.find_all('tr')[1:]
        topic, form = page.select("p.subbig")
        date = page.select('#title_content > h1 > small')[0].text[5:15]

        data = {
            'topic': topic.text,
            'form': form.text,
            'date': date,
            'sitting': self.sittingIndex,
            'voting': url.split('=')[-1],
            'results': {},
        }

        for row in rows:
            cols = row.find_all('td')[:7]
            club = cols[0].text
            cols_numbers = [int(ele.text.replace("-", "0")) for ele in cols[1:]]
            members, _, _for, against, abstain, absent = cols_numbers

            data['results'][club] = {
                'members': members,
                'for': _for,
                'against': against,
                'abstain': abstain,
                'absent': absent
            }

        return data

    def get_data(self, lastVoting=1):
        urls = []

        for i in range(lastVoting, self.votingCount + 1):
            urls.append(self.getQueryUrl(self.sittingIndex, i))

        sitting_data = [self.getVoting(url) for url in urls]

        return sitting_data


def get_sittings_data(dbSitting=None, dbVoting=None):
    sitting_and_voting = get_all_sitting_and_voting_count()
    if dbSitting:
        sitting_and_voting = {k: v for k, v in sitting_and_voting.items() if int(k) >= dbSitting}


    all_votings = sum(sitting_and_voting.values()) - (dbVoting or 0)
    print(f'Do pobrania: {all_votings}')
    data = []
    for key, value in sitting_and_voting.items():
        sejmVouting = SejmVoting(key, value)
        if int(key) == dbSitting:
            data.extend(sejmVouting.get_data(dbVoting + 1))
        else:
            data.extend(sejmVouting.get_data())
        if all_votings:
            print(f'pobrane: {len(data)} progress {round(len(data) / all_votings * 100, 1)}%', )

    return data


if __name__ == '__main__':
    start = datetime.now()
    data = get_sittings_data()
    print(f'Finish in {datetime.now() - start}')
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump({'data': data}, file, indent=2, ensure_ascii=False)

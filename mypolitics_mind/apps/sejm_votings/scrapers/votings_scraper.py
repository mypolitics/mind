import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import concurrent.futures as futures

BASE_URL = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9'


def get_page(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'
    page = BeautifulSoup(response.text, 'html.parser')

    notFound = page.find(text="Brak danych")

    return None if notFound is not None else page


def get_new_setting_and_voting_count():
    response = requests.get(BASE_URL)
    response.encoding = 'UTF-8'
    page = get_page(BASE_URL)

    table = page.select('tbody > tr')

    sittingIndex = table[0].select_one('td').text

    index = 1
    for row in table[1:]:
        if row.select_one('td').text.strip():
            break
        index += 1

    votingCount = sum((int(row.select('td')[-1].text) for row in table[:index]))

    return int(sittingIndex), votingCount


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
        data = {
            'topic': topic.text,
            'form': form.text,
            'date': page.select('#title_content > h1 > small')[0].text[5:15],
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

        with futures.ThreadPoolExecutor() as execut:
            data = execut.map(self.getVoting, urls)

        return list(data)


def get_new_sitting_data(dbSitting=None, dbVoting=None):
    newSitting, newVotingCount = get_new_setting_and_voting_count()
    sejmVouting = SejmVoting(newSitting, newVotingCount)

    if newSitting == dbSitting:
        if newVotingCount == dbVoting:
            return None

        dbVoting = dbVoting + 1 if dbVoting else 1
        return sejmVouting.get_data(dbVoting)

    return sejmVouting.get_data()


if __name__ == '__main__':
    start = datetime.now()
    data = get_new_sitting_data()
    print(f'Finish in {datetime.now() - start}')

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

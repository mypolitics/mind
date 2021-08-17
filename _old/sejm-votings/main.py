import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Process

class SejmVoting:
    baseUrl = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9'
    sittingIndex = ""
    votingIndex = ""

    def __init__(self, sittingIndex, votingIndex):
        self.queryUrl = self.getQueryUrl(sittingIndex, votingIndex)
        self.sittingIndex = sittingIndex
        self.votingIndex = votingIndex

    def getQueryUrl(self, sittingIndex, votingIndex):
        return f"{self.baseUrl}&NrPosiedzenia={sittingIndex}&NrGlosowania={votingIndex}"

    def getPage(self):
        response = requests.get(self.queryUrl)
        response.encoding = 'UTF-8'
        page = BeautifulSoup(response.text, 'html.parser')
        notFound = page.find(text="Brak danych")

        return None if notFound is not None else page

    def getVoting(self):
        page = self.getPage()
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
            'voting': self.votingIndex,
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


sittings_config = {
 "22": 183,
 "23": 23,
 "24": 73,
 "25": 198,
 "26": 94,
 "27": 90,
 "28": 173,
 "29": 18,
 "30": 159,
 "31": 19,
 "33": 111,
 "34": 91,
 "35": 89,
}


def process_sitting(sitting):
    with open("lines.txt", "a") as lines:
        for voting in range(1, sittings_config[sitting]):
            sv = SejmVoting(sitting, voting)
            print(sv.getVoting())
            if sv is None:
                break

            voting_data = str(json.dumps(sv.getVoting()))
            lines.write("\n" + voting_data)

if __name__=='__main__':
    for sitting in sittings_config:
        Process(target=process_sitting, args=(sitting,)).start()

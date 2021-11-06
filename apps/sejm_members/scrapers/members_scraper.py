import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

MEMBERS_PAGE_URL = 'https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A'
MEMBERS_PAGE = requests.get(MEMBERS_PAGE_URL)


def get_page(url):
    return requests.get(url).content


def get_members_urls(page):
    page = BeautifulSoup(page.content, 'html.parser')
    members_link = page.select('ul.deputies > li > div > a', href=True)
    urls = list(
        map(lambda x: 'https://www.sejm.gov.pl/' + x['href'], members_link))
    return urls


def parse_page(url):
    html = get_page(url)
    page = BeautifulSoup(html, 'html.parser')

    name = page.select_one('#title_content > h1').text
    electionDate = page.select_one(
        'div.partia > ul > li:nth-child(1) > p.right').text
    list = page.select_one('div.partia > ul > li:nth-child(2) > p.right').text
    region = page.select_one(
        'div.partia > ul > li:nth-child(3) > p.right').text
    votes = page.select_one('div.partia > ul > li:nth-child(4) > p.right').text
    pledge = page.select_one(
        'div.partia > ul > li:nth-child(5) > p.right').text
    experience = page.select_one(
        'div.partia > ul > li:nth-child(6) > p.right').text
    party = page.select_one('div.partia > ul > li:nth-child(7) > p.right').text

    dateOfBirth = page.select_one(
        'div.cv > ul > li:nth-child(1) > p.right').text

    education = page.select_one('div.cv > ul > li:nth-child(2)')

    if education.select_one('p.left').text == 'Wykształcenie:':
        education = education.select_one('p.right').text
    else:
        education = None

    school = page.select_one('div.cv > ul > li:nth-last-child(2)')

    if school.select_one('p.left').text == 'Ukończona szkoła:':
        school = school.select_one('p.right').text
    else:
        school = None

    job = page.select_one('div.cv > ul > li:nth-last-child(1) > p.right').text

    photoUrl = page.select_one(
        '#view\\:_id1\\:_id2\\:facetMain\\:_id109\\:_id111')['src']

    return {
        'name': name,
        'electionDate': electionDate,
        'list': list,
        'region': region,
        'votes': votes,
        'pledge': pledge,
        'experience': experience,
        'party': party,
        'dateOfBirth': dateOfBirth,
        'education': education,
        'school': school,
        'job': job,
        'photoUrl': photoUrl
    }


def get_all_members():
    urls = get_members_urls(MEMBERS_PAGE)

    result = [parse_page(url) for url in urls]

    return result


if __name__ == '__main__':
    start = datetime.now()
    data = get_all_members()
    with open('members.json', 'w', encoding='utf-8') as file:
        json.dump({'members': data}, file, indent=2, ensure_ascii=False)

    print(f'Finish in {datetime.now() - start}')

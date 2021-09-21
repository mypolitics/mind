from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os
import aiohttp
import asyncio

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

URL = 'https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A'
URL = requests.get(URL)
PAGE = BeautifulSoup(URL.content, 'html.parser')


async def get_page(session, url):
    async with session.get(url) as r:
        return await r.text()


async def get_all_pages(session, urls):
    tasks = []

    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


def parse_page(html):
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
    try:
        education = page.select_one(
            'div.cv > ul > li:nth-child(2) > p.right').text
    except AttributeError:
        education = None
    try:
        school = page.select_one(
            'div.cv > ul > li:nth-child(3) > p.right').text
    except AttributeError:
        school = None
    try:
        job = page.select_one('div.cv > ul > li:nth-child(4) > p.right').text
    except AttributeError:
        job = None
    photoUrl = page.select_one(
        '#view\\:_id1\\:_id2\\:facetMain\\:_id109\\:_id111')['src']

    return {
        'name': name,
        'electionDate': datetime.strptime(electionDate, '%d-%m-%Y').date(),
        'list': list,
        'region': region,
        'votes': votes,
        'pledge': datetime.strptime(pledge, '%d-%m-%Y').date(),
        'experience': experience,
        'party': party,
        'dateOfBirth': dateOfBirth,
        'education': education,
        'school': school,
        'job': job,
        'photoUrl': photoUrl
    }


async def get_members(urls):
    members = []
    async with aiohttp.ClientSession() as session:
        pages = await get_all_pages(session, urls)

    for page in pages:
        member = parse_page(page)
        members.append(member)

    return members


def get_all_members():
    members_link = PAGE.select('ul.deputies > li > div > a', href=True)
    urls = list(
        map(lambda x: 'https://www.sejm.gov.pl/' + x['href'], members_link))

    results = asyncio.run(get_members(urls))

    return results

import asyncio
import math
import os
from datetime import datetime

import aiohttp
import requests as requests
from bs4 import BeautifulSoup

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_and_parse_page(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'
    return BeautifulSoup(response.text, 'html.parser')


async def get_page_async(session, url):
    async with session.get(url) as r:
        return await r.text()


def parse_article(page, url):
    page = BeautifulSoup(page, 'html.parser')

    title = page.select_one('article h1').text
    image_src = page.select_one('article img', src=True)['src']
    author_name = page.select_one(
        'article #ArticleInfo > li:first-child > b').text
    date = page.select_one('article #ArticleInfo > li:last-child > b').text
    content = str(page.select_one('article .ModuleText'))
    slug = url.split('/').pop()

    if date == author_name:
        author_name = None

    return {
        'title': title,
        'slug': slug,
        'date': datetime.strptime(date, '%d.%m.%Y, %H:%M'),
        'content': content,
        'image': {
            'src': image_src,
            'alt': title,
        },
        'author': author_name,
    }


class PoinformowaniScraper:
    base_page = 'https://wiadomosci.poinformowani.pl/'
    per_page = 48

    def get_page_urls(self, index):
        url = f'{self.base_page}?page={index}'
        page = get_and_parse_page(url)
        links = page.select('article > a', href=True)

        return list(map(lambda link: link['href'], links))

    def get_urls(self, start, end):
        urls = []

        pages_count = math.ceil(end / self.per_page)
        for page in range(pages_count):
            page_urls = self.get_page_urls(page + 1)
            urls.extend(page_urls)

        return urls[start:end]

    async def parse_many_articles(self, start, end, end_slug):

        urls = self.get_urls(start, end)

        if end_slug:
            end_index = None
            for url in urls:
                if end_slug in url:
                    end_index = urls.index(url)
            urls = urls[:end_index]
        articles = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                page = await get_page_async(session, url)
                articles.append(parse_article(page, url))

        return articles

    def get_many_articles(self, start=0, end=per_page, slug=None):
        return asyncio.run(self.parse_many_articles(start, end, slug))

import math
import requests as requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_and_parse_page(url):
    response = requests.get(url)
    response.encoding = 'UTF-8'
    return BeautifulSoup(response.text, 'html.parser')


class PoinformowaniUtil:
    base_page = 'https://wiadomosci.poinformowani.pl/'
    per_page = 48

    def get_page_urls(self, index):
        url = f'{self.base_page}?page={index}'
        page = get_and_parse_page(url)
        links = page.select('article > a', href=True)
        return list(map(lambda link: link['href'], links))

    def get_urls(self, start, end):
        urls = []

        pages = math.ceil(end / self.per_page)
        for page in range(0, pages):
            page_urls = self.get_page_urls(page + 1)
            urls.extend(page_urls)

        return urls[start:end]

    def get_single_article(self, url):
        page = get_and_parse_page(url)
        title = page.select_one('article h1').text
        image_src = page.select_one('article img', src=True)['src']
        author_name = page.select_one(
            'article #ArticleInfo > li:first-child > b').text
        date = page.select_one('article #ArticleInfo > li:last-child > b').text
        content = str(page.select_one('article .ModuleText'))
        slug = url.split('/').pop()

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

    def get_many_articles(self, start, end):
        articles = []
        urls = self.get_urls(start, end)

        for url in urls:
            article = self.get_single_article(url)

            articles.append(article)

        return articles

    def get_new_articles(self, slug, start=0, end=per_page):

        articles = []
        urls = self.get_urls(start, end)

        for url in urls:
            article = self.get_single_article(url)

            if article['slug'] == slug:
                break

            articles.append(self.get_single_article(url))

        return articles

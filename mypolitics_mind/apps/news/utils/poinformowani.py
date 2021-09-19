import math
import requests as requests
from bs4 import BeautifulSoup


class PoinformowaniUtil:
    base_page = 'https://wiadomosci.poinformowani.pl/'

    @staticmethod
    def get_and_parse_page(self, url):
        response = requests.get(url)
        response.encoding = 'UTF-8'
        return BeautifulSoup(response.text, 'html.parser')

    def get_page_urls(self, index):
        url = f'{self.base_page}?page={index}'
        page = self.get_and_parse_page(url)
        links = page.select('article > a', href=True)
        return list(map(lambda link: link['href'], links))

    def get_urls(self, start, end):
        urls = []
        per_page = 48
        pages = math.ceil(end / per_page)
        for page in range(0, pages):
            page_urls = self.get_page_urls(page + 1)
            urls.extend(page_urls)

        return urls[start:end]

    def get_single_article(self, url):
        page = self.get_and_parse_page(url)
        title = page.select_one('article h1').text
        image_src = page.select_one('article img', src=True)['src']
        author_name = page.select_one('article #ArticleInfo > li:first-child > b').text
        date = page.select_one('article #ArticleInfo > li:last-child > b').text
        content = str(page.select_one('article .ModuleText'))
        slug = url.split('/').pop()

        return {
            'title': title,
            'slug': slug,
            'date': date,
            'content': content,
            'image': {
                'src': image_src,
                'alt': title,
            },
            'author': {
                'name': author_name,
            },
        }

    def get_many_articles(self, start, end):
        articles = []
        urls = self.get_urls(start, end)

        for url in urls:
            articles.append(self.get_single_article(url))

        return articles

import math
import requests as requests
from bs4 import BeautifulSoup

class PoinformowaniUtil:
    base_page = 'https://wiadomosci.poinformowani.pl/'

    def getAndParsePage(self, url):
        response = requests.get(url)
        response.encoding = 'UTF-8'
        return BeautifulSoup(response.text, 'html.parser')

    def getPageUrls(self, index):
        url = f'{self.base_page}?page={index}'
        page = self.getAndParsePage(url)
        links = page.select('article > a', href=True)
        return list(map(lambda link: link['href'], links))

    def getUrls(self, start, end):
        urls = []
        per_page = 48
        pages = math.ceil(end / per_page)
        for page in range(0, pages):
            page_urls = self.getPageUrls(page+1)
            urls.extend(page_urls)

        return urls[start:end]

    def getSingleArticle(self, url):
        page = self.getAndParsePage(url)
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


    def getManyArticles(self, start, end):
        articles = []
        urls = self.getUrls(start, end)

        for url in urls:
            articles.append(self.getSingleArticle(url))

        return articles

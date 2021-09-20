from django.http import HttpResponse

from mypolitics_mind.apps.news.models import News
from mypolitics_mind.apps.news.serializers import NewsSerializer
from mypolitics_mind.apps.news.utils.poinformowani import PoinformowaniUtil
from rest_framework import viewsets, mixins
from rest_framework.response import Response


class NewsPoinformowaniViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request, *args, **kwargs):
        newest = self.queryset.first()

        poinformowani = PoinformowaniUtil()

        articles = poinformowani.get_new_articles(newest.slug)
        new_articles = []
        for article in articles:
            article = News(
                title=article['title'],
                content=article['content'],
                date=article['date'],
                image=article['image'],
                slug=article['slug'],
                author=article['author']
            )
            new_articles.append(article)

        News.objects.bulk_create(new_articles)

        return super(NewsPoinformowaniViewSet, self).list(request, *args, **kwargs)

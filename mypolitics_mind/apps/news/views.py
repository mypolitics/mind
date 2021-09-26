from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from mypolitics_mind.apps.news.models import News
from mypolitics_mind.apps.news.scrapers.poinformowani import PoinformowaniScraper
from mypolitics_mind.apps.news.serializers import NewsSerializer


class NewsPoinformowaniViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = ['date']
    filterset_fields = ['author']
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        current_tz = timezone.get_current_timezone()
        poinformowani = PoinformowaniScraper()

        newest = self.queryset.first()

        articles = poinformowani.get_many_articles(slug=newest.slug if newest else None)

        new_articles = []

        for article in articles:
            article['date'] = current_tz.localize(article['date'])
            article = News(**article)

            new_articles.append(article)

        News.objects.bulk_create(new_articles)

        return super(NewsPoinformowaniViewSet, self).list(request, *args, **kwargs)

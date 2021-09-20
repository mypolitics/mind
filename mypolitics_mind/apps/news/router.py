from rest_framework import routers

from mypolitics_mind.apps.news.views import NewsPoinformowaniViewSet

news_router = routers.DefaultRouter()

news_router.register(r'newspaper/poinformowani', NewsPoinformowaniViewSet)

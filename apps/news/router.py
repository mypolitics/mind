from rest_framework import routers

from apps.news.views import NewsPoinformowaniViewSet

news_router = routers.DefaultRouter()

news_router.register(r'newspaper/poinformowani', NewsPoinformowaniViewSet)

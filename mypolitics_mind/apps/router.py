from rest_framework import routers

from mypolitics_mind.apps.news.router import news_router
from mypolitics_mind.apps.news.views import NewsPoinformowaniViewSet

router = routers.DefaultRouter()
router.registry.extend(news_router.registry)

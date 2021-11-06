from rest_framework import routers

from apps.news.router import news_router
from apps.sejm_members.router import members_router
from apps.sejm_votings.router import votings_router

router = routers.DefaultRouter()

router.registry.extend(news_router.registry)
router.registry.extend(members_router.registry)
router.registry.extend(votings_router.registry)



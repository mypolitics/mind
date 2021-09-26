from rest_framework import routers

from mypolitics_mind.apps.news.router import news_router
from mypolitics_mind.apps.sejm_members.router import members_router
from mypolitics_mind.apps.sejm_votings.router import votings_router

router = routers.DefaultRouter()

router.registry.extend(news_router.registry)
router.registry.extend(members_router.registry)
router.registry.extend(votings_router.registry)

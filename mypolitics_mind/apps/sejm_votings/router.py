from rest_framework import routers

from mypolitics_mind.apps.sejm_votings.views import VotingViewSet

votings_router = routers.DefaultRouter()

votings_router.register(r'parliament/pl/sejm/votings', VotingViewSet)

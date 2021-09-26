import base64
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from mypolitics_mind.apps.sejm_votings.models import Voting
from mypolitics_mind.apps.sejm_votings.serializers import VotingSerializer
import mypolitics_mind.apps.sejm_votings.scrapers.votings_scraper as votings_scraper


class VotingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = ['sitting', 'voting', 'date']
    filterset_fields = ['id', 'sitting']
    search_fields = ['topic', 'form']

    def list(self, request, *args, **kwargs):
        newest = self.queryset.first()
        if newest:
            votings = votings_scraper.get_new_sitting_data(newest.sitting, newest.voting)
        else:
            votings = votings_scraper.get_new_sitting_data()

        if votings:
            voting_to_save = []
            for voting in votings:
                id_slug = f'{voting["sitting"]}{voting["voting"]}{voting["date"]}'
                id_byte = bytes(id_slug, encoding='utf8')
                id = base64.urlsafe_b64encode(id_byte).decode()

                voting['id'] = id
                voting["date"] = datetime.strptime(voting["date"], '%d-%m-%Y').date()
                voting_to_save.append(Voting(**voting))

            Voting.objects.bulk_create(voting_to_save)

        return super(VotingViewSet, self).list(request, *args, **kwargs)

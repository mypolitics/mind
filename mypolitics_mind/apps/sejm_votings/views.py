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

    filterset_fields = ['sitting']
    search_fields = ['topic', 'form']
    ordering_fields = ['sitting', 'voting', 'date']

    def get_queryset(self):
        queryset = Voting.objects.all()
        ids = self.request.query_params.get('ids')
        if ids is not None:
            ids = ids.split(',')
            return queryset.filter(id__in=ids)
        return queryset

    def list(self, request, *args, **kwargs):
        newest = Voting.objects.first()
        if newest:
            votings = votings_scraper.get_sittings_data(newest.sitting, newest.voting)
        else:
            votings = votings_scraper.get_sittings_data()

        if votings:
            voting_to_save = []

            for voting in votings:
                if not voting:
                    continue

                voting['id'] = gen_id(voting)

                if voting["date"]:
                    try:
                        voting["date"] = datetime.strptime(voting["date"], '%d-%m-%Y').date()
                    except ValueError:
                        voting["date"] = None
                voting_to_save.append(Voting(**voting))

            Voting.objects.bulk_create(voting_to_save)

        return super(VotingViewSet, self).list(request, *args, **kwargs)


def gen_id(voting: dict):
    id_str = f'{votings_scraper.get_nr_kadnencji()}/{voting["sitting"]}/{voting["voting"]}'
    id_byte = bytes(id_str, encoding='utf8')
    return base64.urlsafe_b64encode(id_byte).decode()

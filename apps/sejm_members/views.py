from datetime import datetime

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import apps.sejm_members.scrapers.members_scraper as members_scraper
from apps.sejm_members.models import Members
from apps.sejm_members.serializers import MemberSerializer


class MembersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Members.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = ['pledge', 'electionDate', 'votes']
    filterset_fields = ['list']
    search_fields = ['name', 'party', 'region']

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def update_data(self, request):
        members = members_scraper.get_all_members()

        with transaction.atomic():
            new_members = []

            for member in members:
                member['electionDate'] = datetime.strptime(member['electionDate'], '%d-%m-%Y').date()
                member['pledge'] = datetime.strptime(member['pledge'], '%d-%m-%Y').date()
                new_members.append(Members(**member))

            self.queryset.delete()
            self.queryset.bulk_create(new_members)
        return Response({'status': 'updated'})

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import mypolitics_mind.apps.sejm_members.scrapers.sejm_scraper as sejm_scraper
from mypolitics_mind.apps.sejm_members.models import Members
from mypolitics_mind.apps.sejm_members.serializers import MemberSerializer


class MembersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Members.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    ordering_fields = ['pledge', 'electionDate', 'votes']
    filterset_fields = ['list']
    search_fields = ['name', 'party', 'region']

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def update_data(self, request):
        members = sejm_scraper.get_all_members()

        new_members = []

        with transaction.atomic():
            for member in members:
                member = Members(
                    name=member['name'],
                    electionDate=member['electionDate'],
                    list=member['list'],
                    region=member['region'],
                    votes=member['votes'],
                    pledge=member['pledge'],
                    experience=member['experience'],
                    party=member['party'],
                    dateOfBirth=member['dateOfBirth'],
                    education=member['education'],
                    school=member['school'],
                    job=member['job'],
                    photoUrl=member['photoUrl'],
                )
                new_members.append(member)

            self.queryset.delete()
            self.queryset.bulk_create(new_members)

        return Response({'status': 'updated', 'members_count': len(new_members)})

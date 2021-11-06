from rest_framework import routers

from apps.sejm_members.views import MembersViewSet

members_router = routers.DefaultRouter()

members_router.register(r'parliament/pl/sejm/members', MembersViewSet)

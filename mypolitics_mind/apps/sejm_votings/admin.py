from django.contrib import admin

# Register your models here.
from mypolitics_mind.apps.sejm_votings.models import Voting


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'form', 'date']
    # search_fields = ['name', 'list', 'party', 'region']
    # list_filter = ['list', 'education']

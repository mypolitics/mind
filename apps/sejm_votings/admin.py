from django.contrib import admin

# Register your models here.
from apps.sejm_votings.models import Voting


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic', 'form', 'sitting', 'voting', 'date']
    search_fields = ['topic', 'form']
    list_filter = ['date', 'sitting']

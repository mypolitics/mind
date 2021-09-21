from django.contrib import admin

# Register your models here.
from mypolitics_mind.apps.sejm_members.models import Members


@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'list', 'job', 'region', 'pledge']
    search_fields = ['name', 'list', 'party', 'region']
    list_filter = ['list', 'education']

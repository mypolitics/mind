from django.contrib import admin
from django.contrib import messages
# Register your models here.
from django.utils.translation import ngettext

from apps.sejm_members.models import Members
from apps.sejm_members.views import MembersViewSet


@admin.action(description='update members')
def update_members(model, request, queryset):
    members_view = MembersViewSet()
    update = members_view.update_data(request).data

    model.message_user(request, ngettext(
        '%d member were successfully downloaded.',
        '%d members were successfully downloaded.',
        update['members_count'],
    ) % update['members_count'], messages.SUCCESS)


@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'list', 'job', 'region', 'pledge']
    search_fields = ['name', 'list', 'party', 'region']
    list_filter = ['list', 'education']

    actions = [update_members]

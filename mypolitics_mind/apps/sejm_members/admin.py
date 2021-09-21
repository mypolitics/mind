from django.contrib import admin

# Register your models here.
from mypolitics_mind.apps.sejm_members.models import Members

admin.site.register(Members)

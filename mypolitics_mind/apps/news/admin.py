from django.contrib import admin

# Register your models here.
from mypolitics_mind.apps.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'date']
    search_fields = ['title', 'slug', 'author', 'content']
    list_filter = ['date', 'author']

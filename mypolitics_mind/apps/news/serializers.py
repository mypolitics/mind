from mypolitics_mind.apps.news.models import News
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

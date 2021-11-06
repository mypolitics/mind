from apps.news.models import News
from common.serializers import DynamicFieldsModelSerializer


class NewsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
